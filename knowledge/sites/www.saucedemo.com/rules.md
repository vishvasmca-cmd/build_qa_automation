
- Before filling the username field, ensure the page is fully loaded and the username input field is visible. Consider adding a wait_for_selector or wait_for_load_state before attempting to fill the field.

- Before filling the username field, ensure the page is fully loaded and any modals or overlays are dismissed. Consider adding a short delay or explicit wait for the username field to be visible.

- Before interacting with the 'ProductsSort by' dropdown, ensure that the page is fully loaded and the dropdown is visible and enabled. Consider adding an explicit wait for the dropdown element.

- Before attempting to fill the username field, ensure the page is fully loaded and the element is visible. Consider adding a wait-for-selector with a shorter timeout before attempting to fill.

- When extracting text from a Playwright Locator object, access the `inner_text` property directly instead of attempting to call it as a function.

- When verifying sorted order, ensure the `expect` assertion receives a Playwright Locator object representing the elements to be checked, not a boolean result of a sorting comparison.

- When verifying a condition using Playwright's `expect` function, ensure that you are passing a Playwright object (Page, Locator, APIResponse) to the `expect` function, not a boolean or other primitive data type. Use Locator.evaluate() to get the sorted values and then use expect(locator).to_have_values(expected_values)

<<<<<<< Updated upstream
- Before attempting to fill the username field, ensure the page is fully loaded and any overlays or modals are dismissed. Consider adding a short wait or an explicit check for the username field's visibility before attempting to fill it.
=======
- Before attempting to fill the username field, ensure the page is fully loaded and any overlaying elements (e.g., modals, spinners) are dismissed. Consider adding a short explicit wait for the username field to be visible before attempting to fill it.
>>>>>>> Stashed changes

- ⚠️ PROHIBITED: DON'T pass the string result of `page.url` directly to `expect(page.url).to_contain()`. The `expect` function requires a Playwright object like `page` or `locator`.

- ✅ PREFERRED: DO pass the Playwright `page` object to the `expect` function when asserting on the URL, and then use the `.to_contain()` method with the expected URL fragment. For example: `expect(page).to_have_url(expected_url)` or `expect(page).to_have_url(re.compile(expected_url_regex))`.

- ⚠️ PROHIBITED: DON'T attempt to call a Playwright Locator object directly as a function. Use appropriate Playwright actions like `.click()` or `.fill()` on the Locator object.

- ✅ PREFERRED: DO use Playwright's action methods (e.g., `.click()`, `.fill()`, `.hover()`) on Locator objects to interact with page elements.

- ⚠️ PROHIBITED: DON'T assume elements are immediately available; always account for potential loading times or animations.

- ✅ PREFERRED: DO use explicit waits or retries when interacting with elements that might not be immediately present in the DOM.

- ⚠️ PROHIBITED: DON'T assume a successful login solely based on immediate response; ALWAYS verify the navigation to the target page (e.g., /inventory.html) within a reasonable timeout.

- ✅ PREFERRED: DO implement explicit waits for critical page elements to load after navigation, especially after login, to ensure the application is fully ready for subsequent actions.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; always implement a retry mechanism or explicit wait for its presence and interactability.

- ✅ PREFERRED: DO use `page.locator('locator').first.fill('value')` to ensure you are interacting with the correct element, especially when multiple elements match the locator.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; ALWAYS implement explicit waits for critical elements to become visible and interactable.

- ✅ PREFERRED: DO use more resilient locators that are less prone to changes in the UI, such as ARIA labels or roles, when available. Prioritize unique attributes over chained locators.
