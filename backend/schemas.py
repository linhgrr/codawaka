from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    referral_code: Optional[str] = None  # Optional referral code field


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool = False
    credits: float
    referral_code: str  # User's own referral code
    referred_by: Optional[str] = None  # Referral code of the user who referred this user

    class Config:
        from_attributes = True


# Admin schema cho cập nhật người dùng
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    credits: Optional[float] = None


# ModelPricing schemas
class ModelPricingBase(BaseModel):
    model_name: str
    credit_cost_per_request: float
    description: Optional[str] = None


class ModelPricingCreate(ModelPricingBase):
    pass


class ModelPricing(ModelPricingBase):
    id: int

    class Config:
        from_attributes = True


# Schema cho cập nhật Model Pricing
class ModelPricingUpdate(BaseModel):
    credit_cost_per_request: Optional[float] = None
    description: Optional[str] = None


# CodeGeneration schemas
class CodeGenerationBase(BaseModel):
    model_name: str
    prompt: str
    language: Optional[str] = None  # Optional language parameter, defaults to None (will use C++ if not specified)


class CodeGenerationCreate(CodeGenerationBase):
    pass


class CodeGenerationUpdate(BaseModel):
    model_name: Optional[str] = None
    prompt: Optional[str] = None
    generated_code: Optional[str] = None
    credits_used: Optional[float] = None
    language: Optional[str] = None


class CodeGenerationByUsername(CodeGenerationBase):
    username: str


class CodeGeneration(CodeGenerationBase):
    id: int
    user_id: int
    generated_code: Optional[str] = None
    credits_used: float
    timestamp: str

    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Payment schemas
class PaymentCreate(BaseModel):
    credits: int  # Number of credits to purchase


class PaymentResponse(BaseModel):
    checkout_url: str  # URL to redirect user for payment
    qr_code: str  # Base64 encoded QR code image
    transaction_id: str  # PayOS transaction ID
    amount: int  # Amount in VND
    credits: int  # Number of credits purchased


class PaymentTransaction(BaseModel):
    id: int
    user_id: int
    amount: int
    credits: int
    transaction_id: str
    status: str
    created_at: str
    completed_at: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentVerify(BaseModel):
    transaction_id: str


# Forgot password schemas
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str