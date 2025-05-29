from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool = False  # Thêm trường is_admin
    credits: float

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