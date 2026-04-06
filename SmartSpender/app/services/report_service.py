from app.repositories.transaction_repository import TransactionRepository
from app.repositories.budget_repository import BudgetRepository
from app.models.transaction import TransactionCategory
from datetime import date
from collections import defaultdict
from typing import List, Dict


class ReportService:
    
    def __init__(self, transaction_repo: TransactionRepository, budget_repo: BudgetRepository):
        self.transaction_repo = transaction_repo
        self.budget_repo = budget_repo
    
    def get_summary(self, user_id: int, salary: float, month_year: str = None) -> dict:
        transactions = self.transaction_repo.get_all(user_id)
        
        total_income = sum(t.amount for t in transactions if t.type.value == "income")
        total_expenses = sum(t.amount for t in transactions if t.type.value == "expense")
        
        # Include salary in total income
        total_income += salary
        
        net_savings = total_income - total_expenses
        burn_rate = (total_expenses / total_income * 100) if total_income > 0 else 0
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_savings": net_savings,
            "burn_rate": round(burn_rate, 1),
            "salary": salary,
            "month": month_year
        }
    
    def get_category_breakdown(self, user_id: int) -> List[dict]:
        transactions = self.transaction_repo.get_all(user_id)
        expenses = [t for t in transactions if t.type.value == "expense"]
        
        total_expenses = sum(t.amount for t in expenses)
        
        breakdown = defaultdict(float)
        for t in expenses:
            breakdown[t.category.value] += t.amount
        
        result = []
        for category, amount in breakdown.items():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            result.append({
                "category": category,
                "amount": amount,
                "percentage": round(percentage, 1)
            })
        
        return sorted(result, key=lambda x: x["amount"], reverse=True)
    
    def get_monthly_trends(self, user_id: int, months: int = 6) -> dict:
        today = date.today()
        trends = defaultdict(lambda: {"income": 0, "expense": 0})
        
        for i in range(months):
            year = today.year
            month = today.month - i
            if month <= 0:
                month += 12
                year -= 1
            
            transactions = self.transaction_repo.get_by_month(user_id, year, month)
            month_key = f"{year}-{month:02d}"
            
            for t in transactions:
                if t.type.value == "income":
                    trends[month_key]["income"] += t.amount
                else:
                    trends[month_key]["expense"] += t.amount
        
        sorted_months = sorted(trends.keys())
        
        return {
            "months": sorted_months,
            "income": [trends[m]["income"] for m in sorted_months],
            "expenses": [trends[m]["expense"] for m in sorted_months]
        }
    
    def get_budget_status(self, user_id: int, month_year: str = None) -> List[dict]:
        if not month_year:
            month_year = date.today().strftime("%Y-%m")
        
        budgets = self.budget_repo.get_all(user_id, month_year)
        
        year, month = map(int, month_year.split("-"))
        transactions = self.transaction_repo.get_by_month(user_id, year, month)
        expenses = [t for t in transactions if t.type.value == "expense"]
        
        spent_by_category = defaultdict(float)
        for t in expenses:
            spent_by_category[t.category.value] += t.amount
        
        result = []
        for budget in budgets:
            spent = spent_by_category.get(budget.category.value, 0)
            remaining = budget.monthly_limit - spent
            percentage_used = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
            
            result.append({
                "category": budget.category.value,
                "budget": budget.monthly_limit,
                "spent": spent,
                "remaining": remaining,
                "status": "on_track" if spent <= budget.monthly_limit else "over_budget",
                "percentage_used": round(percentage_used, 1)
            })
        
        return result
    
    def get_subscription_total(self, user_id: int) -> float:
        subscriptions = self.transaction_repo.get_subscriptions(user_id)
        return sum(s.amount for s in subscriptions)