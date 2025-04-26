from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    credits = Column(Float, default=2)  # Default credits changed from 10 to 2
    # Các cột mới thêm nullable=True để tương thích với db hiện tại
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(String, nullable=True)
    registration_ip = Column(String)
    
    # Relationship to CodeGeneration
    code_generations = relationship("CodeGeneration", back_populates="user")
    # Relationship to PaymentTransaction
    payment_transactions = relationship("PaymentTransaction", back_populates="user")


class ModelPricing(Base):
    __tablename__ = "model_pricing"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, unique=True, index=True)
    credit_cost_per_request = Column(Float)
    description = Column(Text, nullable=True)


class CodeGeneration(Base):
    __tablename__ = "code_generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_name = Column(String, index=True)
    prompt = Column(Text)
    generated_code = Column(Text, nullable=True)
    credits_used = Column(Float)
    timestamp = Column(String)  # ISO format timestamp
    
    # Relationship to User
    user = relationship("User", back_populates="code_generations")


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)  # Amount in VND
    credits = Column(Integer)  # Number of credits purchased
    transaction_id = Column(String, unique=True, index=True)  # PayOS transaction ID
    status = Column(String)  # pending, completed, failed
    created_at = Column(String)  # ISO format timestamp
    completed_at = Column(String, nullable=True)  # ISO format timestamp when payment completed
    
    # Relationship to User
    user = relationship("User", back_populates="payment_transactions")