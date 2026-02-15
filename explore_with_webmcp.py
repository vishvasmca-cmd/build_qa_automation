"""
WebMCP-Enhanced Explorer - Proof of Concept

This script demonstrates WebMCP integration with the existing Explorer agent
WITHOUT modifying core agent files. It wraps the Explorer to inject WebMCP tools.

Usage:
    python explore_with_webmcp.py --project test-websites-e2e/saucedemo_e2e
    
This proves that WebMCP can be integrated non-invasively.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.agents.explorer import ExplorerAgent
from core.lib.webmcp_polyfill import (
    WebMCPPolyfill,
    create_sort_products_tool_polyfill,
    create_add_to_cart_by_rank_tool_polyfill,
    create_get_cart_total_tool_polyfill
)


class WebMCPExplorerWrapper:
    """
    Wrapper around ExplorerAgent that adds WebMCP capabilities
   
    This demonstrates integration WITHOUT modifying core files.
    """
    
    def __init__(self, project_dir: str, headed: bool = False):
        self.explorer = ExplorerAgent(project_dir, headed=headed)
        
        # Initialize WebMCP with pre-built tools
        self.webmcp = WebMCPPolyfill()
        self.webmcp.register_tool(create_sort_products_tool_polyfill())
        self.webmcp.register_tool(create_add_to_cart_by_rank_tool_polyfill())
        self.webmcp.register_tool(create_get_cart_total_tool_polyfill())
        
        print("[WebMCP Wrapper] Initialized with 3 e-commerce tools")
        print(f"  - {self.webmcp.list_tools()}")
    
    async def explore_with_webmcp(self):
        """
        Run exploration with WebMCP tool injection
        
        This hooks into the exploration process to inject WebMCP tools
        """
        # Monkey-patch the explorer's explore method to inject WebMCP
        original_explore_scenario = self.explorer._explore_scenario
        
        async def webmcp_enhanced_explore_scenario(page, scenario, discovery_stats, depth=0):
            # Inject WebMCP tools before exploring
            if page:
                await self.webmcp.inject_tools(page)
                print(f"[WebMCP] Tools injected into {page.url}")
            
            # Call original exploration
            return await original_explore_scenario(page, scenario, discovery_stats, depth)
        
        # Replace with enhanced version
        self.explorer._explore_scenario = webmcp_enhanced_explore_scenario
        
        # Run original explore
        await self.explorer.explore()


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="WebMCP-Enhanced Explorer (PoC)")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("WebMCP-Enhanced Explorer - Proof of Concept")
    print("=" * 70)
    print(f"\nProject: {args.project}")
    print(f"Mode: {'Headed' if args.headed else 'Headless'}")
    print("\nThis demonstrates WebMCP integration WITHOUT modifying core files.")
    print("Web MCP tools will be automatically injected during exploration.\n")
    
    wrapper = WebMCPExplorerWrapper(args.project, headed=args.headed)
    await wrapper.explore_with_webmcp()
    
    print("\n" + "=" * 70)
    print("✅ WebMCP-Enhanced Exploration Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
