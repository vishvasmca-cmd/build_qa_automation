import re
from typing import Dict, Any, List

async def _parse_goal_requirements(self, goal: str) -> Dict[str, Any]:
    """
    Parse goal string to extract structured requirements.
    Returns dict with cart_item_count, required_fields, completion_keywords.
    """
    requirements = {
        "cart_item_count": None,
        "required_fields": {},
        "completion_keywords": []
    }
    
    # Cart item count: "verify 2 items exist"
    if match := re.search(r"verify (\d+) items? exist", goal, re.I):
        requirements["cart_item_count"] = int(match.group(1))
    
    # Required fields: "Zip: 90210"
    if match := re.search(r"Zip:\s*(\d+)", goal, re.I):
        requirements["required_fields"]["postal-code"] = match.group(1)
    
    # Completion indicators
    if "checkout" in goal.lower() and ("complete" in goal.lower() or "verify" in goal.lower()):
        requirements["completion_keywords"] = ["complete", "thank you", "order placed"]
    
    return requirements


async def _validate_current_state(self, page: Page, requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate current page state against parsed requirements.
    Returns validation result with violations and corrective actions.
    """
    violations = []
    corrective_action = None
    
    # Check cart item count
    if requirements.get("cart_item_count"):
        try:
            cart_count = await page.locator('.cart_item').count()
            expected = requirements["cart_item_count"]
            
            if cart_count < expected:
                violations.append(f"Cart has {cart_count} items, expected {expected}")
                # Force navigation back to inventory
                corrective_action = "navigate -> https://www.saucedemo.com/inventory.html"
                self.log(f"    [VALIDATE] Cart Violation: {cart_count}/{expected} items", "red")
        except Exception as e:
            self.log(f"    [WARN] Cart validation error: {e}", "yellow")
    
    # Check required form fields
    for field_id, expected_value in requirements.get("required_fields", {}).items():
        try:
            field = page.locator(f"#{field_id}, [name='{field_id}']")
            if await field.count() > 0:
                actual_value = await field.input_value()
                if not actual_value:
                    violations.append(f"Field '{field_id}' is empty")
                    corrective_action = f"fill -> {field_id.replace('-', ' ').title()}"
        except:
            pass
    
    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "corrective_action": corrective_action
    }
