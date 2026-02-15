
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
        implementation="""
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
        implementation="""
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
        implementation="""
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
        implementation="""
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
        implementation="""
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
