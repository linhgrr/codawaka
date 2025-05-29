from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

from models import ModelPricing


class ModelService:
    """
    Service for handling model pricing operations
    """
    
    @staticmethod
    def get_model_by_id(db: Session, model_id: int) -> Optional[ModelPricing]:
        """Get a model by ID"""
        return db.query(ModelPricing).filter(ModelPricing.id == model_id).first()
    
    @staticmethod
    def get_model_by_name(db: Session, model_name: str) -> Optional[ModelPricing]:
        """Get a model by name"""
        return db.query(ModelPricing).filter(ModelPricing.model_name == model_name).first()
    
    @staticmethod
    def get_all_models(db: Session) -> List[ModelPricing]:
        """Get all models"""
        return db.query(ModelPricing).all()
    
    @staticmethod
    def create_model(
        db: Session, 
        model_name: str, 
        credit_cost_per_request: float, 
        description: Optional[str] = None
    ) -> ModelPricing:
        """Create a new model pricing"""
        # Check if model already exists
        existing_model = ModelService.get_model_by_name(db, model_name)
        if existing_model:
            raise HTTPException(status_code=400, detail="Model already exists")
        
        # Create new model
        db_model = ModelPricing(
            model_name=model_name,
            credit_cost_per_request=credit_cost_per_request,
            description=description
        )
        
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        
        return db_model
    
    @staticmethod
    def update_model(
        db: Session, 
        model_id: int, 
        credit_cost_per_request: Optional[float] = None,
        description: Optional[str] = None
    ) -> ModelPricing:
        """Update a model pricing"""
        db_model = ModelService.get_model_by_id(db, model_id)
        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # Update fields
        if credit_cost_per_request is not None:
            db_model.credit_cost_per_request = credit_cost_per_request
        
        if description is not None:
            db_model.description = description
        
        db.commit()
        db.refresh(db_model)
        
        return db_model
    
    @staticmethod
    def delete_model(db: Session, model_id: int) -> bool:
        """Delete a model pricing"""
        db_model = ModelService.get_model_by_id(db, model_id)
        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        db.delete(db_model)
        db.commit()
        
        return True