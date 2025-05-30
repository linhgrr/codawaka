from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import User
from core.security import get_current_active_user
from services.user_service import UserService
from models import User as UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.get("/me/credits")
async def read_user_credits(current_user: User = Depends(get_current_active_user)):
    """Get current user's credits"""
    return {"credits": current_user.credits}


@router.get("/me/referrals")
async def read_user_referrals(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get referral statistics for current user"""
    # Get users who used this user's referral code
    referral_count = db.query(UserModel).filter(
        UserModel.referred_by == current_user.referral_code
    ).count()
    
    return {
        "referral_code": current_user.referral_code,
        "total_referrals": referral_count,
        "referral_link": f"/register?ref={current_user.referral_code}"
    }