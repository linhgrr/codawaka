import base64
from datetime import datetime
from typing import Dict, Any
import qrcode
from io import BytesIO
import logging

# Import PayOS SDK và các kiểu dữ liệu cần thiết
from payos import PayOS, PaymentData, ItemData

from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PaymentTransaction, User
from config import Config

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo PayOS SDK client
try:
    payos_client = PayOS(
        client_id=Config.PAYMENT.PAYOS_CLIENT_ID,
        api_key=Config.PAYMENT.PAYOS_API_KEY,
        checksum_key=Config.PAYMENT.PAYOS_CHECKSUM_KEY
    )
    logger.info("PayOS SDK đã được khởi tạo thành công")
except Exception as e:
    logger.error(f"Không thể khởi tạo PayOS SDK: {str(e)}")
    raise ValueError(f"Không thể khởi tạo PayOS SDK: {str(e)}")

class PaymentService:
    @staticmethod
    def create_payment(db: Session, user_id: int, credits: int) -> Dict[str, Any]:
        """
        Tạo một giao dịch thanh toán với PayOS
        """
        # Xác thực yêu cầu credit tối thiểu
        if credits < Config.PAYMENT.MIN_CREDITS:
            raise ValueError(f"Yêu cầu tối thiểu {Config.PAYMENT.MIN_CREDITS} credits")
        
        # Tính toán số tiền cần thanh toán (VND)
        amount = credits * Config.PAYMENT.CREDIT_PRICE
        
        # Lấy thông tin người dùng
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Không tìm thấy người dùng")
        
        # Tạo mã đơn hàng duy nhất
        order_code = int(f"{user_id}{int(datetime.now().timestamp())}")
        
        # Tạo dữ liệu item theo mô hình ItemData của PayOS
        item = ItemData(
            name="Credits",
            quantity=credits,
            price=Config.PAYMENT.CREDIT_PRICE
        )
        
        # Tạo dữ liệu thanh toán theo mô hình PaymentData của PayOS
        payment_data = PaymentData(
            orderCode=order_code,
            amount=amount,
            description=f"Mua {credits} credits",
            items=[item],
            cancelUrl=Config.PAYMENT.PAYMENT_CANCEL_URL,
            returnUrl=Config.PAYMENT.PAYMENT_SUCCESS_URL
        )
        
        try:
            # Gọi API tạo link thanh toán qua PayOS SDK
            logger.info(f"Tạo thanh toán với PayOS SDK: orderCode={order_code}, amount={amount}")
            result = payos_client.createPaymentLink(paymentData=payment_data)
            logger.info(f"Kết quả từ PayOS SDK: {result.to_json() if hasattr(result, 'to_json') else result}")
            
            # Lấy thông tin từ kết quả thanh toán
            payment_link_id = result.paymentLinkId
            checkout_url = result.checkoutUrl
            qr_code_data = result.qrCode
            
            # Lưu thông tin giao dịch vào cơ sở dữ liệu
            transaction = PaymentTransaction(
                user_id=user_id,
                amount=amount,
                credits=credits,
                transaction_id=payment_link_id,
                status="pending",
                created_at=datetime.now().isoformat(),
                completed_at=None
            )
            
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            
            # Tạo mã QR từ dữ liệu QR nếu không có sẵn
            if not qr_code_data:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(checkout_url)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered)
                qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            else:
                qr_code_base64 = qr_code_data
            
            # Trả về thông tin thanh toán
            return {
                "checkout_url": checkout_url,
                "qr_code": qr_code_base64,
                "transaction_id": payment_link_id,
                "amount": amount,
                "credits": credits
            }
            
        except Exception as e:
            logger.error(f"Lỗi khi tạo thanh toán với PayOS: {str(e)}")
            raise ValueError(f"Lỗi khi tạo thanh toán: {str(e)}")
    
    @staticmethod
    def verify_payment(db: Session, transaction_id: str) -> bool:
        """
        Xác minh trạng thái thanh toán với PayOS
        """
        try:
            # Kiểm tra xem giao dịch đã được xử lý trước đó chưa
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.transaction_id == transaction_id
            ).first()
            
            if not transaction:
                logger.warning(f"Không tìm thấy giao dịch với ID: {transaction_id}")
                raise ValueError("Không tìm thấy giao dịch")
            
            # Nếu giao dịch đã được hoàn thành trước đó, trả về thành công ngay
            if transaction.status == "completed":
                logger.info(f"Giao dịch {transaction_id} đã được xử lý trước đó, không cần xác minh lại")
                return True
                
            # Sử dụng PayOS SDK để kiểm tra thông tin thanh toán
            logger.info(f"Xác minh thanh toán với PayOS SDK: {transaction_id}")
            payment_info = payos_client.getPaymentLinkInformation(orderId=transaction_id)
            logger.info(f"Thông tin thanh toán: {payment_info.to_json() if hasattr(payment_info, 'to_json') else payment_info}")
            
            # Cập nhật trạng thái giao dịch dựa trên thông tin từ PayOS
            payment_status = payment_info.status
            
            if payment_status == "PAID":
                # Cập nhật trạng thái giao dịch thành công
                transaction.status = "completed"
                transaction.completed_at = datetime.now().isoformat()
                
                # Cộng credits cho người dùng
                user = db.query(User).filter(User.id == transaction.user_id).first()
                if user:
                    user.credits += transaction.credits
                    logger.info(f"Đã cộng {transaction.credits} credits cho người dùng {user.id}")
                
                db.commit()
                return True
            
            elif payment_status in ["CANCELLED", "EXPIRED"]:
                # Cập nhật trạng thái giao dịch thất bại
                transaction.status = "failed"
                db.commit()
            
            return False
            
        except Exception as e:
            logger.error(f"Lỗi khi xác minh thanh toán: {str(e)}")
            raise ValueError(f"Lỗi khi xác minh thanh toán: {str(e)}")
    
    @staticmethod
    def process_webhook(db: Session, webhook_data: dict) -> bool:
        """
        Xử lý dữ liệu webhook từ PayOS
        """
        try:
            # Xác minh tính hợp lệ của dữ liệu webhook
            verified_data = payos_client.verifyPaymentWebhookData(webhook_data)
            logger.info(f"Dữ liệu webhook đã xác minh: {verified_data.to_json() if hasattr(verified_data, 'to_json') else verified_data}")
            
            # Lấy mã giao dịch từ dữ liệu đã xác minh
            payment_link_id = verified_data.paymentLinkId
            
            # Tìm giao dịch trong cơ sở dữ liệu
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.transaction_id == payment_link_id
            ).first()
            
            if not transaction:
                logger.warning(f"Không tìm thấy giao dịch với ID: {payment_link_id}")
                return False
            
            # Kiểm tra nếu giao dịch đã hoàn thành thì bỏ qua
            if transaction.status == "completed":
                logger.info(f"Giao dịch {payment_link_id} đã được xử lý trước đó")
                return True
            
            # Cập nhật trạng thái giao dịch
            if verified_data.code == "00":  # Thanh toán thành công
                transaction.status = "completed"
                transaction.completed_at = datetime.now().isoformat()
                
                # Cộng credits cho người dùng
                user = db.query(User).filter(User.id == transaction.user_id).first()
                if user:
                    user.credits += transaction.credits
                    logger.info(f"Đã cộng {transaction.credits} credits cho người dùng {user.username}")
                
                db.commit()
                return True
            else:
                logger.warning(f"Webhook báo trạng thái không thành công: {verified_data.code} - {verified_data.desc}")
                return False
                
        except Exception as e:
            logger.error(f"Lỗi khi xử lý webhook: {str(e)}")
            return False
    
    @staticmethod
    def get_all_payment_transactions(db: Session, skip: int = 0, limit: int = 100):
        """
        Lấy tất cả các giao dịch thanh toán
        """
        return db.query(PaymentTransaction).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_payment_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """
        Lấy các giao dịch thanh toán của một người dùng cụ thể
        """
        return db.query(PaymentTransaction).filter(PaymentTransaction.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_payment_transactions_count(db: Session) -> int:
        """
        Lấy tổng số giao dịch thanh toán
        """
        return db.query(PaymentTransaction).count()
    
    @staticmethod
    def get_user_payment_transactions_count(db: Session, user_id: int) -> int:
        """
        Lấy tổng số giao dịch thanh toán của một người dùng cụ thể
        """
        return db.query(PaymentTransaction).filter(PaymentTransaction.user_id == user_id).count()
    
    @staticmethod
    def get_payment_statistics(db: Session):
        """
        Lấy thống kê tổng quan về các giao dịch thanh toán
        """
        # Tổng số giao dịch
        total_transactions = db.query(PaymentTransaction).count()
        
        # Tổng số giao dịch thành công
        completed_transactions = db.query(PaymentTransaction).filter(
            PaymentTransaction.status == "completed"
        ).count()
        
        # Tổng số giao dịch đang xử lý
        pending_transactions = db.query(PaymentTransaction).filter(
            PaymentTransaction.status == "pending"
        ).count()
        
        # Tổng số giao dịch thất bại
        failed_transactions = db.query(PaymentTransaction).filter(
            PaymentTransaction.status == "failed"
        ).count()
        
        # Tổng số tiền đã thanh toán thành công
        total_amount = db.query(func.sum(PaymentTransaction.amount)).filter(
            PaymentTransaction.status == "completed"
        ).scalar() or 0
        
        # Tổng số credits đã mua thành công
        total_credits = db.query(func.sum(PaymentTransaction.credits)).filter(
            PaymentTransaction.status == "completed"
        ).scalar() or 0
        
        return {
            "total_transactions": total_transactions,
            "completed_transactions": completed_transactions,
            "pending_transactions": pending_transactions,
            "failed_transactions": failed_transactions,
            "total_amount": total_amount,
            "total_credits": total_credits
        }