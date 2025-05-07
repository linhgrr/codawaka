"""
Repository for code generation related database operations.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from .base import BaseRepository
from models import CodeGeneration, User
from schemas import CodeGenerationCreate, CodeGenerationUpdate

class CodeGenerationRepository(BaseRepository[CodeGeneration, CodeGenerationCreate, CodeGenerationUpdate]):
    """CodeGeneration repository with code generation specific methods."""
    
    def __init__(self, db: Session):
        super().__init__(CodeGeneration, db)
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CodeGeneration]:
        """
        Get code generation history for a user.
        
        Args:
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of CodeGeneration objects
        """
        return self.db.query(CodeGeneration)\
            .filter(CodeGeneration.user_id == user_id)\
            .order_by(CodeGeneration.id.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def count_by_user_id(self, user_id: int) -> int:
        """
        Count code generations for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Number of code generations
        """
        return self.db.query(CodeGeneration).filter(CodeGeneration.user_id == user_id).count()
    
    def create_generation(
        self, 
        user_id: int,
        model_name: str,
        prompt: str,
        generated_code: str,
        credits_used: float
    ) -> CodeGeneration:
        """
        Create a new code generation record.
        
        Args:
            user_id: ID of the user
            model_name: Name of the model used
            prompt: The code generation prompt
            generated_code: The generated code
            credits_used: Credits used for the generation
            
        Returns:
            Created CodeGeneration object
        """
        try:
            code_gen = CodeGeneration(
                user_id=user_id,
                model_name=model_name,
                prompt=prompt,
                generated_code=generated_code,
                credits_used=credits_used,
                timestamp=datetime.utcnow().isoformat()
            )
            
            self.db.add(code_gen)
            self.db.commit()
            self.db.refresh(code_gen)
            
            return code_gen
        except Exception as e:
            # Rollback transaction on error
            self.db.rollback()
            print(f"Error creating code generation record: {str(e)}")
            raise