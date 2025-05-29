from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import json
import requests
import openai
import google.generativeai as genai

from models import User, ModelPricing, CodeGeneration
from config import Config

# Configure APIs with keys from config
openai.api_key = Config.AI.OPENAI_API_KEY
genai.configure(api_key=Config.AI.GOOGLE_API_KEY)

class DirectAPICodeGenerator:
    """
    Implementation that directly calls OpenAI and Google APIs for code generation
    without using agent architecture.
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
            # Create the API call to OpenAI
            response = openai.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a code generation assistant. Provide only the code without comments, explanations, or markdown formatting."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=Config.AI.DEFAULT_TEMPERATURE,
                max_tokens=Config.AI.DEFAULT_MAX_TOKENS,
            )
            
            # Extract the generated code from the response
            if response and response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            return None
        except Exception as e:
            print(f"Error generating code with OpenAI: {str(e)}")
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
            
            # Initialize the model
            model = genai.GenerativeModel(actual_model)
            
            # Generate content
            response = model.generate_content(
                [
                    "You are a code generation assistant. Provide only the code without comments, explanations, or markdown formatting.",
                    formatted_prompt
                ]
            )
            
            # Extract the text response
            if response and response.text:
                # Remove any markdown code block formatting if present
                code = response.text.strip()
                if code.startswith("```") and code.endswith("```"):
                    # Extract the content between the code blocks
                    lines = code.split("\n")
                    if len(lines) > 2:
                        # Check if the first line contains language specification
                        if "```" in lines[0] and len(lines[0]) > 3:
                            code = "\n".join(lines[1:-1])
                        else:
                            code = "\n".join(lines[1:-1])
                return code
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


class CodeGenerationService:
    """
    Service for handling code generation requests and related operations.
    """
    
    @staticmethod
    def process_generation_request(
        db: Session, 
        user_id: int, 
        model_name: str, 
        prompt: str,
        language: Optional[str] = None
    ) -> Optional[CodeGeneration]:
        """
        Process a code generation request, check credits, and record the transaction.
        
        Args:
            db: Database session
            user_id: ID of the user making the request
            model_name: Name of the model to use
            prompt: The code generation prompt
            language: Optional programming language preference
            
        Returns:
            Optional[CodeGeneration]: The code generation record or None if failed
        """
        # Get the user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Get the model pricing
        model_pricing = db.query(ModelPricing).filter(
            ModelPricing.model_name == model_name
        ).first()
        
        # If model doesn't exist in the pricing table, return None
        if not model_pricing:
            return None
        
        # Check if user has enough credits
        if user.credits < model_pricing.credit_cost_per_request:
            return None
        
        # Generate code using direct API calls instead of agents
        generated_code = DirectAPICodeGenerator.generate_code(model_name, prompt, language)
        
        # If code generation failed, return None
        if generated_code is None:
            return None
        
        # Deduct credits from user
        user.credits -= model_pricing.credit_cost_per_request
        
        # Create code generation record
        code_gen = CodeGeneration(
            user_id=user_id,
            model_name=model_name,
            prompt=prompt,
            generated_code=generated_code,
            credits_used=model_pricing.credit_cost_per_request,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Add and commit to the database
        db.add(code_gen)
        db.commit()
        db.refresh(code_gen)
        
        return code_gen