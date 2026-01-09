
- ⚠️ PROHIBITED: DON'T use boolean return values from page object methods directly within Playwright's `expect` assertions. `expect` needs a Locator object.

- ✅ PREFERRED: DO ensure that page object methods intended for visibility assertions return a Playwright Locator object representing the element to be checked. Use `locator(<locator>).is_visible()` inside the page object method.

- ⚠️ PROHIBITED: DON'T assume the `.woocommerce-message` element is always present or immediately visible after registration. Verify the registration process and consider alternative success indicators.

- ✅ PREFERRED: DO implement robust error handling and logging during the registration process to identify potential failures. Use explicit waits with appropriate timeouts to ensure elements are fully rendered before assertions.

- ⚠️ PROHIBITED: DON'T directly assert `to_contain` on `page.url`. Use `page.locator` to create a locator for the URL.

- ✅ PREFERRED: DO use `expect(page).to_have_url` or `expect(page.locator('body')).to_have_text` to validate the URL or content after a redirect.

- ⚠️ PROHIBITED: DON'T directly assert on `page.url` using `to_contain`. Use `page.locator('body').locator('xpath=//desired-element').textContent()` to get the text content and then assert.

- ✅ PREFERRED: DO use `expect(page).to_have_url()` or `expect(page.locator('body')).to_have_text()` to assert on URL or page content respectively.

- ⚠️ PROHIBITED: DON'T assume successful registration without explicitly verifying the absence of error messages and the presence of success indicators (e.g., successful login, account dashboard).

- ✅ PREFERRED: DO implement robust error handling and validation after registration, including checking for specific error messages and verifying successful account creation through login or dashboard access.

- ⚠️ PROHIBITED: DON'T use `expect(True).to_be(False)` as a direct assertion. Instead, use Playwright's assertion methods on locators or page elements to verify the absence of error messages or the presence of expected elements after a successful registration.

- ✅ PREFERRED: DO use Playwright's `expect` function with locators or page elements to assert the expected state of the application after registration. For example, `expect(page.locator('#success-message')).to_be_visible()`.

- ⚠️ PROHIBITED: DON'T assume successful registration without verifying the absence of error messages and/or presence of success indicators.

- ✅ PREFERRED: DO implement robust error handling and validation to accurately determine the success or failure of critical operations like user registration.

- ⚠️ PROHIBITED: DON'T use a hardcoded email address for registration tests without implementing a mechanism to ensure uniqueness (e.g., generating a random email).

- ✅ PREFERRED: DO generate a unique email address for each registration test to avoid conflicts with existing accounts.

- ⚠️ PROHIBITED: DON'T use a hardcoded email address for registration tests without implementing a mechanism to ensure uniqueness or cleanup existing accounts.

- ✅ PREFERRED: DO implement a strategy for generating unique email addresses for registration tests, such as using a timestamp or a random string, or implement a cleanup process to delete existing accounts before running the test.

- ⚠️ PROHIBITED: DON'T use a hardcoded email address for registration tests without implementing a mechanism to generate unique email addresses for each test run or cleaning up the test data.

- ✅ PREFERRED: DO implement a mechanism to generate unique email addresses for registration tests, such as using a timestamp or a random string appended to a base email address, or implement a cleanup process to delete the test account after the test run.

- ⚠️ PROHIBITED: DON'T use hardcoded email addresses for registration tests without implementing a mechanism to generate unique email addresses for each test run.

- ✅ PREFERRED: DO implement a mechanism to generate unique email addresses for registration tests, such as using a timestamp or a random string appended to a base email address.
