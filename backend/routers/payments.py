from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import PaymentCreate, PaymentResponse, PaymentTransaction as PaymentTransactionSchema, PaymentVerify
from models import PaymentTransaction
from core.security import get_current_user, get_user_id_from_token
from services.payment_service import PaymentService

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)


@router.post("/create", response_model=PaymentResponse)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_token)
):
    """
    Tạo giao dịch thanh toán để mua credits
    """
    try:
        # Xác thực số lượng credit (tối thiểu 10)
        if payment.credits < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Số lượng tối thiểu là 10 credits"
            )
        
        # Tạo giao dịch thanh toán qua PaymentService
        result = PaymentService.create_payment(db, current_user_id, payment.credits)
        return result
    except ValueError as e:
        # Xử lý lỗi xác thực và thiếu cấu hình
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log lỗi để debug
        import logging
        logging.error(f"Lỗi khi tạo thanh toán: {str(e)}")
        
        # Trả về thông báo lỗi chi tiết hơn
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo thanh toán: {str(e)}"
        )


@router.get("/verify/{transaction_id}", response_model=bool)
def verify_payment(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_token)
):
    """
    Xác minh trạng thái thanh toán với PayOS và cập nhật credits nếu thanh toán thành công
    """
    try:
        result = PaymentService.verify_payment(db, transaction_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi xác minh thanh toán: {str(e)}"
        )


@router.get("/history", response_model=List[PaymentTransactionSchema])
def get_payment_history(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_token)
):
    """
    Lấy lịch sử thanh toán của người dùng hiện tại
    """
    transactions = db.query(PaymentTransaction).filter(
        PaymentTransaction.user_id == current_user_id
    ).all()
    
    return transactions


@router.post("/webhook")
async def payment_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint nhận các thông báo webhook từ PayOS khi có cập nhật trạng thái thanh toán
    """
    try:
        # Đọc dữ liệu webhook từ body request
        webhook_data = await request.json()
        
        # Xử lý dữ liệu webhook
        result = PaymentService.process_webhook(db, webhook_data)
        
        if result:
            return {"status": "success", "message": "Webhook processed successfully"}
        else:
            return {"status": "error", "message": "Failed to process webhook"}
    except Exception as e:
        import logging
        logging.error(f"Lỗi khi xử lý webhook: {str(e)}")
        return {"status": "error", "message": f"Error processing webhook: {str(e)}"}