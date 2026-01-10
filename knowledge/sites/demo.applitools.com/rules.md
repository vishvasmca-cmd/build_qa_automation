
- ⚠️ PROHIBITED: DON'T assume elements with test IDs are immediately available; always account for potential loading times or animations.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements, especially those identified by test IDs, to ensure they are fully loaded and interactive before attempting to fill or click.

- ⚠️ PROHIBITED: DON'T assume that elements with `data-test` attributes are immediately available; always account for potential loading delays or dynamic rendering.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements identified by `data-test` attributes, especially after page loads or transitions.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; always implement explicit waits for critical elements.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before interacting with elements, especially after navigation or significant UI changes.

- ⚠️ PROHIBITED: DON'T assume that elements with `data-test` attributes are immediately available; always account for potential loading delays or dynamic rendering.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements, especially those identified by `data-test` attributes, to ensure they are fully loaded and interactive.

- ⚠️ PROHIBITED: DON'T assume that elements with `data-test` attributes are immediately available; always implement retry mechanisms or explicit waits.

- ✅ PREFERRED: DO use `page.locator('[data-test="username"]').wait_for(state='visible', timeout=5000)` before attempting to fill the username field to ensure it's present and ready for interaction.

- ⚠️ PROHIBITED: DON'T assume that elements with `data-test` attributes are immediately available; always account for potential loading times or animations.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements, especially those identified by `data-test` attributes, to ensure they are fully loaded and interactive.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; always wait for it to be present before attempting to fill it.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before interacting with elements, especially after page loads or navigations.

- ⚠️ PROHIBITED: DON'T assume that elements with `data-test` attributes are immediately available; always account for potential loading delays or animations.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements, especially those identified by `data-test` attributes, to ensure they are fully loaded and interactive.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; always implement explicit waits for critical elements.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before interacting with elements, especially after navigation or significant UI changes.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; ALWAYS implement explicit waits for critical elements to appear and become interactable.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before attempting to interact with elements, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T assume elements are immediately available after page load; always implement explicit waits for critical elements like the username field.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before attempting to interact with elements, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T assume that elements with simple IDs are immediately available; always account for potential loading delays or animations.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements, especially after page loads or transitions, to ensure they are fully loaded and interactable.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available and interactable upon page load. ALWAYS implement a check for its presence and visibility before attempting to fill it.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` before attempting to interact with the username field to ensure it is fully loaded and ready for input.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; always implement explicit waits for critical elements.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before interacting with elements, especially after navigation or significant page changes.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; always wait for it to be visible and enabled before attempting to fill it.

- ✅ PREFERRED: DO use `page.locator('[id='username']').wait_for(state='visible', timeout=5000)` before attempting to fill the username field to ensure it is present and interactable.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; account for potential loading delays or animations.

- ✅ PREFERRED: DO implement explicit waiting mechanisms (e.g., `locator.wait_for()` or `locator.is_visible()`) before attempting to interact with the username field.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; always implement a retry mechanism or explicit wait for its presence.

- ✅ PREFERRED: DO implement explicit waits with `locator.wait_for()` before attempting to interact with elements, especially after page loads or navigations.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; always check for its presence and visibility before attempting to fill it.

- ✅ PREFERRED: DO use `locator.wait_for()` with explicit visibility and/or enabled state checks before interacting with critical form elements like the username field.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; always check for its presence and visibility before attempting to fill it.

- ✅ PREFERRED: DO implement a retry mechanism or explicit waiting strategy (e.g., `wait_for_selector`, `wait_for_element_state`) to ensure the username field is fully loaded and interactable before attempting to fill it.

- ⚠️ PROHIBITED: DON'T assume that the username field is immediately available; always implement a wait strategy.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before attempting to fill the username field, or use `locator.is_visible()` to check if the element is visible before interacting with it.

- ⚠️ PROHIBITED: DON'T rely solely on role-based locators with regular expressions for critical elements like 'Sign in' buttons without verifying their reliability across different environments and states.

- ✅ PREFERRED: DO implement explicit waits with error handling for critical elements like 'Sign in' buttons, especially when using role-based locators or regular expressions, and consider adding visual validation to confirm the element's presence and state.

- ⚠️ PROHIBITED: DON'T assume that the login button is immediately available after page load. Always implement a wait strategy.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='stable'` before attempting to click on critical elements like the login button, especially after navigation or content updates.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; ALWAYS implement explicit waits for critical elements like login buttons.

- ✅ PREFERRED: DO use `locator.evaluate` to check if the element is visible and enabled before attempting to click it, especially after a page load or navigation.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available after page load; always implement a wait strategy.

- ✅ PREFERRED: DO implement an explicit wait for the '#log-in' button to be visible and enabled before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'` options.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available after page load. It might be rendered dynamically or blocked by an overlay.

- ✅ PREFERRED: DO implement explicit waits with `locator.wait_for()` before interacting with critical elements like the '#log-in' button, ensuring they are visible and enabled.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available; always implement a retry mechanism or explicit wait with error handling.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff or a longer explicit wait (e.g., 60 seconds) for the '#log-in' button to handle potential loading delays or intermittent issues.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available; always implement a wait strategy.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='enabled'` before attempting to click the '#log-in' button to ensure it's ready for interaction.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available after page load; it might be dynamically loaded or require a specific state to be clickable.

- ✅ PREFERRED: DO implement explicit waits with `locator.wait_for()` before attempting to click '#log-in' to ensure it's visible, enabled, and stable.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available after page load; it might be hidden or disabled.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='enabled'` before attempting to click the '#log-in' button to ensure it's ready for interaction.

- ⚠️ PROHIBITED: DON'T assume the '#log-in' button is immediately available; always implement a check for its presence and interactability before attempting to click it.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` and `state='enabled'` options before clicking the '#log-in' button to ensure it's ready for interaction.
