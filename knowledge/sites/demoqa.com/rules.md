
- ⚠️ PROHIBITED: DON'T rely solely on the default 'networkidle' load state without considering potential network issues or slow-loading resources. Avoid implicit waits.

- ✅ PREFERRED: DO implement explicit waits for critical elements to appear on the page after navigation, or use a more lenient load state like 'domcontentloaded' if appropriate. Consider increasing the timeout or retrying the navigation.

- ⚠️ PROHIBITED: DON'T use ambiguous locators like '#item-2' without ensuring they uniquely identify the target element.

- ✅ PREFERRED: DO use more specific locators, such as combining ID with text matching or using role-based locators with filters, to target elements accurately.

- ⚠️ PROHIBITED: DON'T assume an element is immediately visible and interactable after page load or state change. ALWAYS verify visibility and stability before attempting actions.

- ✅ PREFERRED: DO use `locator.wait_for()` with explicit visibility and/or enabled state checks before interacting with elements, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T use ambiguous locators like '#item-2' without ensuring they uniquely identify the target element.

- ✅ PREFERRED: DO use more specific locators, combining attributes, text content, or roles to uniquely identify elements, especially when dealing with dynamic content or lists.

- ⚠️ PROHIBITED: DON'T assume elements are immediately visible and clickable after page load; always verify their visibility before interacting with them.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` to ensure an element is fully rendered and interactive before attempting to click or interact with it.

- ⚠️ PROHIBITED: DON'T use ambiguous locators like '#item-2' without ensuring uniqueness; always validate locator specificity.

- ✅ PREFERRED: DO use more specific locators, combining attributes, text content, or hierarchical relationships to target elements uniquely (e.g., using `nth=0` or `first` to select the first matching element, or combining `get_by_role` with `filter` and specific text).

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the project's root directory is correctly set in the test environment.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory. Verify the project structure and adjust import statements accordingly.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project's directory structure and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and module import paths to ensure that all modules can be imported correctly.

- ⚠️ PROHIBITED: DON'T use ambiguous locators that can resolve to multiple elements without using filters or explicit indexing.

- ✅ PREFERRED: DO use more specific locators, such as data attributes, text matching, or role-based selectors, to target unique elements.
