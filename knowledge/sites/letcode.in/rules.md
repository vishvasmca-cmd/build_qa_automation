
- ⚠️ PROHIBITED: DON'T pass string values directly to Playwright's `expect()` assertion. ALWAYS use a Locator object to target the element you want to assert against.

- ✅ PREFERRED: DO use Playwright's `locator()` to get the element, then use `expect(locator).to_have_value(expected_value)` or `expect(locator).to_have_text(expected_text)` for assertions.
