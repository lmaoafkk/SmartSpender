from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from app.dependencies import SessionDep, AuthDep
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.budget_repository import BudgetRepository
from app.services.report_service import ReportService
from app.models.transaction import Transaction, TransactionType, TransactionCategory
from app.models.budget import Budget, BudgetCategory
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.schemas.budget import BudgetCreate
from datetime import date
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/finance", tags=["finance"])
templates = None


def set_templates(templates_instance):
    global templates
    templates = templates_instance


# ============ PAGE ROUTES ============

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, session: SessionDep, current_user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="finance/dashboard.html",
        context={"user": current_user}
    )


@router.get("/transactions", response_class=HTMLResponse)
async def transactions_page(request: Request, session: SessionDep, current_user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="finance/transactions.html",
        context={"user": current_user}
    )


@router.get("/recurring", response_class=HTMLResponse)
async def recurring_page(request: Request, session: SessionDep, current_user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="finance/recurring.html",
        context={"user": current_user}
    )


@router.get("/budget", response_class=HTMLResponse)
async def budget_page(request: Request, session: SessionDep, current_user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="finance/budget.html",
        context={"user": current_user}
    )


@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request, session: SessionDep, current_user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="finance/analytics.html",
        context={
            "user": current_user,
            "current_date": datetime.now()
        }
    )


# ============ API ROUTES ============

@router.get("/api/transactions")
async def get_transactions(session: SessionDep, current_user: AuthDep):
    repo = TransactionRepository(session)
    transactions = repo.get_all(current_user.id)
    
    return [
        {
            "id": t.id,
            "name": t.name,
            "amount": t.amount,
            "type": t.type.value,
            "category": t.category.value,
            "is_subscription": t.is_subscription,
            "is_recurring": t.is_recurring,
            "next_billing_date": t.next_billing_date.isoformat() if t.next_billing_date else None,
            "date": t.date.isoformat()
        }
        for t in transactions
    ]


@router.post("/api/transactions")
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep, current_user: AuthDep):
    repo = TransactionRepository(session)
    
    transaction = Transaction(
        name=transaction_data.name,
        amount=transaction_data.amount,
        type=transaction_data.type,
        category=transaction_data.category,
        is_subscription=transaction_data.is_subscription,
        is_recurring=transaction_data.is_recurring,
        next_billing_date=transaction_data.next_billing_date,
        date=transaction_data.date,
        user_id=current_user.id
    )
    
    created = repo.create(transaction)
    
    return {
        "id": created.id,
        "name": created.name,
        "amount": created.amount,
        "type": created.type.value,
        "category": created.category.value,
        "date": created.date.isoformat()
    }


@router.delete("/api/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, session: SessionDep, current_user: AuthDep):
    repo = TransactionRepository(session)
    transaction = repo.get_by_id(transaction_id, current_user.id)
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    repo.delete(transaction)
    return {"message": "Transaction deleted"}


@router.get("/api/reports/summary")
async def get_summary(session: SessionDep, current_user: AuthDep, month: Optional[str] = None):
    txn_repo = TransactionRepository(session)
    budget_repo = BudgetRepository(session)
    service = ReportService(txn_repo, budget_repo)
    
    return service.get_summary(current_user.id, current_user.salary, month)


@router.get("/api/reports/category-breakdown")
async def get_category_breakdown(session: SessionDep, current_user: AuthDep):
    txn_repo = TransactionRepository(session)
    budget_repo = BudgetRepository(session)
    service = ReportService(txn_repo, budget_repo)
    
    return service.get_category_breakdown(current_user.id)


@router.get("/api/reports/monthly-trends")
async def get_monthly_trends(session: SessionDep, current_user: AuthDep, months: int = 6):
    txn_repo = TransactionRepository(session)
    budget_repo = BudgetRepository(session)
    service = ReportService(txn_repo, budget_repo)
    
    return service.get_monthly_trends(current_user.id, months)


@router.get("/api/reports/budget-status")
async def get_budget_status(session: SessionDep, current_user: AuthDep, month: Optional[str] = None):
    txn_repo = TransactionRepository(session)
    budget_repo = BudgetRepository(session)
    service = ReportService(txn_repo, budget_repo)
    
    return service.get_budget_status(current_user.id, month)


@router.post("/api/budgets")
async def create_or_update_budget(budget_data: BudgetCreate, session: SessionDep, current_user: AuthDep):
    repo = BudgetRepository(session)
    
    budget = Budget(
        category=budget_data.category,
        monthly_limit=budget_data.monthly_limit,
        month_year=budget_data.month_year,
        user_id=current_user.id
    )
    
    result = repo.create_or_update(budget)
    
    return {
        "id": result.id,
        "category": result.category.value,
        "monthly_limit": result.monthly_limit,
        "month_year": result.month_year
    }


@router.put("/api/user/salary")
async def update_salary(salary: float, session: SessionDep, current_user: AuthDep):
    current_user.salary = salary
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return {"message": "Salary updated", "salary": current_user.salary}


@router.post("/api/user/refresh")
async def refresh_user_data(session: SessionDep, current_user: AuthDep):
    # Delete all transactions for this user
    txn_repo = TransactionRepository(session)
    all_transactions = txn_repo.get_all(current_user.id)
    for txn in all_transactions:
        txn_repo.delete(txn)
    
    # Delete all budgets for this user
    budget_repo = BudgetRepository(session)
    all_budgets = budget_repo.get_all(current_user.id)
    for budget in all_budgets:
        budget_repo.delete(budget.id, current_user.id)
    
    # Reset salary to 0
    current_user.salary = 0.0
    session.add(current_user)
    session.commit()
    session.expire_all()
    session.refresh(current_user)
    return {"message": "User data refreshed successfully - all transactions, budgets, and salary cleared"}