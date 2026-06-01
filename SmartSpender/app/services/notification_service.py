from email.message import EmailMessage
from email.utils import formataddr
import logging
import smtplib
from typing import Optional

import httpx

from app.config import get_settings
from app.models.budget import BudgetCategory
from app.models.transaction import Transaction, TransactionType
from app.repositories.budget_repository import BudgetRepository
from app.repositories.transaction_repository import TransactionRepository

logger = logging.getLogger(__name__)

BUDGET_WARNING_THRESHOLD = 0.9
BREVO_EMAIL_URL = "https://api.brevo.com/v3/smtp/email"
RESEND_EMAIL_URL = "https://api.resend.com/emails"


class NotificationService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        budget_repo: BudgetRepository,
    ):
        self.transaction_repo = transaction_repo
        self.budget_repo = budget_repo

    def get_budget_alert_for_transaction(self, transaction: Transaction) -> Optional[dict]:
        if transaction.type != TransactionType.EXPENSE:
            return None

        month_year = transaction.date.strftime("%Y-%m")
        try:
            budget_category = BudgetCategory(transaction.category.value)
        except ValueError:
            return None

        budget = self.budget_repo.get_by_category(
            transaction.user_id,
            budget_category,
            month_year,
        )

        if not budget or budget.monthly_limit <= 0:
            return None

        month_transactions = self.transaction_repo.get_by_month(
            transaction.user_id,
            transaction.date.year,
            transaction.date.month,
        )
        spent = sum(
            txn.amount
            for txn in month_transactions
            if txn.type == TransactionType.EXPENSE and txn.category.value == budget.category.value
        )
        percentage_used = spent / budget.monthly_limit

        if percentage_used < BUDGET_WARNING_THRESHOLD:
            return None

        remaining = budget.monthly_limit - spent
        category_name = budget.category.value.replace("_", " ").title()
        is_over_budget = spent > budget.monthly_limit
        title = "Budget alert"
        message = (
            f"You are over your {category_name} budget by ${abs(remaining):.2f}."
            if is_over_budget
            else f"You are close to your {category_name} budget. ${remaining:.2f} remaining."
        )

        return {
            "title": title,
            "message": message,
            "category": budget.category.value,
            "spent": round(spent, 2),
            "budget": round(budget.monthly_limit, 2),
            "remaining": round(remaining, 2),
            "percentage_used": round(percentage_used * 100, 1),
            "level": "over_budget" if is_over_budget else "near_budget",
        }

    def send_budget_alert_email(self, recipient_email: str, alert: Optional[dict]) -> bool:
        if not alert:
            return False

        settings = get_settings()
        if settings.brevo_api_key and settings.brevo_sender_email:
            logger.info("Sending budget alert email with Brevo API.")
            return self._send_brevo_budget_alert_email(
                recipient_email,
                alert,
                settings.brevo_api_key,
                settings.brevo_sender_email,
                settings.brevo_sender_name,
            )

        if settings.resend_api_key and settings.resend_from_email:
            logger.info("Sending budget alert email with Resend.")
            return self._send_resend_budget_alert_email(
                recipient_email,
                alert,
                settings.resend_api_key,
                settings.resend_from_email,
            )

        if not settings.smtp_host or not settings.smtp_from_email:
            logger.warning(
                "Skipping budget alert email because neither Resend nor SMTP is configured."
            )
            return False

        logger.info("Sending budget alert email with SMTP.")
        return self._send_smtp_budget_alert_email(recipient_email, alert)

    def _email_body(self, alert: dict) -> str:
        return "\n".join(
            [
                alert["message"],
                "",
                f"Spent: ${alert['spent']:.2f}",
                f"Budget: ${alert['budget']:.2f}",
                f"Used: {alert['percentage_used']:.1f}%",
            ]
        )

    def _send_brevo_budget_alert_email(
        self,
        recipient_email: str,
        alert: dict,
        api_key: str,
        sender_email: str,
        sender_name: str,
    ) -> bool:
        try:
            response = httpx.post(
                BREVO_EMAIL_URL,
                headers={
                    "api-key": api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "sender": {
                        "name": sender_name,
                        "email": sender_email,
                    },
                    "to": [{"email": recipient_email}],
                    "subject": alert["title"],
                    "textContent": self._email_body(alert),
                },
                timeout=10,
            )
            if response.is_error:
                logger.warning(
                    "Brevo rejected budget alert email. Status: %s Body: %s",
                    response.status_code,
                    response.text,
                )
                return False
            return True
        except Exception as exc:
            logger.warning("Failed to send budget alert email with Brevo: %s", exc)
            return False

    def _send_resend_budget_alert_email(
        self,
        recipient_email: str,
        alert: dict,
        api_key: str,
        from_email: str,
    ) -> bool:
        try:
            response = httpx.post(
                RESEND_EMAIL_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": from_email,
                    "to": [recipient_email],
                    "subject": alert["title"],
                    "text": self._email_body(alert),
                },
                timeout=10,
            )
            if response.is_error:
                logger.warning(
                    "Resend rejected budget alert email. Status: %s Body: %s",
                    response.status_code,
                    response.text,
                )
                return False
            return True
        except Exception as exc:
            logger.warning("Failed to send budget alert email with Resend: %s", exc)
            return False

    def _send_smtp_budget_alert_email(self, recipient_email: str, alert: dict) -> bool:
        settings = get_settings()
        smtp_password = settings.smtp_password.replace(" ", "")

        message = EmailMessage()
        message["Subject"] = alert["title"]
        message["From"] = formataddr((settings.smtp_from_name, settings.smtp_from_email))
        message["To"] = recipient_email
        message.set_content(self._email_body(alert))

        try:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as smtp:
                if settings.smtp_use_tls:
                    smtp.starttls()
                if settings.smtp_username and smtp_password:
                    smtp.login(settings.smtp_username, smtp_password)
                smtp.send_message(message)
            return True
        except Exception as exc:
            logger.warning("Failed to send budget alert email: %s", exc)
            return False
