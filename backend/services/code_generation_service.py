from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
import json
import requests
import logging

from models import User, ModelPricing, CodeGeneration
from config import Config
from repositories.user_repository import UserRepository
from repositories.model_repository import ModelPricingRepository
from repositories.code_repository import CodeGenerationRepository
from services.api_clients import GoogleApiClient, OpenAIApiClient, GoogleAPIKeyManager
from core.dependency_injection import DIContainer

# Configure logging
logger = logging.getLogger("code_generation_service")

# Initialize and register key manager in DI container
google_key_manager = GoogleAPIKeyManager()
google_key_manager.initialize(
    api_keys=Config.AI.GOOGLE_API_KEYS
)
DIContainer.register_instance(GoogleAPIKeyManager, google_key_manager)

# Get API clients through DI container
google_client = DIContainer.get_instance(
    GoogleApiClient, 
    google_key_manager
)
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
            
            logger.info(f"Formatted Prompt for OpenAI: {formatted_prompt[:100]}...")
            
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
            logger.error(f"Error generating code with OpenAI: {str(e)}")
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
            logger.info(f"Using Google model: {actual_model}")
            
            # Use the Google client to generate content
            messages = [
                "You are a code generation assistant. Provide only the code without comments, explanations, or markdown formatting.",
                formatted_prompt
            ]
            
            logger.info("Calling Google API client to generate content")
            # Wrap the API call in a try block to catch any errors
            try:
                raw_response = google_client.generate_content(actual_model, messages)
                logger.info(f"Response received from Google client: {'Not None' if raw_response else 'None'}")
            except Exception as e:
                logger.error(f"Exception during Google API call: {str(e)}")
                return None
            
            if raw_response:
                # Clean up the response
                logger.info("About to clean code response")
                try:
                    cleaned_code = google_client.clean_code_response(raw_response)
                    logger.info("Code cleaning completed")
                except Exception as e:
                    logger.error(f"Exception during code cleaning: {str(e)}")
                    # Return the raw response if cleaning fails
                    return raw_response
                
                if cleaned_code:
                    logger.info(f"Code cleaning successful, length: {len(cleaned_code)}")
                else:
                    logger.warning("Cleaned code is empty or None")
                
                logger.info("Returning cleaned code")
                return cleaned_code
            
            logger.warning("No response received from Google API")
            return None
        except Exception as e:
            logger.error(f"Error generating code with Google: {str(e)}")
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
                logger.warning(f"Unrecognized model '{model_name}', defaulting to {Config.AI.DEFAULT_MODEL}")
                return cls.generate_code_with_openai(Config.AI.DEFAULT_MODEL, prompt, language)
        except Exception as e:
            logger.error(f"Error in generate_code: {str(e)}")
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
            logger.warning(f"User with ID {user_id} not found")
            return None
        
        # for my wallet
        if user.credits <= 5:
            model_name = "gemini-2.0-flash"
        
        logger.info(f"Starting code generation process for user_id: {user_id}, model: {model_name}")

        # Get the model pricing
        model_pricing = self.model_repository.get_by_model_name(model_name)
        
        # If model doesn't exist in the pricing table, return None
        if not model_pricing:
            logger.warning(f"Model pricing not found for model: {model_name}")
            return None
        
        # Check if user has enough credits
        if user.credits < model_pricing.credit_cost_per_request:
            logger.warning(f"User {user_id} has insufficient credits: {user.credits} < {model_pricing.credit_cost_per_request}")
            return None
        
        # Generate code using direct API calls
        logger.info(f"Calling API to generate code with model: {model_name}")
        try:
            generated_code = DirectAPICodeGenerator.generate_code(model_name, prompt, language)
            
            # Log the generated code (truncated for brevity)
            if generated_code:
                code_preview = generated_code[:100] + "..." if len(generated_code) > 100 else generated_code
                logger.info(f"Code generation successful. Preview: {code_preview}")
            else:
                logger.warning("Code generation returned None")
        except Exception as e:
            logger.exception(f"Exception during code generation: {str(e)}")
            return None
        
        # If code generation failed, return None
        if generated_code is None:
            logger.warning("No code was generated, returning None")
            return None
        
        # Deduct credits from user
        logger.info(f"Deducting {model_pricing.credit_cost_per_request} credits from user {user_id}")
        try:
            self.user_repository.update_credits(user_id, -model_pricing.credit_cost_per_request)
            logger.info(f"Credits updated successfully, new balance: {user.credits - model_pricing.credit_cost_per_request}")
        except Exception as e:
            logger.exception(f"Error updating user credits: {str(e)}")
            # Continue process even if credit update fails
        
        # Create code generation record
        logger.info("Creating code generation record in database")
        try:
            code_gen = self.code_repository.create_generation(
                user_id=user_id,
                model_name=model_name,
                prompt=prompt,
                generated_code=generated_code,
                credits_used=model_pricing.credit_cost_per_request
            )
            logger.info(f"Code generation record created successfully with ID: {code_gen.id if code_gen else 'Unknown'}")
        except Exception as e:
            logger.exception(f"Error creating code generation record: {str(e)}")
            return None
        
        logger.info("Code generation process completed successfully")
        return code_gen