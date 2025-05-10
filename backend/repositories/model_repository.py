"""
Repository for model pricing related database operations.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseRepository
from models import ModelPricing
from schemas import ModelPricingCreate, ModelPricingUpdate

class ModelPricingRepository(BaseRepository[ModelPricing, ModelPricingCreate, ModelPricingUpdate]):
    """ModelPricing repository with model-specific methods."""
    
    def __init__(self, db: Session):
        super().__init__(ModelPricing, db)
    
    def get_by_model_name(self, model_name: str) -> Optional[ModelPricing]:
        """
        Get model pricing by model name.
        
        Args:
            model_name: Name of the model to search for
            
        Returns:
            ModelPricing or None if not found
        """
        return self.db.query(ModelPricing).filter(ModelPricing.model_name == model_name).first()
    
    def get_all_active_models(self) -> List[ModelPricing]:
        """
        Get all active models.
        
        Returns:
            List of active ModelPricing objects
        """
        return self.db.query(ModelPricing).filter(ModelPricing.is_active == True).all()
    
    def update_pricing(self, model_name: str, new_cost: float) -> bool:
        """
        Update the pricing for a model.
        
        Args:
            model_name: Name of the model to update
            new_cost: New credit cost per request
            
        Returns:
            True if update successful, False otherwise
        """
        model = self.get_by_model_name(model_name)
        if model:
            model.credit_cost_per_request = new_cost
            self.db.commit()
            return True
        return False