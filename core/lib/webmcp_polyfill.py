"""
WebMCP Polyfill - Works without Chrome 145+ or flags

This provides the same WebMCP interface as webmcp_wrapper.py but uses standard
page.evaluate() instead of navigator.modelContext API.

Benefits:
- ✅ Works on ANY Chromium/Chrome version
- ✅ Same API as native WebMCP
- ✅ Drop-in replacement - switch to native when available
- ✅ Production-ready TODAY

Use this until Chrome enables WebMCP by default.
"""

import json
from typing import Dict, Any, List
from playwright.async_api import Page


class WebMCPPolyfillTool:
    """Polyfill version of WebMCP tool"""
    
    def __init__(self, name: str, description: str, input_schema: Dict, execute_js: str):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.execute_js = execute_js


class WebMCPPolyfill:
    """
    Polyfill for WebMCP - provides same functionality without navigator.modelContext
    
    Works by injecting tools into window.__webmcp namespace
    """
    
    def __init__(self):
        self.tools: Dict[str, WebMCPPolyfillTool] = {}
    
    def register_tool(self, tool: WebMCPPolyfillTool):
        """Register a tool for injection"""
        self.tools[tool.name] = tool
        print(f"[WebMCP Polyfill] Tool registered: {tool.name}")
    
    async def inject_tools(self, page: Page):
        """Inject all tools into page via window.__webmcp"""
        
        # Build tools object for injection
        tools_dict = {}
        for name, tool in self.tools.items():
            tools_dict[name] = tool.execute_js
        
        tools_json = json.dumps(tools_dict)
        
        # Inject polyfill namespace
        injection_script = f"""
            (() => {{
                // WebMCP Polyfill - provides same interface as navigator.modelContext
                window.__webmcp = window.__webmcp || {{}};
                window.__webmcp.tools = {tools_json};
                
                window.__webmcp.callTool = async (toolName, params) => {{
                    const tools = window.__webmcp.tools;
                    
                    if (!tools[toolName]) {{
                        return {{
                            success: false,
                            error: 'Tool not found: ' + toolName,
                            available_tools: Object.keys(tools)
                        }};
                    }}
                    
                    try {{
                        // Create function from string and execute
                        const toolFunc = new Function('params', 'return (' + tools[toolName] + ')(params)');
                        const result = await toolFunc(params);
                        return result;
                    }} catch (error) {{
                        return {{
                            success: false,
                            error: error.message,
                            tool: toolName,
                            stack: error.stack
                        }};
                    }}
                }};
                
                console.log('[WebMCP Polyfill] Injected ' + Object.keys(window.__webmcp.tools).length + ' tools');
            }})();
        """
        
        await page.add_init_script(injection_script)
        try:
            await page.evaluate(injection_script)
        except:
            pass # Ignore if evaluation fails (e.g. if page is navigating)
        print(f"[WebMCP Polyfill] ✅ Injected {len(self.tools)} tools into page (Persistent)")

    
    async def call_tool(self, page: Page, tool_name: str, params: Dict) -> Dict[str, Any]:
        """
        Call a registered tool
        
        Args:
            page: Playwright page
            tool_name: Name of tool to call
            params: Parameters matching tool's input schema
        
        Returns:
            Structured result from tool execution
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not registered",
                "available_tools": list(self.tools.keys())
            }
        
        params_json = json.dumps(params)
        
        result = await page.evaluate(f"""
            async () => {{
                return await window.__webmcp.callTool('{tool_name}', {params_json});
            }}
        """)
        
        return result
    
    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self.tools.keys())


# ============================================================================
# Pre-built E-Commerce Tools (Polyfill versions)
# ============================================================================

def create_sort_products_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill version of sort products tool"""
    return WebMCPPolyfillTool(
        name="sort_products_by_price",
        description="Sort products by price (low to high or high to low)",
        input_schema={
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["low_to_high", "high_to_low"]
                }
            }
        },
        execute_js="""
            async (params) => {
                const select = document.querySelector('.product_sort_container') || 
                              document.querySelector('select[data-test="product-sort-container"]') ||
                              document.querySelector('select[name*="sort"]');
                
                if (!select) {
                    return { success: false, error: "Sort dropdown not found" };
                }
                
                const value = params.direction === "low_to_high" ? "lohi" : "hilo";
                select.value = value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                
                await new Promise(resolve => setTimeout(resolve, 500));
                
                const products = [...document.querySelectorAll('.inventory_item')].map(p => ({
                    name: p.querySelector('.inventory_item_name')?.textContent || 'Unknown',
                    price: parseFloat((p.querySelector('.inventory_item_price')?.textContent ||'0').replace('$', ''))
                }));
                
                return {
                    success: true,
                    direction: params.direction,
                    product_count: products.length,
                    first_product: products[0],
                    last_product: products[products.length - 1]
                };
            }
        """
    )


