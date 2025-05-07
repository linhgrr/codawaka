"""
Repository for user-related database operations.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .base import BaseRepository
from models import User
from schemas import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User repository with custom user-specific methods."""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username to search for
            
        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: Email to search for
            
        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        """
        Get user by username or email.
        
        Args:
            username_or_email: Username or email to search for
            
        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(
            or_(User.username == username_or_email, User.email == username_or_email)
        ).first()
    
    def get_by_referral_code(self, referral_code: str) -> Optional[User]:
        """
        Get user by referral code.
        
        Args:
            referral_code: Referral code to search for
            
        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.referral_code == referral_code).first()
    
    def update_credits(self, user_id: int, credit_change: float) -> bool:
        """
        Update user credits.
        
        Args:
            user_id: ID of user to update
            credit_change: Amount to add or subtract from user credits
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            user = self.get(user_id)
            if user:
                user.credits += credit_change
                self.db.commit()
                return True
            return False
        except Exception as e:
            # Rollback transaction on error
            self.db.rollback()
            print(f"Error updating user credits: {str(e)}")
            raise