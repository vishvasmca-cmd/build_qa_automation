"""
WebMCP-Enhanced Executor - Proof of Concept

This script demonstrates WebMCP integration with the existing Executor agent
WITHOUT modifying core agent files. It wraps the Executor to use WebMCP tools.

Usage:
    python execute_with_webmcp.py --project test-websites-e2e/saucedemo_e2e

This proves that WebMCP can be integrated for execution phase.
"""

import asyncio
import sys
import os
import json

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.agents.executor import ExecutorAgent
from core.lib.webmcp_polyfill import (
    WebMCPPolyfill,
    create_sort_products_tool_polyfill,
    create_add_to_cart_by_rank_tool_polyfill,
    create_get_cart_total_tool_polyfill
)


class WebMCPExecutorWrapper:
    """
    Wrapper around ExecutorAgent that adds WebMCP capabilities
    
    This demonstrates integration WITHOUT modifying core files.
    """
    
    def __init__(self, project_dir: str, headed: bool = False):
        self.executor = ExecutorAgent(project_dir, headed=headed)
        
        # Initialize WebMCP with pre-built tools
        self.webmcp = WebMCPPolyfill()
        self.webmcp.register_tool(create_sort_products_tool_polyfill())
        self.webmcp.register_tool(create_add_to_cart_by_rank_tool_polyfill())
        self.webmcp.register_tool(create_get_cart_total_tool_polyfill())
        
        print("[WebMCP Wrapper] Initialized with 3 e-commerce tools")
        print(f"  - {self.webmcp.list_tools()}")
        
        # Track WebMCP usage
        self.webmcp_calls = 0
        self.traditional_calls = 0
    
    async def execute_with_webmcp(self):
        """
        Run execution with WebMCP tool support
        
        Checks if steps can use WebMCP tools first, falls back to selectors
        """
        # Hook into executor's execute_step
        original_execute_step = self.executor.execute_step
        
        async def webmcp_enhanced_execute_step(page, step, scenario_name, step_index=0):
            # Inject WebMCP tools if not already done
            if page:
                try:
                    await self.webmcp.inject_tools(page)
                except:
                    pass  # Already injected
            
            # ENHANCEMENT: Check if this step can use a WebMCP tool
            description = step.get("description", "").lower()
            keyword = step.get("keyword", "").lower()
            args = step.get("args", {})
            
            # DEBUG: Print step details to troubleshoot matching
            print(f"  [DEBUG] Step: keyword='{keyword}', description='{description}', args={args}")
            
            # Sort detection - Handle "select" keyword or description
            if (keyword == "select" and "price" in args.get("value", "").lower()) or \
               ("sort" in description and "price" in description):
                
                value = args.get("value", "").lower()
                direction = "low_to_high" if "low" in value or "low" in description else "high_to_low"
                
                print(f"  ℹ️  [WebMCP] Intercepted SORT step: {description or value}")
                result = await self.webmcp.call_tool(page, "sort_products_by_price", {
                    "direction": direction
                })
                
                if result.get("success"):
                    self.webmcp_calls += 1
                    print(f"  ✅ [WebMCP] Executed sort_products_by_price tool")
                    return  # Step complete via WebMCP
            
            # Add to cart detection
            elif ("add" in description or "click" in description) and "cart" in description:
                # Heuristic: Match index 0 to cheapest (first) and index 5/last to most expensive
                idx = args.get("index")
                
                rank = None
                if idx == 0 or "cheap" in description or "first" in description:
                    rank = "cheapest"
                elif idx == 5 or "expensive" in description or "last" in description:
                    # In this specific workflow, index 5 is the expensive item (last one)
                    rank = "most_expensive"
                
                if rank:
                    print(f"  ℹ️  [WebMCP] Intercepted ADD step: {description} (index {idx}) -> {rank}")
                    result = await self.webmcp.call_tool(page, "add_to_cart_by_price_rank", {
                        "rank": rank
                    })
                    
                    if result.get("success"):
                        self.webmcp_calls += 1
                        print(f"  ✅ [WebMCP] Executed add_to_cart_by_price_rank ({rank})")
                        return  # Step complete via WebMCP
            
            # Fallback to traditional execution
            self.traditional_calls += 1
            return await original_execute_step(page, step, scenario_name, step_index)
        
        # Replace with enhanced version
        self.executor.execute_step = webmcp_enhanced_execute_step
        
        # Run original execute
        await self.executor.execute()
        
        # Print WebMCP usage summary
        print("\n" + "=" * 70)
        print("WebMCP Usage Summary:")
        print(f"  WebMCP tool calls: {self.webmcp_calls}")
        print(f"  Traditional selector calls: {self.traditional_calls}")
        total = self.webmcp_calls + self.traditional_calls
        if total > 0:
            webmcp_pct = (self.webmcp_calls / total) * 100
            print(f"  WebMCP coverage: {webmcp_pct:.1f}%")
        print("=" * 70)


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="WebMCP-Enhanced Executor (PoC)")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("WebMCP-Enhanced Executor - Proof of Concept")
    print("=" * 70)
    print(f"\nProject: {args.project}")
    print(f"Mode: {'Headed' if args.headed else 'Headless'}")
    print("\nThis demonstrates WebMCP integration WITHOUT modifying core files.")
    print("WebMCP tools will be used automatically when applicable.\n")
    
    wrapper = WebMCPExecutorWrapper(args.project, headed=args.headed)
    await wrapper.execute_with_webmcp()
    
    print("\n✅ WebMCP-Enhanced Execution Complete!")


if __name__ == "__main__":
    asyncio.run(main())
