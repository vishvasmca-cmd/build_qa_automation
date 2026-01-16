"""
Base Tool class for the Tool Registry pattern.
All automation tools inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from playwright.async_api import Page


class Tool(ABC):
    """
    Base class for all automation tools.
    Each tool encapsulates a specific automation capability.
    """
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.last_error = None
    
    @abstractmethod
    async def execute(self, page: Page, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool's primary action.
        
        Args:
            page: Playwright Page object
            **kwargs: Tool-specific arguments
            
        Returns:
            Dict with 'status' (success/failure) and relevant data
        """
        pass
    
    @abstractmethod
    def get_signature(self) -> Dict[str, Any]:
        """
        Returns the tool's signature for documentation and validation.
        
        Returns:
            Dict with 'description', 'arguments', 'example'
        """
        pass
    
    async def validate_args(self, **kwargs) -> bool:
        """
        Validate the arguments before execution.
        Override in subclass for custom validation.
        """
        return True
    
    def _log(self, message: str, level: str = "INFO"):
        """Internal logging helper"""
        prefix = "✅" if level == "SUCCESS" else "⚠️" if level == "WARN" else "📋"
        print(f"{prefix} [{self.name}] {message}")
