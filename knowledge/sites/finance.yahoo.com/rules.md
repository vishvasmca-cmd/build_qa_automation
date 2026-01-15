
- ⚠️ PROHIBITED: DON'T rely on exact text matching for navigation elements like 'News' headings, as content can change dynamically or be A/B tested.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for critical navigation elements, especially when dealing with dynamically loaded content or external websites.

- ⚠️ PROHIBITED: DON'T assume that the 'Markets' link is immediately visible and clickable upon page load. Account for potential loading delays or dynamic content insertion.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the 'Markets' link is present and enabled before attempting to click it. Consider using `locator.wait_for()` with a reasonable timeout.

- ⚠️ PROHIBITED: DON'T rely on exact text matching for headings, especially when content is dynamically loaded or A/B tested. This can lead to brittle tests.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes or a combination of roles and partial text matches, along with explicit waits for element visibility and stability before attempting to interact with them.

- ⚠️ PROHIBITED: DON'T assume that navigation links are immediately available; always implement a short wait or retry mechanism.

- ✅ PREFERRED: DO use `wait_for_selector` or `wait_for_load_state` to ensure the target element is present and interactable before attempting to click it.

- ⚠️ PROHIBITED: DON'T rely on exact text matching for dynamic content like 'News' headings, as the content or presence of the element might vary.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes or CSS selectors that are less prone to changes in text content or page structure. Consider adding a wait condition to ensure the element is visible and stable before attempting to click.

- ✅ PREFERRED: DO implement a retry mechanism or explicit waiting strategy (e.g., `page.wait_for_selector()` or `locator.wait_for()` with `state='visible'`) before attempting to click the 'Markets' link.

- ⚠️ PROHIBITED: DON'T rely on exact text matching for navigation elements like 'News' headings, as content can change frequently or be localized.

- ✅ PREFERRED: DO implement retry mechanisms or longer timeouts for critical navigation elements, especially when dealing with dynamic content or external websites.

- ⚠️ PROHIBITED: DON'T assume that elements like 'Markets' links are immediately available upon page load; account for potential loading delays or dynamic content rendering.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements that might not be immediately present or stable, especially for navigation elements like 'Markets' links.

- ⚠️ PROHIBITED: DON'T rely on exact text matching for navigation elements like 'News' headings, as dynamic content or A/B testing might alter the text slightly.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes or CSS selectors, combined with retry mechanisms or increased timeouts when targeting potentially slow-loading or dynamically changing elements.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; always implement explicit waits for critical elements.

- ✅ PREFERRED: DO use `locator.wait_for()` with a reasonable timeout before interacting with elements, especially those that might be dynamically loaded or subject to animations.
