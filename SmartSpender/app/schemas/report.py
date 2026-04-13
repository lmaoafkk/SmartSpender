from pydantic import BaseModel
from typing import List, Dict, Optional


class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    burn_rate: float
    salary: float
    month: str


class CategoryBreakdownResponse(BaseModel):
    category: str
    amount: float
    percentage: float


class MonthlyTrendResponse(BaseModel):
    months: List[str]
    income: List[float]
    expenses: List[float]


class BudgetStatusResponse(BaseModel):
    id: int
    category: str
    budget: float
    spent: float
    remaining: float
    status: str  # "on_track" or "over_budget"
    percentage_used: float
