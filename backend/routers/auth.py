from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User  # Đảm bảo import User từ models, không phải từ schemas
from schemas import Token, UserCreate, User as UserSchema  # Đổi tên tránh xung đột
from core.security import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from services.user_service import UserService

router = APIRouter(
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/register", response_model=UserSchema)
def register_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Register a new user"""
    # Get client IP address for anti-fraud checks
    client_ip = request.client.host if request.client else None
    
    return UserService.create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password,
        referral_code=user.referral_code,
        client_ip=client_ip
    )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Get access token using username and password"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create-admin", response_model=UserSchema)
def create_admin_user(
    admin: UserCreate,
    db: Session = Depends(get_db)
):
    """Create the first admin user (only works if no admin exists)"""
    # Check if any admin already exists
    try:
        existing_admin = db.query(User).filter(User.is_admin == True).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error: {}".format(str(e))
        )
    if existing_admin:
        # Admin already exists, require authentication
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin already exists. Only current admins can create new admins."
        )
    
    # No admin exists yet, allow creating the first admin
    return UserService.create_user(
        db=db,
        username=admin.username,
        email=admin.email,
        password=admin.password,
        is_admin=True
    )