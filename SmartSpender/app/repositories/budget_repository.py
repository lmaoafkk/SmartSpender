from sqlmodel import Session, select
from app.models.budget import Budget, BudgetCategory
from typing import List, Optional


class BudgetRepository:
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self, user_id: int, month_year: Optional[str] = None) -> List[Budget]:
        query = select(Budget).where(Budget.user_id == user_id)
        if month_year:
            query = query.where(Budget.month_year == month_year)
        return self.session.exec(query).all()
    
    def get_by_category(self, user_id: int, category: BudgetCategory, month_year: str) -> Optional[Budget]:
        return self.session.exec(
            select(Budget).where(
                Budget.user_id == user_id,
                Budget.category == category,
                Budget.month_year == month_year
            )
        ).first()
    
    def create_or_update(self, budget: Budget) -> Budget:
        existing = self.get_by_category(
            budget.user_id, 
            budget.category, 
            budget.month_year
        )
        
        if existing:
            existing.monthly_limit = budget.monthly_limit
            self.session.commit()
            self.session.refresh(existing)
            return existing
        else:
            self.session.add(budget)
            self.session.commit()
            self.session.refresh(budget)
            return budget
    
    def delete(self, budget_id: int, user_id: int) -> bool:
        budget = self.session.exec(
            select(Budget).where(Budget.id == budget_id, Budget.user_id == user_id)
        ).first()
        
        if budget:
            self.session.delete(budget)
            self.session.commit()
            return True
        return False