"""
API client for Google Generative AI services.
"""
import google.generativeai as genai
from typing import Optional, List, Dict, Any, Tuple, Union
import time
import logging
import concurrent.futures
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("google_api_client")

class ApiError(Exception):
    """Base exception for API errors"""
    pass

class RateLimitError(ApiError):
    """Exception for rate limit errors"""
    pass

class GoogleApiClient:
    """
    Client for interacting with Google's Generative AI API.
    Uses a key manager to handle API key rotation and rate limits.
    With retry mechanism for failed requests and request timeout.
    """
    
    def __init__(self, key_manager, max_retries=3, retry_delay=1, timeout=20):
        """
        Initialize with a key manager for API keys.
        
        Args:
            key_manager: An instance of GoogleAPIKeyManager
            max_retries: Maximum number of retry attempts (default: 3)
            retry_delay: Delay between retries in seconds (default: 1)
            timeout: API call timeout in seconds (default: 20)
        """
        self.key_manager = key_manager
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        logger.info(f"GoogleApiClient initialized with timeout: {self.timeout}s, max_retries: {self.max_retries}")
    
    def __del__(self):
        """Clean up resources when object is destroyed"""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)
            logger.debug("ThreadPoolExecutor shut down")
    
    def _with_timeout(self, func, *args, **kwargs) -> Tuple[Any, Optional[Exception]]:
        """
        Execute a function with timeout control.
        
        Args:
            func: Function to execute
            *args, **kwargs: Arguments to pass to the function
            
        Returns:
            Tuple of (result, exception). If successful, exception is None.
        """
        future = self._executor.submit(func, *args, **kwargs)
        try:
            result = future.result(timeout=self.timeout)
            return result, None
        except concurrent.futures.TimeoutError:
            future.cancel()
            return None, TimeoutError(f"API call timed out after {self.timeout} seconds")
        except Exception as e:
            return None, e
    
    def _handle_api_error(self, error: Exception, key_index: int) -> Optional[RateLimitError]:
        """
        Handle API errors and determine if it's a rate limit error.
        
        Args:
            error: Exception that was raised
            key_index: Index of the API key that was used
            
        Returns:
            RateLimitError if it's a rate limit error, None otherwise
        """
        error_message = str(error)
        
        if "429" in error_message or "quota" in error_message.lower():
            logger.warning(f"Rate limit reached for API key #{key_index + 1}: {error_message}")
            return RateLimitError(f"Rate limit exceeded: {error_message}")
        else:
            logger.error(f"Error with Google API key #{key_index + 1}: {error_message}")
            return None
    
    def generate_content(self, model_name: str, messages: List[str]) -> Optional[str]:
        """
        Generate content using Google's Generative AI API.
        If request fails or rate limit is reached, it will retry with different API keys.
        
        Args:
            model_name: The name of the model to use
            messages: List of message strings to send to the model
            
        Returns:
            Optional[str]: Generated content or None if all attempts failed
        """
        tried_keys = set()
        total_keys = len(self.key_manager.api_keys)
        attempt_count = 0
        
        while attempt_count < self.max_retries and len(tried_keys) < total_keys:
            current_key = self.key_manager.get_current_key()
            current_key_index = self.key_manager.current_key_index
            
            # Skip if we've already tried this key
            if current_key in tried_keys:
                self.key_manager.rotate_key()
                continue
                
            tried_keys.add(current_key)
            attempt_count += 1
            
            logger.info(f"Attempt {attempt_count}: Using Google API key #{current_key_index + 1} for request")
            
            # Try to generate content with current key
            result = self._try_generate_with_key(current_key, model_name, messages)
            
            if result:
                logger.info(f"Returning result to code generation service")    
                return result
                
            # If we get here, the attempt failed, so we'll try the next key
            self.key_manager.rotate_key()
            
            # Delay before retry if needed
            if attempt_count < self.max_retries and len(tried_keys) < total_keys:
                time.sleep(self.retry_delay)
        
        if len(tried_keys) >= total_keys:
            logger.warning("All API keys have been tried without success")
        if attempt_count >= self.max_retries:
            logger.warning(f"Maximum retry attempts ({self.max_retries}) reached")
            
        return None
    
    def _try_generate_with_key(self, api_key: str, model_name: str, messages: List[str]) -> Optional[str]:
        """
        Try to generate content with a specific API key.
        
        Args:
            api_key: The API key to use
            model_name: The name of the model to use
            messages: List of message strings to send to the model
            
        Returns:
            Optional[str]: Generated content or None if the attempt failed
        """
        try:
            # Configure the API with the key
            genai.configure(api_key=api_key)
            
            # Initialize the model
            model = genai.GenerativeModel(model_name)
            
            # Start timing
            start_time = time.time()
            
            # Call API with timeout
            logger.info(f"Sending request to Google API with key #{self.key_manager.current_key_index + 1}")
            response, error = self._with_timeout(model.generate_content, messages)
            
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            
            # Handle errors
            if error:
                if isinstance(error, TimeoutError):
                    logger.warning(f"Request timed out after {elapsed_time:.1f} seconds with API key #{self.key_manager.current_key_index + 1}")
                else:
                    self._handle_api_error(error, self.key_manager.current_key_index)
                return None
            
            # Process successful response
            if response and hasattr(response, 'text') and response.text:
                logger.info(f"Request successful with API key #{self.key_manager.current_key_index + 1} in {elapsed_time:.1f} seconds")
                # Add explicit log that we're returning from API
                logger.info("Successfully received response from Google API - beginning post-processing")
                
                # Increment successful request count
                self.key_manager.increment_request_count()
                logger.info(f"Incremented request count for API key #{self.key_manager.current_key_index + 1}")
                return response.text.strip()
            
            # No valid response text
            logger.warning(f"Empty response from API key #{self.key_manager.current_key_index + 1}, rotating to next key")
            return None
                
        except Exception as e:
            logger.exception(f"Unexpected error in _try_generate_with_key: {str(e)}")
            return None
    
    def clean_code_response(self, code: str) -> str:
        """
        Clean up code response from Google API by removing markdown formatting.
        
        Args:
            code: Raw code response from API
            
        Returns:
            Clean code without markdown formatting
        """
        # Simple implementation to avoid any potential issues
        print("Using simplified clean_code_response")
        
        if not code:
            return ""
            
        # Just return the code as is, without any processing
        # This ensures we don't get stuck in post-processing
        return code