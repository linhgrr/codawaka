"""
API client for OpenAI services.
"""
import openai
from typing import Optional, List, Dict, Any

class OpenAIApiClient:
    """
    Client for interacting with OpenAI's API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize with API key.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key
        openai.api_key = api_key
    
    def generate_code(self, model_name: str, system_prompt: str, user_prompt: str,
                     temperature: float = 0.2, max_tokens: int = 4000) -> Optional[str]:
        """
        Generate code using OpenAI API.
        
        Args:
            model_name: The name of the OpenAI model to use
            system_prompt: The system prompt for context
            user_prompt: The user prompt with specific request
            temperature: The randomness parameter (default: 0.2)
            max_tokens: Maximum tokens in the response (default: 4000)
            
        Returns:
            Optional[str]: Generated code or None if generation failed
        """
        try:
            response = openai.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            # Extract the generated code from the response
            if response and response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            return None
        except Exception as e:
            print(f"Error generating code with OpenAI: {str(e)}")
            return None
    
    async def generate_code_async(self, model_name: str, system_prompt: str, user_prompt: str,
                               temperature: float = 0.2, max_tokens: int = 4000) -> Optional[str]:
        """
        Generate code using OpenAI API asynchronously.
        
        Args:
            model_name: The name of the OpenAI model to use
            system_prompt: The system prompt for context
            user_prompt: The user prompt with specific request
            temperature: The randomness parameter (default: 0.2)
            max_tokens: Maximum tokens in the response (default: 4000)
            
        Returns:
            Optional[str]: Generated code or None if generation failed
        """
        try:
            async with openai.AsyncClient(api_key=self.api_key) as client:
                response = await client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                
                # Extract the generated code from the response
                if response and response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content.strip()
                return None
        except Exception as e:
            print(f"Error generating code with OpenAI async: {str(e)}")
            return None