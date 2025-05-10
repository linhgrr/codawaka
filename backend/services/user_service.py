from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status, Request, BackgroundTasks
import random
import string
import ipaddress
import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from config import Config
from core.security import get_password_hash
from email.mime.multipart import MIMEMultipart

from models import User

RESET_PASSWORD_SECRET = Config.SECURITY.SECRET_KEY
RESET_PASSWORD_EXPIRE_MINUTES = 30
FRONTEND_BASE_URL = Config.PAYMENT.FRONTEND_BASE_URL

class UserService:
    """
    Service for handling user-related operations
    """
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by their ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get a user by their username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by their email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_referral_code(db: Session, referral_code: str) -> Optional[User]:
        """Get a user by their referral code"""
        return db.query(User).filter(User.referral_code == referral_code).first()
    
    @staticmethod
    def generate_unique_referral_code(db: Session, length: int = 8) -> str:
        """Generate a unique referral code"""
        while True:
            # Generate a random code with uppercase letters and numbers
            chars = string.ascii_uppercase + string.digits
            code = ''.join(random.choice(chars) for _ in range(length))
            
            # Check if code already exists
            existing = db.query(User).filter(User.referral_code == code).first()
            if not existing:
                return code
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_users_count(db: Session) -> int:
        """Get the count of all users"""
        return db.query(User).count()
    
    @staticmethod
    def get_users_by_ip(db: Session, ip: str) -> List[User]:
        """Get all users registered with a specific IP"""
        return db.query(User).filter(User.registration_ip == ip).all()
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, 
                   referral_code: Optional[str] = None, 
                   client_ip: Optional[str] = None,
                   is_admin: bool = False) -> User:
        """Create a new user"""
        # Check if username already exists
        if UserService.get_user_by_username(db, username):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Check if email already exists
        if UserService.get_user_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check for suspicious multi-account creation from same IP
        if client_ip:
            ip_user_count = db.query(User).filter(User.registration_ip == client_ip).count()
            if ip_user_count >= 3:  # Limit to 3 accounts per IP address
                raise HTTPException(
                    status_code=400, 
                    detail="Maximum account limit reached for your network. Please contact support."
                )
        
        # Generate unique referral code for new user
        new_referral_code = UserService.generate_unique_referral_code(db)
        
        # Create new user
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin,
            referral_code=new_referral_code,
            registration_ip=client_ip
        )
        
        # Process referral code if provided
        if referral_code:
            # Look up the referring user
            referring_user = UserService.get_user_by_referral_code(db, referral_code)
            if referring_user:
                # Set the referred_by field on the new user
                db_user.referred_by = referral_code
                
                # Add bonus credits to referring user (but only if it appears legitimate)
                # Check if referring user and new user have different IPs to prevent self-referrals
                if client_ip != referring_user.registration_ip:
                    referring_user.credits += 3  # Add 3 credits for successful referral
                    
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> User:
        """Update user details"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user attributes
        for key, value in kwargs.items():
            if hasattr(db_user, key) and value is not None:
                setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(db_user)
        db.commit()
        
        return True
    
    @staticmethod
    def add_credits(db: Session, user_id: int, amount: float) -> User:
        """Add credits to a user account"""
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_user.credits += amount
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def forgot_password(db: Session, email: str, background_tasks: BackgroundTasks):
        """Handle forgot password request"""

        user = UserService.get_user_by_email(db, email)
        if not user:
            print("Email không tồn tại")  # Không tiết lộ email tồn tại hay không
            return  # Không tiết lộ email tồn tại hay không
        # Tạo token reset password
        expire = datetime.now() + timedelta(minutes=RESET_PASSWORD_EXPIRE_MINUTES)
        payload = {"sub": user.username, "exp": expire}
        token = jwt.encode(payload, RESET_PASSWORD_SECRET, algorithm="HS256")
        # Tạo link reset password
        reset_link = f"{FRONTEND_BASE_URL}reset-password?token={token}"
        # Gửi email trong background
        background_tasks.add_task(UserService.send_reset_email, user.email, reset_link)

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str):
        try:
            payload = jwt.decode(token, RESET_PASSWORD_SECRET, algorithms=["HS256"])
            username = payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Token đã hết hạn")
        except Exception:
            raise HTTPException(status_code=400, detail="Token không hợp lệ")
        user = UserService.get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)

    @staticmethod
    def send_reset_email(email: str, reset_link: str):
        # Tạo email hỗn hợp (HTML + plain-text để phòng trường hợp client không đọc được HTML)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🔒 Đặt lại mật khẩu Codawaka"
        msg['From'] = Config.EMAIL.FROM_ADDRESS
        msg['To'] = email

        # Plain-text fallback (nếu client không hiển thị HTML)
        text = f"""
    Xin chào,

    Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn.

    Truy cập đường dẫn sau để đặt lại mật khẩu:
    {reset_link}

    Nếu bạn không yêu cầu, vui lòng bỏ qua email này.

    © 2025 Codawaka. All rights reserved.
    """

        # HTML chính
        html = f"""
    <html>
    <body style="font-family: sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <table align="center" width="600" cellpadding="0" cellspacing="0"
            style="background-color: #ffffff; border-radius: 8px; overflow: hidden; margin: 40px auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <!-- Header -->
        <tr>
            <td style="background-color: #004fff; padding: 20px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Codawaka</h1>
            </td>
        </tr>

        <!-- Body -->
        <tr>
            <td style="padding: 40px;">
            <p style="font-size: 16px; color: #333; margin-top: 0;">Xin chào,</p>
            <p style="font-size: 16px; color: #333;">
                Chúng tôi đã nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn. 
                Nhấn nút bên dưới để tiếp tục:
            </p>

            <!-- Call-to-Action Button -->
            <p style="text-align: center; margin: 40px 0;">
                <a href="{reset_link}"
                style="background-color: #004fff;
                        color: #ffffff;
                        padding: 14px 28px;
                        text-decoration: none;
                        border-radius: 4px;
                        display: inline-block;
                        font-size: 16px;">
                Đặt lại mật khẩu
                </a>
            </p>

            <p style="font-size: 14px; color: #777; line-height: 1.5;">
                Nếu nút trên không hoạt động, sao chép và dán đường dẫn sau vào trình duyệt:<br/>
                <a href="{reset_link}" style="color: #004fff;">{reset_link}</a>
            </p>

            <p style="font-size: 16px; color: #333;">
                Nếu bạn không yêu cầu, vui lòng bỏ qua email này. 
                Mọi thắc mắc vui lòng liên hệ support@codawaka.com.
            </p>
            </td>
        </tr>

        <!-- Footer -->
        <tr>
            <td style="background-color: #f4f4f4; padding: 20px; text-align: center;">
            <p style="font-size: 12px; color: #999; margin: 0;">
                © 2025 Codawaka. All rights reserved.
            </p>
            </td>
        </tr>
        </table>
    </body>
    </html>
    """

        # Đính kèm cả plain-text và HTML
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        # Gửi email
        try:
            with smtplib.SMTP(Config.EMAIL.SMTP_SERVER, Config.EMAIL.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.EMAIL.SMTP_USER, Config.EMAIL.SMTP_PASSWORD)
                server.sendmail(Config.EMAIL.FROM_ADDRESS, [email], msg.as_string())
            print(f"✅ Đã gửi email đặt lại mật khẩu đến {email}")
        except Exception as e:
            print(f"❌ Lỗi gửi email: {e}")
