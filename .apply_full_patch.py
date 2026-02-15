"""
Comprehensive patch to add tool-driven goal verification to explorer.py
"""
import re

print("Reading explorer.py...")
with open('core/agents/explorer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports to include verification tools
print("Step 1: Updating imports...")
import_pattern = r'(from core\.lib\.webmcp_polyfill import \(  # WebMCP integration\s+WebMCPPolyfill,\s+create_sort_products_tool_polyfill,\s+create_add_to_cart_by_rank_tool_polyfill,\s+create_get_cart_total_tool_polyfill,\s+create_login_tool_polyfill)\s*\)'

import_replacement = r'''\1,
    create_verify_cart_items_tool_polyfill,
    create_get_cart_count_tool_polyfill,
    create_verify_cart_total_tool_polyfill,
    create_get_sorted_products_tool_polyfill,
    create_verify_checkout_form_tool_polyfill
)'''

content = re.sub(import_pattern, import_replacement, content)

# 2. Update tool registrations
print("Step 2: Adding tool registrations...")
registration_pattern = r'(self\.webmcp\.register_tool\(create_login_tool_polyfill\(\)\))'
registration_replacement = r'''\1
        # Verification tools
        self.webmcp.register_tool(create_verify_cart_items_tool_polyfill())
        self.webmcp.register_tool(create_get_cart_count_tool_polyfill())
        self.webmcp.register_tool(create_verify_cart_total_tool_polyfill())
        self.webmcp.register_tool(create_get_sorted_products_tool_polyfill())
        self.webmcp.register_tool(create_verify_checkout_form_tool_polyfill())'''

content = re.sub(registration_pattern, registration_replacement, content)

# 3. Read and insert the new methods before _verify_goal_completion (if it exists)
print("Step 3: Inserting tool-driven methods...")
with open('.temp_tool_methods.py', 'r', encoding='utf-8') as f:
    new_methods = f.read()

# Find _verify_goal_completion and insert before it
verify_pattern = r'(\n\s+async def _verify_goal_completion\()'
if re.search(verify_pattern, content):
    content = re.sub(verify_pattern, '\n' + new_methods + r'\1', content, count=1)
    print("   ✓ Inserted methods before _verify_goal_completion")
else:
    print("   ⚠ _verify_goal_completion not found, appending methods to end")
    content += '\n' + new_methods

# Write the updated content
print("Writing updated explorer.py...")
with open('core/agents/explorer.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ SUCCESS: All changes applied to explorer.py")
print("\nNext steps:")
print("1. Integrate method calls into _explore_scenario loop")
print("2. Test the tool-driven verification")
