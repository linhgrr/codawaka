"""
Manager for Google API keys with round-robin rotation and rate limiting.
"""
import threading
from typing import Dict, List
import logging

# Configure logging
logger = logging.getLogger("google_key_manager")

class GoogleAPIKeyManager:
    """
    Manages Google API keys using a round-robin approach to respect rate limits.
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
            self.request_counts = {}
            self.max_requests_per_key = 0
            self._initialized = False
    
    def initialize(self, api_keys: List[str], max_requests_per_key: int = 100):
        """
        Initialize the key manager with keys and settings.
        
        Args:
            api_keys: List of Google API keys
            max_requests_per_key: Maximum number of requests per key before rotation
        """
        with self._lock:
            self.api_keys = api_keys
            self.current_key_index = 0
            self.request_counts = {key: 0 for key in self.api_keys}
            self.max_requests_per_key = max_requests_per_key
            
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
    
    def increment_request_count(self) -> None:
        """
        Increment the request count for the current key and rotate if needed.
        """
        logger.info("Incrementing request count for current API key")
        with self._lock:
            if not self._initialized:
                raise ValueError("GoogleAPIKeyManager not initialized. Call initialize() first.")
                
            current_key = self.api_keys[self.current_key_index]
            self.request_counts[current_key] += 1
            
            # Check if we need to rotate to the next key
            if self.request_counts[current_key] >= self.max_requests_per_key:
                logger.info(f"API key {current_key} has reached its request limit. Rotating to next key.")
                self.rotate_key()
    
    def rotate_key(self) -> None:
        """
        Rotate to the next API key in the list.
        """
        logger.info("Rotating to the next API key")
        try:
            # Use a timeout when acquiring lock to prevent deadlock
            if not self._lock.acquire(timeout=2):  # 2 second timeout
                logger.warning("Could not acquire lock for key rotation within timeout - continuing with existing key")
                return
                
            try:
                if not self._initialized:
                    logger.error("GoogleAPIKeyManager not initialized. Cannot rotate key.")
                    return
                    
                if not self.api_keys:
                    logger.error("No API keys available. Cannot rotate.")
                    return
                    
                # Reset current key's count if we've gone through all keys
                if all(count >= self.max_requests_per_key for count in self.request_counts.values()):
                    self.request_counts = {key: 0 for key in self.api_keys}
                
                # Move to next key
                old_index = self.current_key_index
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                
                logger.info(f"Rotated from key index {old_index} to key index {self.current_key_index}")
            finally:
                # Always release the lock
                self._lock.release()
        except Exception as e:
            logger.exception(f"Error rotating API key: {str(e)}")
            # Make sure we don't leave the lock acquired
            try:
                self._lock.release()
            except:
                pass
    
    def reset_counts(self) -> None:
        """Reset all request counts to zero."""
        with self._lock:
            if not self._initialized:
                raise ValueError("GoogleAPIKeyManager not initialized. Call initialize() first.")
                
            self.request_counts = {key: 0 for key in self.api_keys}
            logger.info("Reset all API key request counts to zero")