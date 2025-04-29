"""
Manager for Google API keys with round-robin rotation for error handling.
"""
import threading
from typing import Dict, List
import logging

# Configure logging
logger = logging.getLogger("google_key_manager")

class GoogleAPIKeyManager:
    """
    Manages Google API keys using rotation when errors occur.
    Implemented as a singleton to ensure only one instance is used throughout the application.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GoogleAPIKeyManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        """
        Initialize the key manager if not already initialized.
        Configuration is loaded when initialize() is called separately.
        """
        if not hasattr(self, '_initialized') or not self._initialized:
            self.api_keys = []
            self.current_key_index = 0
            self._initialized = False
    
    def initialize(self, api_keys: List[str]):
        """
        Initialize the key manager with keys.
        
        Args:
            api_keys: List of Google API keys
        """
        with self._lock:
            self.api_keys = api_keys
            self.current_key_index = 0
            
            # Keys must be set before using the manager
            if not self.api_keys:
                raise ValueError("No Google API keys available. Please provide at least one API key.")
                
            self._initialized = True
            logger.info(f"GoogleAPIKeyManager initialized with {len(self.api_keys)} keys")
    
    def get_current_key(self) -> str:
        """
        Get the current API key.
        
        Returns:
            str: The current API key
        
        Raises:
            ValueError: If no API keys are available or manager is not initialized
        """
        with self._lock:
            if not self._initialized:
                raise ValueError("GoogleAPIKeyManager not initialized. Call initialize() first.")
                
            if not self.api_keys:
                raise ValueError("No Google API keys available")
                
            return self.api_keys[self.current_key_index]
    
    def rotate_key(self) -> None:
        """
        Rotate to the next API key in the list.
        """
        logger.info("Rotating to the next API key")
        with self._lock:
            if not self._initialized:
                logger.error("GoogleAPIKeyManager not initialized. Cannot rotate key.")
                return
                
            if not self.api_keys:
                logger.error("No API keys available. Cannot rotate.")
                return
            
            # Move to next key
            old_index = self.current_key_index
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            
            logger.info(f"Rotated from key index {old_index} to key index {self.current_key_index}")