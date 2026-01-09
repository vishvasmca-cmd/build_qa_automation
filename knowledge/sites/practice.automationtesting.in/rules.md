
- ⚠️ PROHIBITED: DON'T use boolean return values from page object methods directly within Playwright's `expect` assertions. `expect` needs a Locator object.

- ✅ PREFERRED: DO ensure that page object methods intended for visibility assertions return a Playwright Locator object representing the element to be checked. Use `locator(<locator>).is_visible()` inside the page object method.
