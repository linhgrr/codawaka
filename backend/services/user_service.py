from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status, Request
import random
import string
import ipaddress

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
    def get_user_by_referral_code(db: Session, referral_code: str) -> Optional[User]:
        """Get a user by their referral code"""
        return db.query(User).filter(User.referral_code == referral_code).first()
    
    @staticmethod
    def generate_unique_referral_code(db: Session, length: int = 8) -> str:
        """Generate a unique referral code"""
        while True:
            # Generate a random code with uppercase letters and numbers
            chars = string.ascii_uppercase + string.digits
            code = ''.join(random.choice(chars) for _ in range(length))
            
            # Check if code already exists
            existing = db.query(User).filter(User.referral_code == code).first()
            if not existing:
                return code
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_users_count(db: Session) -> int:
        """Get the count of all users"""
        return db.query(User).count()
    
    @staticmethod
    def get_users_by_ip(db: Session, ip: str) -> List[User]:
        """Get all users registered with a specific IP"""
        return db.query(User).filter(User.registration_ip == ip).all()
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, 
                   referral_code: Optional[str] = None, 
                   client_ip: Optional[str] = None,
                   is_admin: bool = False) -> User:
        """Create a new user"""
        # Check if username already exists
        if UserService.get_user_by_username(db, username):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Check if email already exists
        if UserService.get_user_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check for suspicious multi-account creation from same IP
        if client_ip:
            ip_user_count = db.query(User).filter(User.registration_ip == client_ip).count()
            if ip_user_count >= 3:  # Limit to 3 accounts per IP address
                raise HTTPException(
                    status_code=400, 
                    detail="Maximum account limit reached for your network. Please contact support."
                )
        
        # Generate unique referral code for new user
        new_referral_code = UserService.generate_unique_referral_code(db)
        
        # Create new user
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin,
            referral_code=new_referral_code,
            registration_ip=client_ip
        )
        
        # Process referral code if provided
        if referral_code:
            # Look up the referring user
            referring_user = UserService.get_user_by_referral_code(db, referral_code)
            if referring_user:
                # Set the referred_by field on the new user
                db_user.referred_by = referral_code
                
                # Add bonus credits to referring user (but only if it appears legitimate)
                # Check if referring user and new user have different IPs to prevent self-referrals
                if client_ip != referring_user.registration_ip:
                    referring_user.credits += 3  # Add 3 credits for successful referral
                    
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