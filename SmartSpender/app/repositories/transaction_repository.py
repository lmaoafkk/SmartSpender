from sqlmodel import Session, select
from app.models.transaction import Transaction
from datetime import date
from typing import List, Optional


class TransactionRepository:
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self, user_id: int) -> List[Transaction]:
        """Get all transactions for a user"""
        return self.session.exec(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.date.desc())
        ).all()
    
    def get_by_id(self, transaction_id: int, user_id: int) -> Optional[Transaction]:
        """Get a single transaction by ID"""
        return self.session.exec(
            select(Transaction).where(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            )
        ).first()
    
    def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction"""
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction
    
    def update(self, transaction: Transaction) -> Transaction:
        """Update an existing transaction"""
        self.session.commit()
        self.session.refresh(transaction)
        return transaction
    
    def delete(self, transaction: Transaction) -> None:
        """Delete a transaction"""
        self.session.delete(transaction)
        self.session.commit()
    
    def get_by_month(self, user_id: int, year: int, month: int) -> List[Transaction]:
        """Get transactions for a specific month and year"""
        start_date = date(year, month, 1)
        
        # Calculate end date (first day of next month)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        return self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date < end_date
            )
        ).all()
    
    def get_by_date_range(self, user_id: int, start_date: date, end_date: date) -> List[Transaction]:
        """Get transactions within a date range"""
        return self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        ).all()
    
    def get_by_type(self, user_id: int, transaction_type: str) -> List[Transaction]:
        """Get transactions by type (income or expense)"""
        return self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.type == transaction_type
            )
        ).all()
    
    def get_by_category(self, user_id: int, category: str) -> List[Transaction]:
        """Get transactions by category"""
        return self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.category == category
            )
        ).all()
    
    def get_subscriptions(self, user_id: int) -> List[Transaction]:
        """Get all subscription transactions"""
        return self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.is_subscription == True
            )
        ).all()
    
    def get_income_total(self, user_id: int) -> float:
        """Get total income for a user"""
        transactions = self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.type == "income"
            )
        ).all()
        return sum(t.amount for t in transactions)
    
    def get_expense_total(self, user_id: int) -> float:
        """Get total expenses for a user"""
        transactions = self.session.exec(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.type == "expense"
            )
        ).all()
        return sum(t.amount for t in transactions)