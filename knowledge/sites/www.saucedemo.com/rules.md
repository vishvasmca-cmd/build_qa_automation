
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

- ⚠️ PROHIBITED: DON'T assume that elements with test IDs are immediately available; always account for potential loading delays or animations.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements identified by test IDs, especially after page loads or transitions.

- ⚠️ PROHIBITED: DON'T use ambiguous locators that can resolve to multiple elements without specifying which element is intended.

- ✅ PREFERRED: DO use more specific locators, such as data-test attributes or chained locators, to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T run asynchronous tests without installing and configuring a suitable pytest plugin (e.g., pytest-asyncio).

- ✅ PREFERRED: DO ensure that the pytest environment is properly configured with the necessary plugins to support the type of tests being executed (synchronous vs. asynchronous).

- ⚠️ PROHIBITED: DON'T assume that elements with test IDs are immediately available after page load; always implement a reasonable wait or retry mechanism.

- ✅ PREFERRED: DO use `locator.wait_for()` with a shorter, more appropriate timeout before interacting with elements, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T use ambiguous locators that can resolve to multiple elements without specifying which element is intended.

- ✅ PREFERRED: DO use more specific locators, such as data-test attributes or unique class names, to target the intended element precisely.

- ⚠️ PROHIBITED: DON'T call Playwright Locator objects directly as functions. Use the appropriate `expect` methods (e.g., `to_be_visible()`, `to_have_text()`) on the Locator object.

- ✅ PREFERRED: DO use the `expect` function from Playwright to assert conditions on Locator objects. For example, `expect(page.locator('.inventory_item').first()).to_be_visible()`.

- ⚠️ PROHIBITED: DON'T pass a raw Locator object directly to the `expect` function without chaining it with an assertion method.

- ✅ PREFERRED: ALWAYS chain a Locator object with an assertion method (e.g., `.to_be_visible()`, `.to_have_count()`) when using `expect` for assertions.

- ⚠️ PROHIBITED: DON'T pass a string directly to `expect(page.url).to_contain()`. Always use a Locator object when asserting on page URLs or other dynamic content.

- ✅ PREFERRED: DO use `expect(page).to_have_url()` or `expect(page.locator('locator')).to_have_text()` when asserting on page URLs or dynamic content.

- ⚠️ PROHIBITED: DON'T use `expect(True).to_be(True)` for assertions. Playwright's `expect` function requires a Playwright object (Page, Locator, APIResponse) to operate on.

- ✅ PREFERRED: DO use Playwright's `expect` function with a Locator object to assert on the state or properties of elements on the page (e.g., `expect(page.locator('#checkout_complete')).to_be_visible()`).

- ⚠️ PROHIBITED: DON'T use wildcard characters in `to_have_url` assertions unless the URL is genuinely dynamic and the wildcard is intended to match a variable part of the URL. Prefer exact matches when possible.

- ✅ PREFERRED: DO use exact URL matches in `to_have_url` assertions whenever the expected URL is static and known. If a portion of the URL is dynamic, use regular expressions or string manipulation to create a more robust assertion.

- ⚠️ PROHIBITED: DON'T assume the checkout process will always require a distinct 'checkout-step-one.html' page; the flow might sometimes skip it.

- ✅ PREFERRED: DO verify the presence of key elements on 'checkout-step-two.html' (e.g., order summary) instead of relying solely on URL matching for 'checkout-step-one.html'.

- ⚠️ PROHIBITED: DON'T assume the page will pause on 'checkout-step-one.html'; the transition to 'checkout-step-two.html' might be too fast to reliably assert.

- ✅ PREFERRED: DO verify the presence of elements specific to 'checkout-step-one.html' *before* asserting the URL, to ensure the page has fully loaded and rendered.

- ⚠️ PROHIBITED: DON'T assume the application will always navigate sequentially through checkout steps; verify each step independently.

- ✅ PREFERRED: DO implement explicit waits or assertions after filling checkout information to ensure the application has fully processed the data and navigated to the expected 'checkout-step-one.html' page before proceeding.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will always resolve correctly without verifying the project's root directory and PYTHONPATH.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory. Verify the PYTHONPATH environment variable is correctly set if needed.
