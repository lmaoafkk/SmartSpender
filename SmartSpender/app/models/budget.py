from sqlmodel import Field, SQLModel
from typing import Optional
from enum import Enum


class BudgetCategory(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    BILLS = "bills"
    HEALTH = "health"
    OTHER = "other"


class Budget(SQLModel, table=True):
    __tablename__ = "budgets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    category: BudgetCategory
    monthly_limit: float
    month_year: str  # Format: "2026-04" for April 2026
    user_id: int = Field(foreign_key="user.id")