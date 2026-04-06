from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date as DateType, datetime
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    BILLS = "bills"
    HEALTH = "health"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Netflix", "Uber", "Groceries"
    amount: float
    type: TransactionType  # income or expense
    category: TransactionCategory
    is_subscription: bool = False
    is_recurring: bool = False
    next_billing_date: Optional[DateType] = None
    date: DateType = Field(default_factory=lambda: DateType.today())
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")