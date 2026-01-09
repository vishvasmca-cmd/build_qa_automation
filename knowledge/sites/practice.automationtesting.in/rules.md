
- ⚠️ PROHIBITED: DON'T use boolean return values from page object methods directly within Playwright's `expect` assertions. `expect` needs a Locator object.

- ✅ PREFERRED: DO ensure that page object methods intended for visibility assertions return a Playwright Locator object representing the element to be checked. Use `locator(<locator>).is_visible()` inside the page object method.

- ⚠️ PROHIBITED: DON'T assume the `.woocommerce-message` element is always present or immediately visible after registration. Verify the registration process and consider alternative success indicators.

- ✅ PREFERRED: DO implement robust error handling and logging during the registration process to identify potential failures. Use explicit waits with appropriate timeouts to ensure elements are fully rendered before assertions.

- ⚠️ PROHIBITED: DON'T directly assert `to_contain` on `page.url`. Use `page.locator` to create a locator for the URL.

- ✅ PREFERRED: DO use `expect(page).to_have_url` or `expect(page.locator('body')).to_have_text` to validate the URL or content after a redirect.

- ⚠️ PROHIBITED: DON'T directly assert on `page.url` using `to_contain`. Use `page.locator('body').locator('xpath=//desired-element').textContent()` to get the text content and then assert.

- ✅ PREFERRED: DO use `expect(page).to_have_url()` or `expect(page.locator('body')).to_have_text()` to assert on URL or page content respectively.
