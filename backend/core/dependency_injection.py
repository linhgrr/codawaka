"""
Dependency Injection container for the application.
This module centralizes dependency management and ensures services are properly initialized.
"""
from typing import Dict, Type, Any

class DIContainer:
    """
    A simple dependency injection container.
    Manages singleton instances of services and their dependencies.
    """
    _instances: Dict[Type, Any] = {}
    
    @classmethod
    def get_instance(cls, service_class, *args, **kwargs):
        """
        Get or create an instance of the specified service class.
        If an instance already exists, return it, otherwise create a new one.
        
        Args:
            service_class: The class to instantiate
            *args, **kwargs: Arguments to pass to the constructor
            
        Returns:
            An instance of the service_class
        """
        if service_class not in cls._instances:
            cls._instances[service_class] = service_class(*args, **kwargs)
        return cls._instances[service_class]
    
    @classmethod
    def register_instance(cls, service_class, instance):
        """
        Register an existing instance for a service class.
        
        Args:
            service_class: The class to register
            instance: The instance to register
        """
        cls._instances[service_class] = instance
    
    @classmethod
    def clear_instances(cls):
        """
        Clear all registered instances.
        Mainly used for testing.
        """
        cls._instances.clear()