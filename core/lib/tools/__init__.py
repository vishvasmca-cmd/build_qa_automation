"""
Tool Registry - Central repository for all automation tools.
"""

from typing import Dict, Optional
from .base_tool import Tool
from .search_tool import SearchTool
from .click_tool import ClickTool
from .fill_tool import FillTool
from .fill_tool import FillTool
from .navigate_tool import NavigateTool
from .verify_tool import VerifyTool
from .get_css_hierarchy import GetCssHierarchyTool


class ToolRegistry:
    """
    Central registry for all automation tools.
    Manages tool discovery, loading, and execution.
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._load_default_tools()
    
    def _load_default_tools(self):
        """Load all built-in tools into the registry"""
        self.register_tool("perform_search", SearchTool())
        self.register_tool("smart_click", ClickTool())
        self.register_tool("smart_fill", FillTool())
        self.register_tool("navigate_to", NavigateTool())
        self.register_tool("verify_text", VerifyTool())
        self.register_tool("get_css_hierarchy", GetCssHierarchyTool())
    
    def register_tool(self, name: str, tool: Tool):
        """Register a new tool"""
        self.tools[name] = tool
        print(f"📦 Registered tool: {name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> Dict[str, Dict]:
        """List all available tools with their signatures"""
        return {
            name: tool.get_signature() 
            for name, tool in self.tools.items()
        }
    
    async def execute_tool(self, tool_name: str, page, **kwargs):
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            page: Playwright Page object
            **kwargs: Tool-specific arguments
            
        Returns:
            Execution result from the tool
        """
        tool = self.get_tool(tool_name)
        
        if not tool:
            return {
                "status": "failure",
                "error": f"Tool '{tool_name}' not found in registry"
            }
        
        # Validate args if the tool supports it
        if hasattr(tool, 'validate_args'):
            if not await tool.validate_args(**kwargs):
                return {
                    "status": "failure",
                    "error": "Invalid arguments for tool"
                }
        
        # Execute the tool
        return await tool.execute(page=page, **kwargs)


# Global registry instance
_registry = None

def get_registry() -> ToolRegistry:
    """Get the global tool registry (singleton pattern)"""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry
