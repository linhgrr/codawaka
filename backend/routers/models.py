from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import ModelPricing, ModelPricingCreate, ModelPricingUpdate
from core.security import get_current_active_user
from services.model_service import ModelService

router = APIRouter(
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ModelPricing])
def get_all_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all available models"""
    return ModelService.get_all_models(db)


@router.post("/", response_model=ModelPricing)
def create_model_pricing(
    model: ModelPricingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new model (admin only)"""
    # Kiểm tra quyền admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không đủ quyền. Chỉ admin mới có thể tạo model mới."
        )
    
    return ModelService.create_model(
        db=db,
        model_name=model.model_name,
        credit_cost_per_request=model.credit_cost_per_request,
        description=model.description
    )