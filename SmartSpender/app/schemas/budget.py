from pydantic import BaseModel
from typing import Optional
from app.models.budget import BudgetCategory


class BudgetCreate(BaseModel):
    category: BudgetCategory
    monthly_limit: float
    month_year: str


class BudgetResponse(BaseModel):
    id: int
    category: BudgetCategory
    monthly_limit: float
    month_year: str
    
    class Config:
        from_attributes = True


class BudgetUpdate(BaseModel):
    monthly_limit: float