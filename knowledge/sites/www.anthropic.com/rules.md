
- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded content without implementing proper waiting mechanisms or considering alternative, more stable locators.

- ✅ PREFERRED: DO implement explicit waits with `page.wait_for_selector()` or `page.wait_for_load_state()` before interacting with elements that are known to load dynamically. Also, consider using data-testid attributes for more robust locators.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded content; it's prone to timing issues.

- ✅ PREFERRED: DO implement explicit waits with `page.locator(...).wait_for()` and consider using more specific locators (e.g., CSS selectors with data attributes) to target elements reliably.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded content without implementing proper waiting mechanisms or considering alternative, more stable locators.

- ✅ PREFERRED: DO implement explicit waits with `page.wait_for_selector()` or `page.wait_for_load_state()` before interacting with elements that are likely to load dynamically. ALSO, consider using data-testid attributes for more robust locators.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a simple name if the element is dynamically loaded or part of a complex component. The name might be ambiguous or not immediately available.

- ✅ PREFERRED: DO use a more specific locator, such as combining `get_by_role` with `within` or `filter` to target the element within a specific container or based on additional attributes. Also, ALWAYS implement explicit waits with reasonable timeouts for dynamically loaded elements.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded content without implementing proper waiting mechanisms or considering alternative, more robust locators.

- ✅ PREFERRED: DO implement explicit waits with `locator.wait_for()` or `page.wait_for_selector()` with a reasonable timeout before interacting with elements that might load dynamically. Consider using more specific locators like data attributes or CSS classes if available.

- ⚠️ PROHIBITED: DON'T rely solely on exact text matches for link names, especially when dealing with dynamically loaded content or potential variations in wording.

- ✅ PREFERRED: DO use more robust locators like data attributes (e.g., data-wf-element-id) or a combination of role and partial text matching to identify links, and implement retry mechanisms with appropriate timeouts.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded or frequently changing elements. The text content might be inconsistent or the element might not be immediately available.

- ✅ PREFERRED: DO implement retry mechanisms or explicit waits with `page.wait_for_selector()` before interacting with elements, especially those that might be dynamically loaded or subject to A/B testing variations. Consider using more robust locators like data attributes or CSS selectors in conjunction with text matching.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded content; it's prone to timing issues.

- ✅ PREFERRED: DO implement explicit waits with `page.locator(...).wait_for()` and consider using more resilient locators like data attributes or CSS selectors in conjunction with role-based locators.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a simple name if the element is dynamically loaded or part of a complex component. The name might be ambiguous or not immediately available.

