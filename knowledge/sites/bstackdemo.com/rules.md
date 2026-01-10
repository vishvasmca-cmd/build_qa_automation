
- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or transition. It might be covered by a loading overlay or require some JavaScript to fully initialize.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with the 'Add to cart' button to ensure it is visible and enabled before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It might be obscured or not yet fully rendered.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with the 'Add to cart' button to ensure it's visible and enabled before attempting to click it.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. Always implement a short wait or visibility check.

- ✅ PREFERRED: DO use explicit waits with `locator.wait_for()` to ensure the 'Add to cart' button is visible and enabled before attempting to click it. Consider using `locator.is_visible()` or `locator.is_enabled()` as conditions.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It may require a short wait or a specific condition to be met.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with 'Add to cart' buttons, especially after actions that might trigger dynamic content updates.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a generic name like 'Add to cart' without ensuring uniqueness or waiting for element stability.

- ✅ PREFERRED: DO implement explicit waits and consider more specific locators (e.g., using data attributes or CSS selectors) to target the 'Add to cart' button, especially when dealing with potentially dynamic content or overlays.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page transition. It may be obscured by a loading overlay or other dynamic content.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with 'Add to cart' buttons, especially after page transitions or dynamic content updates. Consider using `locator.wait_for()` with a `state='visible'` or `state='enabled'` option.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It may require a short delay or a specific condition to be met.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the 'Add to cart' button is visible, enabled, and stable before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It might be behind a loading state or animation.

- ✅ PREFERRED: DO implement explicit waits with `page.locator(...).first.wait_for()` before attempting to click the 'Add to cart' button, checking for visibility and/or enabling.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or transition. It might be covered by an overlay, animation, or still loading.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the 'Add to cart' button is visible and enabled before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. It might be covered by a loading overlay or require some JavaScript to execute first.

- ✅ PREFERRED: DO implement a retry mechanism or explicit wait condition before clicking the 'Add to cart' button, ensuring it is both visible and enabled.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; always account for potential loading delays or animations.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements that may not be immediately available, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T rely on deeply nested CSS selectors that are prone to breaking due to minor UI changes. AVOID using auto-generated or framework-specific class names like 'MuiModal-root' or 'css-8ndowl'.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes (e.g., data-testid, data-qa) or ARIA labels, to identify elements. If those are unavailable, use a combination of more stable CSS selectors and explicit waits for element visibility and stability.

- ⚠️ PROHIBITED: DON'T assume that the cart icon ('1 item') is immediately clickable after adding an item. Account for potential delays due to animations or background processes.

- ✅ PREFERRED: DO implement explicit waits with error handling to ensure the cart icon ('1 item') is both visible and enabled before attempting to click it.

- ⚠️ PROHIBITED: DON'T pass a function directly as the role name argument to `getByRole`. Ensure you are passing a string or a regular expression.

- ✅ PREFERRED: DO verify that the argument passed to `getByRole` for the role name is a string or a regular expression before using it in the locator.

- ⚠️ PROHIBITED: DON'T rely on deeply nested CSS selectors that are prone to breaking due to minor UI changes. AVOID using auto-generated CSS classes like 'css-10if7qv'.

- ✅ PREFERRED: DO use more resilient locators, such as data-testid attributes, ARIA roles, or text-based selectors, whenever possible. If CSS selectors are necessary, prefer stable, semantic class names.

- ⚠️ PROHIBITED: DON'T assume the 'View cart' button is immediately clickable after adding an item to the cart. Account for potential loading times or overlays.

- ✅ PREFERRED: DO implement a retry mechanism or explicit wait condition for the 'View cart' button to become clickable after adding an item to the cart. Consider checking for the absence of a loading overlay or the presence of a specific element indicating readiness.

- ⚠️ PROHIBITED: DON'T rely on deeply nested CSS selectors or dynamically generated class names for critical UI elements like buttons in the floating cart. These are prone to breaking with UI updates.

- ✅ PREFERRED: DO use more resilient locators, such as role-based selectors (e.g., `getByRole('button', { name: 'Checkout' })`) or data attributes (e.g., `data-test-id='checkout-button'`) to identify UI elements.  Prioritize data attributes assigned by developers for testing purposes.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. Always implement a wait strategy.

- ✅ PREFERRED: DO use explicit waits with `locator.wait_for()` before clicking the 'Add to cart' button, ensuring it's both visible and enabled.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. Always implement a wait strategy.

- ✅ PREFERRED: DO use explicit waits with `locator.wait_for()` to ensure the 'Add to cart' button is visible and enabled before attempting to click it.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately available after a page transition. NEVER click it without explicitly waiting for it to be visible and enabled.

- ✅ PREFERRED: DO use explicit waits with error handling to ensure the 'Add to cart' button is both visible and enabled before attempting to click it. ALWAYS check for overlay elements that might be blocking the button.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. It might be covered by an overlay or require some elements to load first.

- ✅ PREFERRED: DO implement explicit waits or use Playwright's auto-waiting features to ensure the 'Add to cart' button is visible and enabled before attempting to click it.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. It might be covered by a loading overlay or require some JavaScript to execute.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with the 'Add to cart' button to ensure it's visible and enabled before attempting to click it.

- ⚠️ PROHIBITED: DON'T rely on default Playwright timeouts for critical UI elements; ALWAYS explicitly wait for expected states (e.g., visibility, enabled) before interacting.

- ✅ PREFERRED: DO implement explicit waits with reasonable timeouts and error handling to ensure elements are ready for interaction before attempting to click or otherwise interact with them.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately available after page load; always implement a waiting mechanism.

- ✅ PREFERRED: DO use explicit waits with `locator.wait_for()` or `locator.is_visible()` before attempting to interact with dynamic elements like the 'Add to cart' button.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. Always implement a check for its visibility and/or enabled state before attempting to click.

- ✅ PREFERRED: DO implement explicit waits with error handling for critical elements like the 'Add to cart' button, especially after actions that might cause a delay in their appearance or availability. Consider using `locator.wait_for()` with specific state options (e.g., `visible`, `enabled`).

- ⚠️ PROHIBITED: DON'T rely on the 'Add to cart' button being immediately available after a page load or product selection. There might be loading delays or animations that prevent interaction.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the 'Add to cart' button is visible and enabled before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. Account for potential delays due to animations, overlays, or dynamic content loading.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with elements like 'Add to cart' buttons, especially after page transitions or dynamic content updates. Consider using `locator.wait_for()` with a `state='visible'` or `state='enabled'` option.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately available after a page load or product selection. NEVER click it without explicitly waiting for its visibility and stability.

- ✅ PREFERRED: DO implement explicit waits with error handling for the 'Add to cart' button to ensure it is visible and interactable before attempting to click. ALWAYS use `locator.wait_for()` with `state='visible'` and `timeout` parameter before clicking.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. ALWAYS implement a retry mechanism or explicit wait condition.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='enabled'` before attempting to click the 'Add to cart' button to ensure it's ready for interaction.

- ⚠️ PROHIBITED: DON'T rely solely on role-based locators like `get_by_role` for critical elements like 'Add to cart' without additional specificity or checks for visibility and stability.

- ✅ PREFERRED: DO implement explicit waits and visibility checks before interacting with elements, especially those that might be dynamically loaded or subject to UI animations. Consider using `locator.wait_for()` with `state='visible'` before clicking.