def create_add_to_cart_by_rank_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill version of add to cart tool"""
    return WebMCPPolyfillTool(
        name="add_to_cart_by_price_rank",
        description="Add cheapest or most expensive product to cart",
        input_schema={
            "type": "object",
            "properties": {
                "rank": {
                    "type": "string",
                    "enum": ["cheapest", "most_expensive"]
                }
            }
        },
        execute_js="""
            async (params) => {
                const products = [...document.querySelectorAll('.inventory_item')].map(p => ({
                    element: p,
                    name: p.querySelector('.inventory_item_name')?.textContent || 'Unknown',
                    price: parseFloat((p.querySelector('.inventory_item_price')?.textContent || '0').replace('$', ''))
                }));
                
                if (products.length === 0) {
                    return { success: false, error: "No products found" };
                }
                
                products.sort((a, b) => a.price - b.price);
                const target = params.rank === "cheapest" ? products[0] : products[products.length - 1];
                
                const button = target.element.querySelector('button[data-test*="add-to-cart"]');
                if (!button) {
                    return { success: false, error: `No add to cart button for ${target.name}` };
                }
                
                button.click();
                
                const cartBadge = document.querySelector('.shopping_cart_badge');
                const cartCount = cartBadge ? parseInt(cartBadge.textContent) : 1;
                
                return {
                    success: true,
                    product_name: target.name,
                    price: target.price,
                    cart_count: cartCount,
                    rank: params.rank
                };
            }
        """
    )


def create_get_cart_total_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill version of get cart total tool"""
    return WebMCPPolyfillTool(
        name="get_cart_total",
        description="Get cart total and item count",
        input_schema={"type": "object", "properties": {}},
        execute_js="""
            async (params) => {
                const totalElement = document.querySelector('.summary_subtotal_label') ||
                                    document.querySelector('[data-test="subtotal-label"]');
                
                if (!totalElement) {
                    return { success: false, error: "Cart total not found" };
                }
                
                const totalText = totalElement.textContent;
                const totalMatch = totalText.match(/\\$([\\d.]+)/);
                const total = totalMatch ? parseFloat(totalMatch[1]) : 0;
                
                const items = document.querySelectorAll('.cart_item');
                
                return {
                    success: true,
                    total: total,
                    item_count: items.length,
                    total_text: totalText
                };
            }
            }
        """
    )


def create_login_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill version of standard login tool"""
    return WebMCPPolyfillTool(
        name="login",
        description="Log in to the application with username and password",
        input_schema={
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["username", "password"]
        },
        execute_js="""
            async (params) => {
                const userField = document.querySelector('input[data-test="username"]') || 
                                 document.querySelector('#user-name') || 
                                 document.querySelector('input[name="user-name"]') ||
                                 document.querySelector('input[name="username"]') ||
                                 document.querySelector('input[type="email"]');

                const passField = document.querySelector('input[data-test="password"]') || 
                                 document.querySelector('#password') || 
                                 document.querySelector('input[name="password"]') ||
                                 document.querySelector('input[type="password"]');

                const submitBtn = document.querySelector('input[data-test="login-button"]') || 
                                 document.querySelector('#login-button') || 
                                 document.querySelector('button[type="submit"]') ||
                                 document.querySelector('input[type="submit"]');

                if (!submitBtn) return { success: false, error: "Login button not found" };

                // Helper to set value compatible with React
                const setReactValue = (element, value) => {
                    const lastValue = element.value;
                    element.value = value;
                    const event = new Event('input', { bubbles: true });
                    // React 16+ hack
                    const tracker = element._valueTracker;
                    if (tracker) {
                        tracker.setValue(lastValue);
                    }
                    element.dispatchEvent(event);
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                };

                if (typeof userField !== 'undefined' && userField) setReactValue(userField, params.username);
                if (typeof passField !== 'undefined' && passField) setReactValue(passField, params.password);
                
                // Small delay to let React process
                await new Promise(r => setTimeout(r, 100));
                
                submitBtn.click();
                
                // Wait for navigation or error
                const maxWait = 5000;
                const start = Date.now();
                while (Date.now() - start < maxWait) {
                    if (window.location.href.includes('inventory.html')) {
                        return {
                            success: true,
                            username: params.username,
                            action: "login_submitted",
                            verified: true
                        };
                    }
                    if (document.querySelector('.error-message-container')) {
                         return {
                             success: false,
                             error: document.querySelector('[data-test="error"]').textContent
                         };
                    }
                    await new Promise(r => setTimeout(r, 100));
                }
                
                // Fallback: If we timed out but no error, maybe it worked?
                // But safer to say it failed verification
                if (window.location.href.includes('inventory.html')) {
                     return { success: true, verified: true };
                }
                
                return {
                    success: false,
                    error: "Login timeout - did not navigate to inventory",
                    current_url: window.location.href
                };
            }
        """
    )

def create_verify_cart_items_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill tool to get detailed cart contents"""
    return WebMCPPolyfillTool(
        name="verify_cart_items",
        description="Get detailed list of items currently in the cart",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
        execute_js="""
            async (params) => {
                const items = Array.from(document.querySelectorAll('.cart_item'));
                const result = items.map(item => ({
                    name: item.querySelector('.inventory_item_name')?.textContent || '',
                    price: item.querySelector('.inventory_item_price')?.textContent || '',
                    quantity: item.querySelector('.cart_quantity')?.textContent || '1'
                }));
                
                return {
                    success: true,
                    items: result,
                    count: result.length
                };
            }
        """
    )


