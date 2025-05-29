from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

from models import User
from core.security import get_password_hash


class UserService:
    """
    Service for handling user-related operations
    """
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by their ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get a user by their username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by their email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_users_count(db: Session) -> int:
        """Get the count of all users"""
        return db.query(User).count()
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, is_admin: bool = False) -> User:
        """Create a new user"""
        # Check if username already exists
        if UserService.get_user_by_username(db, username):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Check if email already exists
        if UserService.get_user_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> User:
        """Update user details"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user attributes
        for key, value in kwargs.items():
            if hasattr(db_user, key) and value is not None:
                setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(db_user)
        db.commit()
        
        return True
    
    @staticmethod
    def add_credits(db: Session, user_id: int, amount: float) -> User:
        """Add credits to a user account"""
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_user.credits += amount
        db.commit()
        db.refresh(db_user)
        
        return db_user