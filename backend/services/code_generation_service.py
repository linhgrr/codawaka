from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
import json
import requests
import threading

from models import User, ModelPricing, CodeGeneration
from config import Config
from repositories.user_repository import UserRepository
from repositories.model_repository import ModelPricingRepository
from repositories.code_repository import CodeGenerationRepository
from services.api_clients.google_client import GoogleApiClient
from services.api_clients.openai_client import OpenAIApiClient
from core.dependency_injection import DIContainer

# Google API key management
class GoogleAPIKeyManager:
    """
    Manages Google API keys using a round-robin approach to respect rate limits.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GoogleAPIKeyManager, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        """Initialize the key manager with keys from config"""
        self.api_keys = Config.AI.GOOGLE_API_KEYS
        self.current_key_index = 0
        self.request_counts = {key: 0 for key in self.api_keys}
        self.max_requests_per_key = Config.AI.GOOGLE_API_REQUESTS_PER_KEY
        
        # Keys must be set before using the manager
        if not self.api_keys:
            raise ValueError("No Google API keys available. Set GOOGLE_API_KEYS in your .env file.")
    
    def get_current_key(self) -> str:
        """Get the current API key"""
        with self._lock:
            if not self.api_keys:
                raise ValueError("No Google API keys available")
            return self.api_keys[self.current_key_index]
    
    def increment_request_count(self) -> None:
        """Increment the request count for the current key and rotate if needed"""
        with self._lock:
            current_key = self.api_keys[self.current_key_index]
            self.request_counts[current_key] += 1
            
            # Check if we need to rotate to the next key
            if self.request_counts[current_key] >= self.max_requests_per_key:
                self.rotate_key()
    
    def rotate_key(self) -> None:
        """Rotate to the next API key in the list"""
        with self._lock:
            # Reset current key's count if we've gone through all keys
            if all(count >= self.max_requests_per_key for count in self.request_counts.values()):
                self.request_counts = {key: 0 for key in self.api_keys}
            
            # Move to next key
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            next_key = self.api_keys[self.current_key_index]
            
            print(f"Rotated to next Google API key (key index: {self.current_key_index})")

# Initialize and register key manager in DI container
google_key_manager = GoogleAPIKeyManager()
DIContainer.register_instance(GoogleAPIKeyManager, google_key_manager)

# Get API clients through DI container
google_client = DIContainer.get_instance(GoogleApiClient, google_key_manager)
openai_client = DIContainer.get_instance(OpenAIApiClient, Config.AI.OPENAI_API_KEY)

class DirectAPICodeGenerator:
    """
    Implementation that directly calls OpenAI and Google APIs for code generation
    using the API clients.
    """
    
    @staticmethod
    def format_prompt(prompt: str, language: str = "C++") -> str:
        """Format the prompt with language specification, defaulting to C++"""
        if language is None:
            language = "C++"
        return Config.AI.CODE_PROMPT_TEMPLATE.format(language=language, prompt=prompt)
       
    @classmethod
    def generate_code_with_openai(cls, model_name: str, prompt: str, language: Optional[str] = None) -> Optional[str]:
        """
        Generate code using OpenAI API directly.
        
        Args:
            model_name: The specific OpenAI model to use
            prompt: The code generation prompt
            language: Optional programming language preference
            
        Returns:
            Optional[str]: The generated code or None if generation failed
        """
        try:
            formatted_prompt = cls.format_prompt(prompt, language)
            
            print(f"Formatted Prompt: {formatted_prompt}")  # Debugging line to check the formatted prompt
            
            system_prompt = "You are a code generation assistant. Provide only the code without comments, explanations, or markdown formatting."
            
            # Use the OpenAI client to generate code
            return openai_client.generate_code(
                model_name=model_name,
                system_prompt=system_prompt,
                user_prompt=formatted_prompt,
                temperature=Config.AI.DEFAULT_TEMPERATURE,
                max_tokens=Config.AI.DEFAULT_MAX_TOKENS
            )
        except Exception as e:
            print(f"Error generating code with OpenAI: {str(e)}")
            return None
    
    @classmethod
    async def generate_code_with_openai_async(cls, model_name: str, prompt: str, language: Optional[str] = None) -> Optional[str]:
        """
        Generate code using OpenAI API asynchronously.
        
        Args:
            model_name: The specific OpenAI model to use
            prompt: The code generation prompt
            language: Optional programming language preference
            
        Returns:
            Optional[str]: The generated code or None if generation failed
        """
        try:
            formatted_prompt = cls.format_prompt(prompt, language)
            
            print(f"Async Formatted Prompt: {formatted_prompt}")
            
            system_prompt = "You are a code generation assistant. Provide only the code without comments, explanations, or markdown formatting."
            
            # Use the OpenAI client to generate code asynchronously
            return await openai_client.generate_code_async(
                model_name=model_name,
                system_prompt=system_prompt,
                user_prompt=formatted_prompt,
                temperature=Config.AI.DEFAULT_TEMPERATURE,
                max_tokens=Config.AI.DEFAULT_MAX_TOKENS
            )
        except Exception as e:
            print(f"Error generating code with OpenAI async: {str(e)}")
            return None
    
    @classmethod
    def generate_code_with_google(cls, model_name: str, prompt: str, language: Optional[str] = None) -> Optional[str]:
        """
        Generate code using Google's Generative AI API directly.
        
        Args:
            model_name: The specific Google model to use
            prompt: The code generation prompt
            language: Optional programming language preference
            
        Returns:
            Optional[str]: The generated code or None if generation failed
        """
        try:
            formatted_prompt = cls.format_prompt(prompt, language)
            
            # Use the mapped model name or default to gemini-pro
            actual_model = Config.AI.GOOGLE_MODEL_MAPPING.get(model_name, "gemini-pro")
            
            # Use the Google client to generate content
            messages = [
                "You are a code generation assistant. Provide only the code without comments, explanations, or markdown formatting.",
                formatted_prompt
            ]
            
            raw_response = google_client.generate_content(actual_model, messages)
            
            if raw_response:
                # Clean up the response
                return google_client.clean_code_response(raw_response)
            return None
        except Exception as e:
            print(f"Error generating code with Google: {str(e)}")
            return None
    
    @classmethod
    def generate_code(cls, model_name: str, prompt: str, language: Optional[str] = None) -> Optional[str]:
        """
        Generate code using either OpenAI or Google API based on the model name.
        
        Args:
            model_name: The name of the model to use for code generation
            prompt: The prompt describing the code to generate
            language: Optional programming language preference
            
        Returns:
            Optional[str]: The generated code or None if generation failed
        """
        try:
            # Route to the appropriate API based on the model name
            if model_name.lower() in [m.lower() for m in Config.AI.OPENAI_MODELS]:
                return cls.generate_code_with_openai(model_name, prompt, language)
            elif model_name.lower() in [m.lower() for m in Config.AI.GOOGLE_MODELS]:
                return cls.generate_code_with_google(model_name, prompt, language)
            else:
                # Default to OpenAI for unrecognized models
                print(f"Unrecognized model '{model_name}', defaulting to {Config.AI.DEFAULT_MODEL}")
                return cls.generate_code_with_openai(Config.AI.DEFAULT_MODEL, prompt, language)
        except Exception as e:
            print(f"Error in generate_code: {str(e)}")
            return None
    
    @classmethod
    async def generate_code_async(cls, model_name: str, prompt: str, language: Optional[str] = None) -> Optional[str]:
        """
        Generate code asynchronously using either OpenAI or Google API based on the model name.
        
        Args:
            model_name: The name of the model to use for code generation
            prompt: The prompt describing the code to generate
            language: Optional programming language preference
            
        Returns:
            Optional[str]: The generated code or None if generation failed
        """
        try:
            # Route to the appropriate API based on the model name
            if model_name.lower() in [m.lower() for m in Config.AI.OPENAI_MODELS]:
                return await cls.generate_code_with_openai_async(model_name, prompt, language)
            elif model_name.lower() in [m.lower() for m in Config.AI.GOOGLE_MODELS]:
                # Google doesn't have an async API yet, so call it synchronously
                # For production, you might want to run this in a thread pool
                return cls.generate_code_with_google(model_name, prompt, language)
            else:
                # Default to OpenAI for unrecognized models
                print(f"Unrecognized model '{model_name}', defaulting to {Config.AI.DEFAULT_MODEL}")
                return await cls.generate_code_with_openai_async(Config.AI.DEFAULT_MODEL, prompt, language)
        except Exception as e:
            print(f"Error in generate_code_async: {str(e)}")
            return None


class CodeGenerationService:
    """
    Service for handling code generation requests and related operations.
    Uses repositories for data access and API clients for external services.
    """
    
    def __init__(self, 
                 user_repository: UserRepository,
                 model_repository: ModelPricingRepository,
                 code_repository: CodeGenerationRepository):
        """
        Initialize with repositories.
        
        Args:
            user_repository: Repository for user operations
            model_repository: Repository for model pricing operations
            code_repository: Repository for code generation operations
        """
        self.user_repository = user_repository
        self.model_repository = model_repository
        self.code_repository = code_repository
    
    @staticmethod
    def get_instance(db: Session):
        """
        Get an instance of the service with properly initialized repositories.
        
        Args:
            db: Database session
            
        Returns:
            CodeGenerationService instance
        """
        user_repo = UserRepository(db)
        model_repo = ModelPricingRepository(db)
        code_repo = CodeGenerationRepository(db)
        
        return CodeGenerationService(user_repo, model_repo, code_repo)
    
    def process_generation_request(
        self, 
        user_id: int, 
        model_name: str, 
        prompt: str,
        language: Optional[str] = None
    ) -> Optional[CodeGeneration]:
        """
        Process a code generation request, check credits, and record the transaction.
        
        Args:
            user_id: ID of the user making the request
            model_name: Name of the model to use
            prompt: The code generation prompt
            language: Optional programming language preference
            
        Returns:
            Optional[CodeGeneration]: The code generation record or None if failed
        """
        # Get the user
        user = self.user_repository.get(user_id)
        if not user:
            return None
        
        # Get the model pricing
        model_pricing = self.model_repository.get_by_model_name(model_name)
        
        # If model doesn't exist in the pricing table, return None
        if not model_pricing:
            return None
        
        # Check if user has enough credits
        if user.credits < model_pricing.credit_cost_per_request:
            return None
        
        # Generate code using direct API calls
        generated_code = DirectAPICodeGenerator.generate_code(model_name, prompt, language)
        
        # If code generation failed, return None
        if generated_code is None:
            return None
        
        # Deduct credits from user
        self.user_repository.update_credits(user_id, -model_pricing.credit_cost_per_request)
        
        # Create code generation record
        code_gen = self.code_repository.create_generation(
            user_id=user_id,
            model_name=model_name,
            prompt=prompt,
            generated_code=generated_code,
            credits_used=model_pricing.credit_cost_per_request
        )
        
        return code_gen
    
    async def process_generation_request_async(
        self, 
        user_id: int, 
        model_name: str, 
        prompt: str,
        language: Optional[str] = None
    ) -> Optional[CodeGeneration]:
        """
        Process a code generation request asynchronously.
        
        Args:
            user_id: ID of the user making the request
            model_name: Name of the model to use
            prompt: The code generation prompt
            language: Optional programming language preference
            
        Returns:
            Optional[CodeGeneration]: The code generation record or None if failed
        """
        # Get the user
        user = self.user_repository.get(user_id)
        if not user:
            return None
        
        # Get the model pricing
        model_pricing = self.model_repository.get_by_model_name(model_name)
        
        # If model doesn't exist in the pricing table, return None
        if not model_pricing:
            return None
        
        # Check if user has enough credits
        if user.credits < model_pricing.credit_cost_per_request:
            return None
        
        # Generate code using direct API calls asynchronously
        generated_code = await DirectAPICodeGenerator.generate_code_async(model_name, prompt, language)
        
        # If code generation failed, return None
        if generated_code is None:
            return None
        
        # Deduct credits from user
        self.user_repository.update_credits(user_id, -model_pricing.credit_cost_per_request)
        
        # Create code generation record
        code_gen = self.code_repository.create_generation(
            user_id=user_id,
            model_name=model_name,
            prompt=prompt,
            generated_code=generated_code,
            credits_used=model_pricing.credit_cost_per_request
        )
        
        return code_gen