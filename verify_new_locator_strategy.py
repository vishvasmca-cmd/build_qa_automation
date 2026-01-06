
import os
import sys
import json
from core.refiner import CodeRefiner

def verify():
    print("🚀 Verifying New Locator Strategy Generation...")
    refiner = CodeRefiner()
    
    # Mock Trace with complex scenarios
    mock_trace = {
        "target_url": "https://example.com/ecommerce",
        "trace": [
            {
                "step": 1,
                "thought": "I need to click the add to cart button for the Premium Laptop",
                "action": "click",
                "locator_used": "page.locator('.product-card').nth(1).get_by_role('button')",
                "url": "https://example.com/ecommerce",
                "element_context": {
                    "tag": "BUTTON",
                    "text": "Add to Cart",
                    "role": "button",
                    "parent_text": "Premium Laptop $1,299"
                }
            },
            {
                "step": 2,
                "thought": "I need to click the View Details button for the notification from 2 hours ago",
                "action": "click",
                "locator_used": "page.locator('.action').nth(5)",
                "url": "https://example.com/notifications",
                "element_context": {
                    "tag": "BUTTON",
                    "text": "View Details",
                    "role": "button",
                    "container_context": {
                        "message": "Your order has shipped",
                        "timestamp": "2 hours ago"
                    }
                }
            }
        ]
    }
    
    # Run Refiner
    test_path = "projects/verify_strategy_test.py"
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    
    # We pass the trace summary directly or save it
    trace_summary = json.dumps(mock_trace, indent=2)
    
    print("🤖 Invoking Refiner...")
    # Manually calling refiner logic to get the code
    code = refiner.generate_code("https://example.com/ecommerce", trace_summary)
    
    if code:
        print("\n✅ Generated Code Snippet:")
        print("-" * 40)
        print(code)
        print("-" * 40)
        
        # Check for expected locators
        if "filter" in code and "get_by_role" in code:
            print("✨ SUCCESS: Refiner is using Chaining and Filtering!")
        else:
            print("❌ FAILURE: Refiner did not use expected chaining/filtering logic.")
            
        if "smart_action" in code:
            print("✨ SUCCESS: Refiner is using smart_action wrapper.")
    else:
        print("❌ Refiner failed to generate code.")

if __name__ == "__main__":
    verify()
