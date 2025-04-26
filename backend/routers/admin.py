from datetime import timedelta
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import User as UserSchema
from schemas import ModelPricing, ModelPricingCreate, ModelPricingUpdate, UserUpdate, CodeGeneration, UserCreate, PaymentTransaction
from core.security import get_current_admin_user
from services.user_service import UserService
from services.model_service import ModelService
from services.code_history_service import CodeHistoryService
from services.payment_service import PaymentService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)],  # All routes require admin privileges
    responses={
        403: {"description": "Forbidden - Admin access required"},
        404: {"description": "Not found"}
    },
)

# User management endpoints
@router.get("/users", response_model=List[UserSchema])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    return UserService.get_all_users(db, skip, limit)


@router.get("/users/count", response_model=dict)
def get_all_users_count(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get the count of all users (admin only)"""
    count = UserService.get_all_users_count(db)
    return {"count": count}


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get user details by ID (admin only)"""
    return UserService.get_user_by_id(db, user_id)


@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update user details (admin only)"""
    return UserService.update_user(
        db=db, 
        user_id=user_id, 
        **user_update.model_dump(exclude_unset=True)
    )


@router.post("/users/{user_id}/add-credits")
def add_user_credits(
    user_id: int,
    amount: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Add credits to a user (admin only)"""
    updated_user = UserService.add_credits(db, user_id, amount)
    return {
        "message": f"Added {amount} credits to user {updated_user.username}",
        "current_credits": updated_user.credits
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete a user (admin only)"""
    UserService.delete_user(db, user_id)
    return {"message": "User deleted successfully"}


# Model management endpoints
@router.post("/models", response_model=ModelPricing)
def create_model(
    model: ModelPricingCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create a new model (admin only)"""
    return ModelService.create_model(
        db=db,
        model_name=model.model_name,
        credit_cost_per_request=model.credit_cost_per_request,
        description=model.description
    )


@router.put("/models/{model_id}", response_model=ModelPricing)
def update_model(
    model_id: int,
    model_update: ModelPricingUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update model details (admin only)"""
    return ModelService.update_model(
        db=db,
        model_id=model_id,
        credit_cost_per_request=model_update.credit_cost_per_request,
        description=model_update.description
    )


@router.delete("/models/{model_id}")
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete a model (admin only)"""
    ModelService.delete_model(db, model_id)
    return {"message": "Model deleted successfully"}


# Code generation history endpoints
@router.get("/code-history", response_model=List[CodeGeneration])
def get_all_code_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get all code generation history across all users (admin only)"""
    return CodeHistoryService.get_all_code_history(db, skip, limit)


@router.get("/code-history/count", response_model=dict)
def get_all_code_history_count(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get the count of all code generation history (admin only)"""
    count = CodeHistoryService.get_all_code_history_count(db)
    return {"count": count}


# Payment transaction endpoints
@router.get("/payment-transactions", response_model=List[PaymentTransaction])
def get_all_payment_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Lấy tất cả các giao dịch thanh toán (chỉ admin)"""
    return PaymentService.get_all_payment_transactions(db, skip, limit)


@router.get("/payment-transactions/count", response_model=dict)
def get_all_payment_transactions_count(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get the count of all payment transactions (admin only)"""
    count = PaymentService.get_all_payment_transactions_count(db)
    return {"count": count}


@router.get("/payment-statistics", response_model=Dict[str, Any])
def get_payment_statistics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Lấy thống kê tổng quan về các giao dịch thanh toán (chỉ admin)"""
    return PaymentService.get_payment_statistics(db)


# Admin management
@router.post("/create-admin", response_model=UserSchema)
def admin_create_admin(
    admin_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create a new admin user (admin only)"""
    return UserService.create_user(
        db=db,
        username=admin_data.username,
        email=admin_data.email,
        password=admin_data.password,
        is_admin=True
    )


@router.get("/users/{user_id}/transactions", response_model=List[PaymentTransaction])
def get_user_payment_transactions(
    user_id: int,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Lấy lịch sử giao dịch của một người dùng cụ thể (chỉ admin)"""
    return PaymentService.get_user_payment_transactions(db, user_id, skip, limit)