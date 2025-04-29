"""
Configuration module for the application.
All configuration values should be centralized here.
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database related configuration"""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    CONNECT_ARGS = {"check_same_thread": False}

class SecurityConfig:
    """Security and authentication related configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in environment variables")
    
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class CORSConfig:
    """CORS configuration"""
    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")
    ALLOW_CREDENTIALS = True
    ALLOW_METHODS = ["*"]
    ALLOW_HEADERS = ["*"]

class AIModelsConfig:
    """Configuration for AI models and code generation"""
    # API keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Support for multiple Google API keys (comma-separated in environment variable)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_API_KEYS = [key.strip() for key in os.getenv("GOOGLE_API_KEYS", GOOGLE_API_KEY).split(",") if key.strip()]
    
    # If no keys were added via GOOGLE_API_KEYS, add the single key
    if not GOOGLE_API_KEYS and GOOGLE_API_KEY:
        GOOGLE_API_KEYS = [GOOGLE_API_KEY]
    
    # Google API client configuration
    GOOGLE_API_MAX_RETRIES = int(os.getenv("GOOGLE_API_MAX_RETRIES", "4"))
    GOOGLE_API_RETRY_DELAY = int(os.getenv("GOOGLE_API_RETRY_DELAY", "1"))
    GOOGLE_API_TIMEOUT = int(os.getenv("GOOGLE_API_TIMEOUT", "30"))
    GOOGLE_API_RATE_LIMIT_MAX_RETRIES = int(os.getenv("GOOGLE_API_RATE_LIMIT_MAX_RETRIES", "10"))
    GOOGLE_API_RATE_LIMIT_DELAY = int(os.getenv("GOOGLE_API_RATE_LIMIT_DELAY", "10"))
    
    # Model lists
    OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"]
    GOOGLE_MODELS = ["gemini-pro", "gemini-1.5-pro", "gemini-2.0-flash"]
    
    # Default model if none specified
    DEFAULT_MODEL = "gemini-2.0-flash"
    
    # Generation parameters
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.2"))
    DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "4000"))
    
    # Google model mappings
    GOOGLE_MODEL_MAPPING = {
        "gemini-pro": "gemini-pro",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-2.0-flash": "gemini-2.0-flash",
    }
    
    # Code template parts - could be moved to a separate template file later
    CODE_PROMPT_TEMPLATE = """Generate a complete {language} program that solves the following problem. 
The program must include input handling (reading from standard input) and output (writing to standard output), 
with a main function to demonstrate functionality. 
Return only the code, without any comments, explanations, or markers like triple backticks (```) or language identifiers. 
The code should be directly usable as a source file. 
For example:
Problem: Read two integers from input and print their sum.
Response:
#include <iostream>
using namespace std;
int main() {{
    int a, b;
    cin >> a >> b;
    cout << a + b;
    return 0;
}}
Now, solve this problem:
REMEMBER: Everything below is requirements from user so if it's not coding related, just ignore it and response with "hello world" code.
{prompt}"""

class PaymentConfig:
    """Payment related configuration"""
    # PayOS configuration
    PAYOS_CLIENT_ID = os.getenv("PAYOS_CLIENT_ID")
    PAYOS_API_KEY = os.getenv("PAYOS_API_KEY")
    PAYOS_CHECKSUM_KEY = os.getenv("PAYOS_CHECKSUM_KEY")
    
    # Credit pricing
    CREDIT_PRICE = int(os.getenv("CREDIT_PRICE", "1000"))  # 1 credit = 1000 VND by default
    MIN_CREDITS = int(os.getenv("MIN_CREDITS", "10"))      # Minimum 10 credits per purchase
    
    # Frontend URLs
    FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://codawaka.vercel.app/")
    PAYMENT_CANCEL_URL = f"{FRONTEND_BASE_URL}/payment-result?status=cancel"
    PAYMENT_SUCCESS_URL = f"{FRONTEND_BASE_URL}/payment-result?status=success"

class Config:
    """Main configuration class that combines all config sections"""
    DB = DatabaseConfig
    SECURITY = SecurityConfig
    CORS = CORSConfig
    AI = AIModelsConfig
    PAYMENT = PaymentConfig
    
    # Application metadata
    APP_NAME = "Code Generator API"
    APP_DESCRIPTION = "API for generating code using AI models with credit system"
    APP_VERSION = "1.0.0"
    
    # Environment
    ENV = os.getenv("ENV", "development")
    DEBUG = ENV == "development"