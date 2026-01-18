# Implementation Plan - Smart Product Selection logic

## Problem
The `ExplorerAgent` fails to select the "first product" after a search operation.
1. **Random Collection Logic:** The current code specifically *randomizes* selection when it detects a collection (lines 407-408 in `explorer.py`). This directly contradicts the user's goal to "add *first* dress".
2. **Ambiguous Locators:** The Vision AI might return a locator that matches *all* 'View Product' buttons (e.g., `.view-product-btn`), and without specific handling, Playwright might error on strict mode or the agent might click an arbitrary one.

## Proposed Solution

### 1. Deterministic Collection Handling in `ExplorerAgent`
Modify `_execute_exploration_action` in `core/agents/explorer.py`.
- **Remove Randomness:** Instead of `random.randint`, check the step description or arguments for ordinal keywords involved ("first", "1st", "second", "random").
- **Default to First:** If no specific ordinal is found, default to selecting the **first** element (`nth=0`) rather than a random one. This is standard automation behavior.

### 2. Update Domain Expert Heuristics
Update `core/lib/domain_expert.py`.
- **Product Grid Awareness:** Add a heuristic for `ecommerce` that explicitly mentions: "When viewing product lists, prefer specific unique identifiers or use 'nth=0' to target the first item if no specific product is requested."

### 3. Tactical "Force Click" Refinement
Ensure the `force=True` logic (which we recently added) applies correctly to these collection items.

## Verification Plan
1. **Code Modification:** Apply changes to `explorer.py` and `domain_expert.py`.
2. **Unit Check:** Verify `_execute_exploration_action` logic handles "first" correctly.
3. **Live Run:** Execute the "Search and Add to Cart" scenario.
   - **Success Criteria:** Agent searches 'dress' -> Identify list of products -> Explicitly clicks the *first* 'View Product' or 'Add to Cart' button -> Verifies cart.