def create_get_cart_count_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill tool to get exact cart item count"""
    return WebMCPPolyfillTool(
        name="get_cart_count",
        description="Get the exact number of items in the cart",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
        execute_js="""
            async (params) => {
                const count = document.querySelectorAll('.cart_item').length;
                const badgeCount = document.querySelector('.shopping_cart_badge')?.textContent || '0';
                
                return {
                    success: true,
                    count: count,
                    badge_count: parseInt(badgeCount)
                };
            }
        """
    )


def create_verify_cart_total_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill tool to get cart financial summary"""
    return WebMCPPolyfillTool(
        name="verify_cart_total",
        description="Get cart subtotal, tax, and total",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
        execute_js="""
            async (params) => {
                const subtotal = document.querySelector('.summary_subtotal_label')?.textContent || '';
                const tax = document.querySelector('.summary_tax_label')?.textContent || '';
                const total = document.querySelector('.summary_total_label')?.textContent || '';
                
                // Extract numeric values
                const extractPrice = (text) => {
                    const match = text.match(/\\$([\\d.]+)/);
                    return match ? parseFloat(match[1]) : 0;
                };
                
                return {
                    success: true,
                    subtotal: subtotal,
                    tax: tax,
                    total: total,
                    subtotal_amount: extractPrice(subtotal),
                    tax_amount: extractPrice(tax),
                    total_amount: extractPrice(total)
                };
            }
        """
    )


def create_get_sorted_products_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill tool to get current product listing with prices"""
    return WebMCPPolyfillTool(
        name="get_sorted_products",
        description="Get list of products with prices in current sort order",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
        execute_js="""
            async (params) => {
                const products = Array.from(document.querySelectorAll('.inventory_item'));
                const result = products.map(p => ({
                    name: p.querySelector('.inventory_item_name')?.textContent || '',
                    price: p.querySelector('.inventory_item_price')?.textContent || '',
                    price_amount: parseFloat((p.querySelector('.inventory_item_price')?.textContent || '$0').replace('$', ''))
                }));
                
                // Find cheapest and most expensive
                const sorted = [...result].sort((a, b) => a.price_amount - b.price_amount);
                
                return {
                    success: true,
                    products: result,
                    count: result.length,
                    cheapest: sorted[0],
                    most_expensive: sorted[sorted.length - 1]
                };
            }
        """
    )


def create_verify_checkout_form_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill tool to check checkout form completion"""
    return WebMCPPolyfillTool(
        name="verify_checkout_form",
        description="Check which checkout form fields are filled",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
        execute_js="""
            async (params) => {
                const firstName = document.querySelector('#first-name')?.value || '';
                const lastName = document.querySelector('#last-name')?.value || '';
                const postalCode = document.querySelector('#postal-code')?.value || '';
                
                const isComplete = !!(firstName && lastName && postalCode);
                
                return {
                    success: true,
                    first_name: firstName,
                    last_name: lastName,
                    postal_code: postalCode,
                    is_complete: isComplete,
                    missing_fields: [
                        ...(!firstName ? ['first_name'] : []),
                        ...(!lastName ? ['last_name'] : []),
                        ...(!postalCode ? ['postal_code'] : [])
                    ]
                };
            }
        """
    )

def create_verify_order_success_tool_polyfill() -> WebMCPPolyfillTool:
    """Polyfill tool to check if order was successful"""
    return WebMCPPolyfillTool(
        name="verify_order_success",
        description="Check if the order completion page is reached",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
        execute_js="""
            async (params) => {
                const header = document.querySelector('.complete-header')?.textContent || '';
                const text = document.querySelector('.complete-text')?.textContent || '';
                const isSuccess = header.includes('THANK YOU') || header.includes('Thank you') || text.includes('dispatch');
                
                return {
                    success: true,
                    is_success: isSuccess,
                    header: header,
                    message: text
                };
            }
        """
    )

