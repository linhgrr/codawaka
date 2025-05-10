from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import CodeGenerationCreate, CodeGeneration, CodeGenerationByUsername
from core.security import get_current_active_user
from services.code_generation_service import CodeGenerationService
from services.code_history_service import CodeHistoryService
from repositories.user_repository import UserRepository
from repositories.code_repository import CodeGenerationRepository
from core.dependency_injection import DIContainer
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
    # Get service instance using DI
    code_gen_service = CodeGenerationService.get_instance(db)
    
    code_gen = code_gen_service.process_generation_request(
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


@router.post("/generate-code-async", response_model=CodeGeneration)
async def generate_code_async(
    code_request: CodeGenerationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate code asynchronously based on a prompt using the specified model"""
    # Get service instance using DI
    code_gen_service = CodeGenerationService.get_instance(db)
    
    code_gen = await code_gen_service.process_generation_request_async(
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
    # Initialize repositories
    user_repository = UserRepository(db)
    
    # Get user by username
    user = user_repository.get_by_username(code_request.username)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    # Get service instance using DI
    code_gen_service = CodeGenerationService.get_instance(db)
    
    code_gen = code_gen_service.process_generation_request(
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
    # Initialize repository
    code_repository = CodeGenerationRepository(db)
    return code_repository.get_by_user_id(current_user.id, skip, limit)


@router.get("/history/count", response_model=dict)
def get_code_generation_history_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the total count of code generation history items for the current user"""
    # Initialize repository
    code_repository = CodeGenerationRepository(db)
    count = code_repository.count_by_user_id(current_user.id)
    return {"count": count}