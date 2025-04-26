"""
Base repository with common database operations.
"""
from typing import TypeVar, Generic, Type, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import Base

T = TypeVar('T', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class BaseRepository(Generic[T, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository for database operations with standard CRUD methods.
    """
    
    def __init__(self, model: Type[T], db: Session):
        """
        Initialize with model class and database session.
        
        Args:
            model: The SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get(self, id: Any) -> Optional[T]:
        """
        Get entity by ID.
        
        Args:
            id: Entity ID
            
        Returns:
            Entity or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get multiple entities with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of entities
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, *, obj_in: CreateSchemaType) -> T:
        """
        Create a new entity.
        
        Args:
            obj_in: Schema with data to create entity
            
        Returns:
            Created entity
        """
        obj_data = obj_in.dict()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, *, db_obj: T, obj_in: UpdateSchemaType) -> T:
        """
        Update an entity.
        
        Args:
            db_obj: Database entity to update
            obj_in: Schema with data to update
            
        Returns:
            Updated entity
        """
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, *, id: Any) -> T:
        """
        Delete an entity.
        
        Args:
            id: Entity ID
            
        Returns:
            Deleted entity
        """
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        self.db.delete(obj)
        self.db.commit()
        return obj
    
    def count(self) -> int:
        """
        Count total entities.
        
        Returns:
            Total count of entities
        """
        return self.db.query(self.model).count()