
- ⚠️ PROHIBITED: DON'T assume the 'Enter Country' field is immediately available; it might be dynamically loaded or require a specific state to be visible.

- ✅ PREFERRED: DO implement explicit waiting mechanisms (e.g., `wait_for_selector`, `wait_for_element_state`) before attempting to interact with the 'Enter Country' field to ensure it's fully loaded and visible.

- ⚠️ PROHIBITED: DON'T rely on partial text matches or generic class names like `.ui-menu-item div` when targeting elements in dynamically generated lists. These are prone to ambiguity.

- ✅ PREFERRED: DO use exact text matches, unique attributes (e.g., IDs), or chain locators to precisely target the desired element in dynamic lists. Leverage `nth()` or `first()` if necessary after narrowing down the selection.
