
- ⚠️ PROHIBITED: DON'T use ambiguous locators that can match multiple elements without providing additional context or specificity.

- ✅ PREFERRED: DO use more specific locators, such as chained locators or ARIA attributes, to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T rely solely on role-based locators for critical navigation elements without ensuring their immediate visibility and clickability.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with elements that may require time to become available or stable, especially after page loads or dynamic content updates.

- ⚠️ PROHIBITED: DON'T assume that the project structure and import paths are correct without verifying them before running the tests.

- ✅ PREFERRED: DO double-check the project's directory structure and import statements to ensure that all modules are accessible before running the tests.

- ⚠️ PROHIBITED: DON'T use `get_by_role("link", name="Demo")` without specifying the context or disambiguating the target element when multiple elements match.

- ✅ PREFERRED: DO use more specific locators, such as chaining locators or using `nth()` to target the desired element when multiple elements match a general locator.

- ⚠️ PROHIBITED: DON'T use `get_by_role` with ambiguous names without additional filtering (e.g., `.first`, `.last`, or `nth(index)`).

- ✅ PREFERRED: DO use more specific locators, such as `getByRole('link', {name: 'Hotels', exact: true})` or target a parent element with a unique identifier to narrow the scope.

- ⚠️ PROHIBITED: DON'T use `get_by_role` without specifying a unique container or element when multiple elements with the same role and name exist.

- ✅ PREFERRED: DO use more specific locators, such as chaining locators or using `nth()` to target the desired element when multiple elements match the initial locator.

- ⚠️ PROHIBITED: DON'T use `get_by_role` without sufficient context when multiple elements with the same role and name exist on the page.

- ✅ PREFERRED: DO use more specific locators, such as `nth()`, `first()`, `last()`, or combine with other attributes (e.g., `data-testid`, `class`) to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T use ambiguous locators that can match multiple elements without providing additional context or specificity.

- ✅ PREFERRED: DO use more specific locators, such as chained locators or `nth()` to target the desired element when multiple elements match the initial locator.

- ⚠️ PROHIBITED: DON'T use `get_by_role` without ensuring uniqueness, especially when targeting common elements like 'link' with generic names.

- ✅ PREFERRED: DO use more specific locators, such as `nth(0)`, `first`, `last`, or combine with other attributes (e.g., `data-testid`, `class`) to target the intended element uniquely.

- ⚠️ PROHIBITED: DON'T use `get_by_role` with overly broad criteria (like just 'link' and 'Demo') without ensuring uniqueness or scoping to a specific container.

- ✅ PREFERRED: DO use more specific locators, such as chaining locators to target elements within a specific section (e.g., navigation bar or footer) or using attributes to distinguish between elements with the same role and name.

- ⚠️ PROHIBITED: DON'T use `get_by_role` without sufficient context when multiple elements with the same role and name exist on the page.

- ✅ PREFERRED: DO use more specific locators, such as chaining locators or using `nth()` to target the desired element when multiple elements match the initial locator.

- ⚠️ PROHIBITED: DON'T use `get_by_role` with ambiguous names without additional filtering (e.g., `.first`, `.last`, or `nth(index)`).

- ✅ PREFERRED: DO use more specific locators, such as `getByRole` combined with `filter` or `locator.nth()` to target the intended element when multiple elements match the initial locator.

- ⚠️ PROHIBITED: DON'T use `get_by_role` without sufficient context when multiple elements with the same role and name exist on the page.

- ✅ PREFERRED: DO use more specific locators, such as chaining locators or using `nth()` to target the desired element when multiple elements match the initial locator.

- ⚠️ PROHIBITED: DON'T assume that navigation links are immediately available after page load; always implement a waiting mechanism.

- ✅ PREFERRED: DO use explicit waits with `locator.wait_for()` to ensure elements are visible and enabled before attempting to interact with them.