- ✅ PREFERRED: DO use a more specific locator, combining `get_by_role` with other attributes like `href` or `data-wf-element-id`, and implement explicit waits with longer timeouts when dealing with dynamically loaded content.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role('link', name='...')` for dynamically loaded elements or elements within complex layouts. The name might be ambiguous or change frequently.

- ✅ PREFERRED: DO use more specific locators, such as CSS selectors combined with text matching, or chained locators to target the element more accurately. Consider using `nth` or `first` to disambiguate if multiple elements match.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a broad regex for link names, especially when multiple links might contain the target text.

- ✅ PREFERRED: DO use more specific locators, combining `get_by_role` with additional attributes (e.g., `data-wf-element-id`, `href`) or `nth` to target the desired element precisely. Consider adding explicit waits for the element to be visible before interacting with it.

- ⚠️ PROHIBITED: DON'T attempt to call a Playwright Locator object directly. Locators are not functions.

- ✅ PREFERRED: DO chain actions like `.click()` directly to the Playwright Locator object returned by locator methods (e.g., `page.get_by_role`).

- ⚠️ PROHIBITED: DON'T attempt to call a Playwright Locator object directly. Locators are not functions.

- ✅ PREFERRED: DO chain actions like `.click()` directly to the Playwright Locator object returned by methods like `page.get_by_role()`.

- ⚠️ PROHIBITED: DON'T directly call `.click()` on a Playwright `Locator` object.  Locators need to resolve to an element first.

- ✅ PREFERRED: DO resolve a Playwright `Locator` to an element using `.first().click()` or `.nth(index).click()` or `.all()` before attempting to interact with it.

- ⚠️ PROHIBITED: DON'T attempt to call a Playwright Locator object directly. Locators are not functions.

- ✅ PREFERRED: DO apply actions like `.click()` directly to the Locator object returned by methods like `get_by_role()` and `first()`.

- ⚠️ PROHIBITED: DON'T call the `first` property of a Playwright Locator object as a function (e.g., `locator.first()`). Access it directly (e.g., `locator.first`).

- ✅ PREFERRED: DO access the `first` property of a Playwright Locator object directly to retrieve the first matching element (e.g., `locator.first`).

- ⚠️ PROHIBITED: DON'T attempt to call a Playwright Locator object directly. Locators are not functions.

- ✅ PREFERRED: DO chain actions like `.click()` directly to the Locator object returned by Playwright's locator methods (e.g., `page.get_by_role()`).

- ⚠️ PROHIBITED: DON'T directly call a Playwright Locator object as a function to perform actions like clicking. Locators must be resolved to elements first.

- ✅ PREFERRED: DO use the `.click()` method on a Playwright Locator object to perform a click action after defining the locator.

- ⚠️ PROHIBITED: DON'T call a Playwright Locator object directly as a function. Use methods like `click()` or refine the locator further before performing actions.

- ✅ PREFERRED: DO use the `click()` method directly on the Locator object returned by `page.get_by_role()` or similar locator methods. If you need a specific element from a list of elements matched by the locator, refine the locator using methods like `first()` or `nth()` BEFORE calling `click()`.

- ⚠️ PROHIBITED: DON'T treat a Playwright Locator object as a clickable element directly after using `.first()`.  Locators need to resolve to an element before interaction.

- ✅ PREFERRED: DO resolve a Playwright Locator to an actual element using `.locator()` or `.element_handle()` before attempting to interact with it (e.g., clicking).

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a broad regex like `re.compile(r"Claude", re.IGNORECASE)` without considering potential ambiguity or timing issues. It can lead to false negatives if the element is slow to load or other elements match the regex.

- ✅ PREFERRED: DO use more specific locators, such as combining `get_by_role` with `data-wf-element-id` or `href` attributes, and implement explicit waits with reasonable timeouts to ensure elements are fully loaded before interacting with them.

- ⚠️ PROHIBITED: DON'T rely solely on element visibility and stability for click actions on elements within dynamic sections; interception can still occur.

- ✅ PREFERRED: DO implement explicit waits for potential intercepting elements to disappear or become non-interactive before attempting to click the target element.

- ⚠️ PROHIBITED: DON'T rely solely on element visibility and stability checks when elements are known to be dynamically covered by other elements. Avoid direct clicks on elements in the navigation bar without ensuring no overlays are present.

- ✅ PREFERRED: DO use `locator.evaluate()` with `element.click()` to force a click on the target element, bypassing Playwright's built-in interception checks.  Also, ALWAYS add a short delay or wait for the intercepting element to disappear before clicking.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or dynamically loaded; implement explicit waiting or alternative interaction methods.

- ✅ PREFERRED: DO use `locator.evaluate()` with `element.click()` to force a click on the element, bypassing Playwright's built-in checks, but only after ensuring the element is visible and stable using `locator.waitForElementState('visible')` and `locator.waitForElementState('stable')`.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or unstable. A simple click may fail due to interception.

- ✅ PREFERRED: DO implement explicit waiting and/or force option in click when dealing with potentially overlapping or dynamically appearing elements. Consider using `element.hover()` before `element.click()` to reveal the target.

- ⚠️ PROHIBITED: DON'T rely solely on element visibility and stability checks; always account for potential overlapping elements that might intercept pointer events.

- ✅ PREFERRED: DO implement a retry mechanism with a short delay and a check for element interception before attempting a click action. Consider using `force: true` as a last resort, but only after exhausting other options.

- ⚠️ PROHIBITED: DON'T immediately click on navigation elements after page load; ensure all overlays and animations are complete.

- ✅ PREFERRED: DO implement explicit waits for element stability (e.g., `locator.wait_for(state='stable')`) before attempting to interact with potentially obscured elements.

- ⚠️ PROHIBITED: DON'T rely solely on element visibility and stability checks when elements are known to be dynamically covered by other elements. Avoid immediate clicks after scrolling.

- ✅ PREFERRED: DO use `locator.hover()` before `locator.click()` to potentially reveal the target element and ensure it's not intercepted. Alternatively, use `locator.force_click()` as a last resort, understanding its potential instability.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or unstable. A simple click may fail due to interception.

- ✅ PREFERRED: DO implement explicit waiting and/or force option when clicking elements that might be obscured or unstable. Consider using `element.click({force: true})` or `element.waitForElementState('stable')` before clicking.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or unstable; it can lead to intermittent failures.

- ✅ PREFERRED: DO implement explicit waiting and/or force-click options when interacting with elements that are prone to interception or instability.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are likely to be obscured or dynamically loaded; the default retry mechanism is insufficient.

- ✅ PREFERRED: DO implement explicit waiting and/or force-click options when interacting with elements that are prone to interception or instability.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or dynamically loaded; it can lead to intermittent failures.

- ✅ PREFERRED: DO implement explicit waiting and retry mechanisms with targeted locator refinement to ensure elements are truly clickable before attempting interaction.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or unstable; ALWAYS implement explicit waiting or alternative targeting strategies.

- ✅ PREFERRED: DO use `locator.hover()` before `locator.click()` to ensure the target element is fully visible and interactive, or use `locator.force_click()` if interception is unavoidable and the element is guaranteed to eventually be clickable.

- ⚠️ PROHIBITED: DON'T rely solely on default Playwright click behavior when elements are potentially obscured or unstable. A simple click may not work.

- ✅ PREFERRED: DO implement explicit waiting and retry mechanisms with targeted locator refinement to ensure the target element is truly clickable and not intercepted before attempting the click action.
