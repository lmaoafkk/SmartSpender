from pydantic import BaseModel, Field
from datetime import date as DateType
from typing import Optional
from app.models.transaction import TransactionType, TransactionCategory


class TransactionCreate(BaseModel):
    name: str
    amount: float
    type: TransactionType
    category: TransactionCategory
    is_subscription: bool = False
    is_recurring: bool = False
    next_billing_date: Optional[DateType] = None
    date: DateType = Field(default_factory=lambda: DateType.today())


class TransactionResponse(BaseModel):
    id: int
    name: str
    amount: float
    type: TransactionType
    category: TransactionCategory
    is_subscription: bool
    is_recurring: bool
    next_billing_date: Optional[DateType]
    date: DateType
    
    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[TransactionCategory] = None
    date: Optional[DateType] = None