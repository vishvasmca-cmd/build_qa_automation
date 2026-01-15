
- ⚠️ PROHIBITED: DON'T rely on exact text matches for dynamically updated elements like stock prices; the values change too frequently.

- ✅ PREFERRED: DO use more robust locators, such as data attributes or stable CSS selectors, combined with explicit waits for element stability when dealing with dynamic content.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for elements displaying dynamic data like stock prices; these values change frequently and will cause test failures.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes or ARIA labels, that are less susceptible to changes in dynamic content. If dynamic text is unavoidable, consider using partial text matching or regular expressions.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for dynamically updated elements like stock prices. The price fluctuations will cause the test to fail intermittently.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes or ARIA labels, combined with partial text matching or regular expressions to identify the target element, and implement retry mechanisms with short intervals.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for dynamically updating elements like stock prices; the values change too frequently.

- ✅ PREFERRED: DO use more robust and less volatile locators, such as data attributes or stable CSS classes, to identify elements that display dynamic data.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for elements that display dynamic data (like stock prices), as these values are subject to change and can cause test failures.

- ✅ PREFERRED: DO use more resilient locators, such as data attributes or partial text matches, combined with appropriate waiting strategies, to interact with dynamic elements.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for dynamic content like stock prices; the values change frequently, making the test brittle.

- ✅ PREFERRED: DO use more robust locators, such as data attributes or CSS selectors that are less susceptible to changes in text content. Consider using a more generic locator and then filtering by text if necessary.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for elements that are likely to change frequently, such as stock prices.

- ✅ PREFERRED: DO use more robust locators, such as data attributes or CSS selectors, that are less susceptible to changes in dynamic content.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for dynamically updated elements like stock prices. The values change frequently, making the test brittle.

- ✅ PREFERRED: DO use more robust locators, such as data attributes or CSS selectors that are less susceptible to changes in text content. Consider using a more generic locator and then filtering by a stable attribute.

- ⚠️ PROHIBITED: DON'T rely on exact text matches for elements that are likely to change frequently (e.g., stock prices).

- ✅ PREFERRED: DO use more robust and less volatile locators, such as data attributes or ARIA labels, whenever possible. If text is necessary, use partial matches or regular expressions to account for slight variations.

- ✅ PREFERRED: DO use more robust locators, such as data attributes or stable CSS classes, to identify elements that display dynamic data. If exact text matching is necessary, consider using regular expressions to account for slight variations.

- ✅ PREFERRED: DO use more robust and less volatile locators, such as data attributes or ARIA labels, combined with partial text matching or regular expressions for dynamic content.
