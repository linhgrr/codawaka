from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

from models import CodeGeneration


class CodeHistoryService:
    """
    Service for handling code generation history operations
    """
    
    @staticmethod
    def get_code_generation_by_id(db: Session, code_gen_id: int) -> Optional[CodeGeneration]:
        """Get a code generation record by ID"""
        return db.query(CodeGeneration).filter(CodeGeneration.id == code_gen_id).first()
    
    @staticmethod
    def get_user_code_history(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Get code generation history for a specific user"""
        return db.query(CodeGeneration).filter(
            CodeGeneration.user_id == user_id
        ).order_by(CodeGeneration.id.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_code_history(db: Session, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """Get all code generation history"""
        return db.query(CodeGeneration).order_by(
            CodeGeneration.id.desc()
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_code_history_count(db: Session, user_id: int) -> int:
        """Get the count of code generation history for a specific user"""
        return db.query(CodeGeneration).filter(CodeGeneration.user_id == user_id).count()
    
    @staticmethod
    def get_all_code_history_count(db: Session) -> int:
        """Get the count of all code generation history"""
        return db.query(CodeGeneration).count()