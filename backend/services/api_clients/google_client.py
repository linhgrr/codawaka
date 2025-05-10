"""
API client for Google Generative AI services.
"""
import google.generativeai as genai
from typing import Optional, List, Dict, Any
import time

class GoogleApiClient:
    """
    Client for interacting with Google's Generative AI API.
    Uses a key manager to handle API key rotation and rate limits.
    With retry mechanism for failed requests.
    """
    
    def __init__(self, key_manager, max_retries=3, retry_delay=1):
        """
        Initialize with a key manager for API keys.
        
        Args:
            key_manager: An instance of GoogleAPIKeyManager
            max_retries: Maximum number of retry attempts (default: 3)
            retry_delay: Delay between retries in seconds (default: 1)
        """
        self.key_manager = key_manager
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def generate_content(self, model_name: str, messages: List[str]) -> Optional[str]:
        """
        Generate content using Google's Generative AI API.
        If request fails, it will retry with different API keys.
        
        Args:
            model_name: The name of the model to use
            messages: List of message strings to send to the model
            
        Returns:
            Optional[str]: Generated content or None if all attempts failed
        """
        # Track which keys we've already tried
        tried_keys = set()
        total_keys = len(self.key_manager.api_keys)
        retries = 0
        
        while retries < self.max_retries and len(tried_keys) < total_keys:
            try:
                # Get current API key and ensure it's configured
                current_key = self.key_manager.get_current_key()
                tried_keys.add(current_key)
                
                genai.configure(api_key=current_key)
                
                # Log which key is being used (for debugging)
                print(f"Attempt {retries+1}: Using Google API key #{self.key_manager.current_key_index + 1} for request")
                
                # Initialize the model
                model = genai.GenerativeModel(model_name)
                
                # Generate content
                response = model.generate_content(messages)
                
                # After successful generation, increment the key usage count
                self.key_manager.increment_request_count()
                
                # Extract the text response
                if response and response.text:
                    print(f"Request successful with API key #{self.key_manager.current_key_index + 1}")
                    return response.text.strip()
                
                # No valid response, rotate key and retry
                print(f"Empty response from API key #{self.key_manager.current_key_index + 1}, rotating to next key")
                self.key_manager.rotate_key()
                retries += 1
                time.sleep(self.retry_delay)
                
            except Exception as e:
                print(f"Error with Google API key #{self.key_manager.current_key_index + 1}: {str(e)}")
                
                # Rotate to next key
                self.key_manager.rotate_key()
                retries += 1
                
                # Only delay if we're going to retry
                if retries < self.max_retries and len(tried_keys) < total_keys:
                    time.sleep(self.retry_delay)
        
        if len(tried_keys) >= total_keys:
            print("All API keys have been tried without success")
        if retries >= self.max_retries:
            print(f"Maximum retry attempts ({self.max_retries}) reached")
            
        return None
    
    def clean_code_response(self, code: str) -> str:
        """
        Clean up code response from Google API by removing markdown formatting.
        
        Args:
            code: Raw code response from API
            
        Returns:
            Clean code without markdown formatting
        """
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