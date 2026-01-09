
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
