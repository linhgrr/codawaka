from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import CodeGenerationCreate, CodeGeneration, CodeGenerationByUsername
from core.security import get_current_active_user
from services.code_generation_service import CodeGenerationService
from services.code_history_service import CodeHistoryService
from typing import List

router = APIRouter(
    prefix="/code",
    tags=["code generation"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate-code", response_model=CodeGeneration)
def generate_code(
    code_request: CodeGenerationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate code based on a prompt using the specified model"""
    code_gen = CodeGenerationService.process_generation_request(
        db=db,
        user_id=current_user.id,
        model_name=code_request.model_name,
        prompt=code_request.prompt,
        language=code_request.language
    )
    
    if code_gen is None:
        raise HTTPException(
            status_code=400,
            detail="Code generation failed. Please check your credits and model name."
        )
    
    return code_gen


@router.post("/completion")
def generate_code_by_username(
    code_request: CodeGenerationByUsername,
    db: Session = Depends(get_db)
):
    """Generate code based on a prompt using the specified model and username for authentication"""
    # Lấy thông tin user dựa trên username
    user = db.query(User).filter(User.username == code_request.username).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    code_gen = CodeGenerationService.process_generation_request(
        db=db,
        user_id=user.id,
        model_name=code_request.model_name,
        prompt=code_request.prompt,
        language=code_request.language
    )
    
    if code_gen is None:
        raise HTTPException(
            status_code=400,
            detail="Code generation failed. Please check your credits and model name."
        )
    
    return code_gen.generated_code


@router.get("/history", response_model=List[CodeGeneration])
def get_code_generation_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the code generation history for the current user with pagination"""
    return CodeHistoryService.get_user_code_history(db, current_user.id, skip, limit)


@router.get("/history/count", response_model=dict)
def get_code_generation_history_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the total count of code generation history items for the current user"""
    count = CodeHistoryService.get_user_code_history_count(db, current_user.id)
    return {"count": count}