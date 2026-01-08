
- Before filling the username field, ensure the page is fully loaded and the username input field is visible and enabled. Consider adding a wait_for_selector before attempting to fill the field.

- Before interacting with elements in the footer (like the 'OrangeHRM, Inc' link), ensure any overlaying elements or animations have completed to prevent click interception or unexpected behavior.

- Before clicking 'Forgot your password?', ensure the element is visible and stable. Consider waiting for network activity to settle or for a specific element to load before attempting to click.

- When clicking the 'OrangeHRM, Inc' link, implement a retry mechanism with a short delay between attempts, as the element might become momentarily unresponsive despite appearing stable.

- Before attempting to click 'Forgot your password', ensure that any overlaying elements (e.g., modals, banners) are dismissed or that the element is fully visible and interactable. Consider adding a short explicit wait for the element to be visible and enabled.

- If a link is visible, enabled and stable but click action times out, try to use JavaScript click or force click.

- When navigating to the password reset page, implement a retry mechanism with exponential backoff to handle potential slow server responses or intermittent network issues. Also, verify that the password reset link is correctly configured and reachable.

- Before interacting with elements in the top navigation bar, ensure the page has fully loaded and any initial animations or transitions have completed. Consider using `locator.wait_for()` with `state='visible'` or `state='stable'` before attempting to click.

- When interacting with elements in the OrangeHRM header, especially navigation links, implement retry logic with exponential backoff to handle potential intermittent loading issues or animations that might delay element availability. Consider using more robust locators than full XPaths.

- When navigating to the login page, implement a retry mechanism with exponential backoff to handle potential network or server delays. Also, verify the page content instead of relying solely on URL matching, as redirects might occur.

- Before clicking 'Forgot your password?', ensure no overlays or modals are present that might obscure the element or prevent it from being interacted with. Check for dynamic content loading that might delay the appearance of the element.

- Before clicking 'Forgot your password?', ensure no modal dialogs or overlays are present that might obscure the element. Also, consider adding a short wait or retry mechanism specifically for this element.

- Before attempting to click 'Forgot your password?', ensure the element is both visible and enabled. Consider adding a short explicit wait with error handling.

- When asserting URL changes after an action, use a precise and complete URL string or a more accurate regular expression to avoid false negatives due to minor URL variations.

- When navigating to the password reset page, anticipate potential delays in network activity and consider increasing the default timeout or explicitly waiting for a specific element to load before proceeding.

- When navigating to the password reset page, anticipate potential delays in resource loading. Increase the default timeout or implement a more robust loading check than 'networkidle', such as waiting for a specific element to be present.

- Before clicking 'Forgot your password', ensure no modal dialogs or overlays are present that might obscure the link. If a modal is present, dismiss it before proceeding.

- Before clicking the 'Forgot your password' link, ensure no modal dialogs or overlays are present that might obscure the element. If a modal is present, dismiss it before attempting to click the link.

- When asserting URL patterns, ensure the pattern accurately reflects the expected URL structure, including any prefixes or suffixes. Prefer exact match when possible.

- When asserting the current URL, prefer exact string matching or a more specific regex over glob patterns, especially when the expected substring is present in the actual URL.

- Before filling the username field on the OrangeHRM login page, ensure the page is fully loaded and the username field is visible. Consider adding a wait_for_selector or wait_for_load_state before attempting to fill the field.

- After submitting a password reset request, verify that the application redirects to a confirmation page or displays a success message before redirecting to the login page. Do not immediately expect a redirect to the login page.

- After submitting a password reset request, always check for the success message on the same page before assuming a redirect or further action is needed.

- After submitting a password reset request, explicitly wait for the 'Reset Password link sent successfully' message to appear before proceeding with assertions.  Consider using a longer timeout or a more robust locator strategy.

- When navigating to the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- When navigating to a new page, especially the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- When navigating to a new page, especially the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- Before attempting to fill the 'Username' field, explicitly wait for the form or relevant section to be fully loaded. Consider using a more robust locator strategy if labels are unreliable.

- When navigating to the OrangeHRM login page, implement a retry mechanism with exponential backoff to handle potential delays in redirection. Also, check for common blocking elements like modals or banners before waiting for the URL.

- When navigating to a new page, especially the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- When navigating to an external URL, implement a retry mechanism with exponential backoff to handle potential network instability or temporary website unavailability. Also, verify the target URL before navigation.

- When interacting with elements in the top navigation bar of OrangeHRM, implement a retry mechanism with exponential backoff to handle potential loading delays or intermittent visibility issues. Before clicking, explicitly wait for the element to be both visible and enabled.

- When clicking on elements within the OrangeHRM header/navigation, implement a retry mechanism with exponential backoff, as network conditions or server-side processing might cause intermittent delays. Also, consider using more resilient locators based on text content or ARIA roles instead of brittle XPaths.

- When asserting the presence of text on a page in Playwright, use `expect(page.locator('body')).to_have_text('expected text')` or `expect(page.locator('selector')).to_have_text('expected text')` instead of `expect(page).to_have_text('expected text')`.

- When asserting the success message after a password reset request, use a more specific locator to target the message element, avoiding the surrounding HTML structure.

- When asserting the presence of specific text after an action that triggers a page update (like submitting a password reset request), target a more specific locator than the entire 'body' to avoid interference from surrounding HTML and whitespace. Also, trim the actual value before comparison.

- Before attempting to fill the username field, ensure the page is fully loaded and the username field is visible and enabled. Consider adding a wait_for_selector or wait_for_load_state before filling the field.

- ALWAYS avoid clicking the OrangeHRM logo (usually top left or brand logo), as it redirects to the external marketing website 'www.orangehrm.com', which is outside our test scope. Focus only on internal application navigation.

- Ensure all modules and dependencies are correctly installed and that import paths are accurate before running tests. Verify the existence and location of the 'projects.core_orangehrm.utils' module.

- ⚠️ PROHIBITED: DON'T assume a specific URL after login; instead, verify the presence of key elements on the target page (e.g., dashboard widgets or employee list table) to ensure successful login and navigation.

- ✅ PREFERRED: DO verify the successful login by checking for the visibility of unique dashboard elements (e.g., a specific dashboard widget) or elements on the employee list page instead of relying solely on URL matching.

- ⚠️ PROHIBITED: DON'T assume a successful login will always redirect to the employee list page.  ALWAYS verify the presence of key elements on the expected page after navigation.

- ✅ PREFERRED: DO add a more robust check after login, such as verifying the visibility of specific elements on the employee list page, to confirm successful redirection and login flow before proceeding with the test.

- ⚠️ PROHIBITED: DON'T assume that module paths are correct without verifying the project's directory structure and relative imports.

- ✅ PREFERRED: ALWAYS double-check module import paths in test files to ensure they accurately reflect the project's file structure and that all necessary modules are installed and accessible.

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the Python environment's PYTHONPATH or project structure.

- ✅ PREFERRED: DO ensure that the PYTHONPATH is correctly configured or that relative imports are properly handled within the project structure to resolve ModuleNotFoundError exceptions.

- ⚠️ PROHIBITED: DON'T assume the correct project structure. ALWAYS verify that the paths to your modules are correct, considering the project's root directory.

- ✅ PREFERRED: DO use relative imports or configure your Python environment (e.g., PYTHONPATH) to ensure that modules can be located correctly, and verify the path to your modules.

- ⚠️ PROHIBITED: DON'T assume that the Python import paths are correctly configured; ALWAYS verify the project structure and relative paths when importing modules.

- ✅ PREFERRED: DO explicitly define and check the PYTHONPATH environment variable to ensure that the necessary directories are included for module resolution.

- ⚠️ PROHIBITED: DON'T directly pass a string representing the URL to Playwright's `expect` function for assertions. ALWAYS pass the Playwright Page object.

- ✅ PREFERRED: DO use `expect(page).to_have_url` or `expect(page).to_have_url(containing=...)` to validate the page URL after navigation.

- ⚠️ PROHIBITED: DON'T use regex literals (e.g., `/dashboard/`) directly within Playwright's `to_have_url` method. Use a string or a compiled regular expression object instead.

- ✅ PREFERRED: DO use a string or a compiled regular expression object with the `to_have_url` method, e.g., `expect(page).to_have_url('dashboard')` or `expect(page).to_have_url(re.compile(r'dashboard'))`.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` with regex for critical input fields like 'Username', as subtle UI changes or internationalization differences can easily break the locator.

- ✅ PREFERRED: DO use a more robust locator strategy, such as combining `get_by_placeholder` with `get_by_text` on a parent element or using a data attribute if available, to improve the stability and accuracy of finding the 'Username' field.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` for critical input fields without verifying its stability and considering potential UI changes or dynamic loading issues.

- ✅ PREFERRED: DO implement retry mechanisms or explicit waits (e.g., `wait_for_selector`, `wait_for_function`) before attempting to interact with input fields, especially after page loads or navigation events.

- ⚠️ PROHIBITED: DON'T assume the login page elements are immediately available. ALWAYS implement a retry or explicit wait strategy before interacting with login form elements.

- ✅ PREFERRED: DO implement retry-ability or an explicit wait with error handling when interacting with input fields, especially on initial page loads. Use visibility checks or other element state verifications to ensure the element is ready for interaction.

- ⚠️ PROHIBITED: DON'T assume the login form is immediately available after page load. ALWAYS wait for the presence of the 'Username' field or a similar key element of the login form before attempting to interact with it.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` for the login form's key elements (e.g., Username field) BEFORE attempting to fill them. This ensures the elements are fully loaded and ready for interaction.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` with regular expressions for critical input fields without verifying the element's visibility and readiness for input.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the target element is both visible and enabled before attempting to interact with it (e.g., `wait_for` or `expect`).

- ⚠️ PROHIBITED: DON'T assume immediate redirection after clicking 'Save' on the Add Employee page; always verify the URL or page content to confirm successful navigation.

- ✅ PREFERRED: DO implement explicit waits or assertions for the expected page content (e.g., a specific element on the employee list page) after saving an employee, rather than relying solely on URL matching.

- ⚠️ PROHIBITED: DON'T assume a direct return to the Employee List page after saving a new employee. The application may redirect to the Employee Personal Details page instead.

- ✅ PREFERRED: DO verify the navigation flow after saving a new employee. Use specific locators on the expected resulting page (Employee Personal Details or Employee List) to confirm successful navigation.

- ⚠️ PROHIBITED: DON'T assume a direct return to the employee list page after saving a new employee. The application might redirect to the employee's personal details page.

- ✅ PREFERRED: DO verify the successful creation of the employee by either checking for a success message on the personal details page or navigating back to the employee list and verifying the employee's presence.

- ⚠️ PROHIBITED: DON'T rely on default timeouts when filling critical fields; explicit waits are necessary.

- ✅ PREFERRED: DO implement a retry-mechanism or adjust timeout settings depending on the observed speed of the webpage loading.

- ⚠️ PROHIBITED: DON'T assume the test file path is correct without verifying its existence in the file system or project structure.

- ✅ PREFERRED: DO double-check the test file path specified in the test execution command or configuration to ensure it matches the actual location of the test file within the project.

- ⚠️ PROHIBITED: DON'T rely solely on label-based locators for input fields without ensuring the element is visible and stable. Specifically, NEVER assume the 'Username' field is immediately available after page load.

- ✅ PREFERRED: DO implement explicit waits (e.g., `page.wait_for_selector()`) or retry mechanisms with short intervals before attempting to interact with critical elements like login fields. ALWAYS verify the test file path before execution to prevent 'file not found' errors.

- ⚠️ PROHIBITED: DON'T assume a successful login and immediate dashboard navigation. ALWAYS add explicit checks for successful login before proceeding with dashboard actions.

- ✅ PREFERRED: DO verify the presence of a unique dashboard element after login, using a reasonable timeout (e.g., 10 seconds) before proceeding with further steps.

- ⚠️ PROHIBITED: DON'T rely on exact URL matches for navigation assertions immediately after login; the trailing `/index` might or might not be present.

- ✅ PREFERRED: DO use a more flexible URL matching strategy (e.g., `**/web/index.php/dashboard*`) or verify the presence of a specific element on the dashboard page to confirm successful login instead of exact url.

- ⚠️ PROHIBITED: DON'T assume that the PYTHONPATH or project structure is correctly configured; ALWAYS verify module import paths before running tests, especially after project restructuring or environment changes.

- ✅ PREFERRED: DO use absolute imports or relative imports with explicit `.` (e.g., `from .pages.dashboard_page import OrangehrmDashboardPage`) to ensure correct module resolution, especially within complex project structures.
- ALWAYS use flexible URL matching (wildcards like `**/dashboard*` or regex `re.compile(r"dashboard")`) when asserting the dashboard page, as it may appear as `/dashboard` or `/dashboard/index`.

- After clicking 'Save' on the Add Employee page, SUCCESS is defined by the appearance of the 'Personal Details' page or a success toast. Do NOT mark global goal as achieved until you move to the 'Admin' module if required by the mission.

- ⚠️ PROHIBITED: DON'T use `page.get_by_locator()` assuming it's a valid Playwright API method. Always refer to the official Playwright documentation for the correct API usage.

- ✅ PREFERRED: ALWAYS use `page.locator('<your locator>')` to create a locator object before performing actions like `fill()`, `click()`, etc.

- ⚠️ PROHIBITED: DON'T assume the OrangeHRM application is immediately responsive. ALWAYS implement retry mechanisms or increase the default timeout for initial page loads, especially after deployments or during peak hours.

- ✅ PREFERRED: DO implement a health check or status check against the target URL (https://opensource-demo.orangehrmlive.com/) BEFORE running tests to ensure the application is reachable and responsive.

- ⚠️ PROHIBITED: DON'T assume the OrangeHRM login page will load within the default 30-second timeout, especially in environments with variable network conditions.

- ✅ PREFERRED: DO implement a retry mechanism or increase the timeout for the page.goto() call when navigating to the OrangeHRM login page.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` without ensuring the element is visible and stable, especially for critical input fields like username/password during login.

- ✅ PREFERRED: DO implement explicit waits with `locator.wait_for()` before interacting with elements, especially after page navigations or form submissions. Consider using `locator.is_visible()` as a condition.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available. ALWAYS implement a retry or conditional wait before attempting to fill it.

- ✅ PREFERRED: DO use `await expect(page.locator('locator')).to_be_visible()` to assert the visibility of the username input field before attempting to fill it.

- ⚠️ PROHIBITED: DON'T assume the test file path is correct without verifying its existence in the file system before running the tests.

- ✅ PREFERRED: DO ensure the test file path is correctly specified and that the test file exists in the file system before initiating test execution.

- ⚠️ PROHIBITED: DON'T assume the test file path is correct without verifying its existence in the file system before running the tests.

- ✅ PREFERRED: DO double-check the test file path and ensure it exists in the specified location before triggering the test execution.

- ⚠️ PROHIBITED: DON'T assume the test file path is correct without verifying its existence in the file system or project structure.

- ✅ PREFERRED: DO double-check and validate the test file path before running the pytest command. Ensure the file exists and the path is relative to the root directory where pytest is executed.

- ⚠️ PROHIBITED: DON'T assume the test file path is correct without verifying its existence in the file system relative to the project root.

- ✅ PREFERRED: ALWAYS double-check and confirm the test file path and ensure it is correctly specified in the pytest command or configuration.

- ⚠️ PROHIBITED: DON'T rely solely on label-based locators for critical input fields like Username without verifying label accuracy and stability. Labels can be easily changed, leading to test failures.

- ✅ PREFERRED: DO prioritize using a combination of locators for important elements, such as ID, data-testid, or a more specific CSS selector, along with the label, to increase resilience to UI changes. Verify the target field is visible before filling.

- ⚠️ PROHIBITED: DON'T assume that the project's folder structure is correctly mirrored in the Python import statements; ALWAYS verify the relative paths.

- ✅ PREFERRED: DO double-check the file paths and module names in import statements to ensure they accurately reflect the project's directory structure and file names.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import ...`) in test files unless the test suite is explicitly designed and executed as a Python package with a defined package structure.

- ✅ PREFERRED: DO ensure that test files are organized within a well-defined package structure, or use absolute imports (e.g., `from projects.orangehrm_enterprise.base_page import BasePage`) when importing modules within the project.

- ⚠️ PROHIBITED: DON'T assume all page objects are available in a test without explicitly importing or defining them.

- ✅ PREFERRED: ALWAYS verify that all required page objects or modules are imported or defined before attempting to use them in a test.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a generic name like 'Add', as it can lead to ambiguity if multiple elements match that description. AVOID directly clicking without visibility check and appropriate waiting.

- ✅ PREFERRED: DO prioritize using more specific and resilient locators, such as `data-testid` attributes, or combine role-based locators with other attributes or parent element constraints to pinpoint the target element. ALWAYS implement a visibility check before attempting to click.

- ⚠️ PROHIBITED: DON'T rely on `filter(has_text)` alone when multiple elements with the same text content are present. Ensure locators are uniquely identifiable.

- ✅ PREFERRED: DO use more specific attributes or chained locators to target the desired element when `filter(has_text)` is not unique. Leverage data attributes or unique class names if available.

- ⚠️ PROHIBITED: DON'T rely on hovering to trigger navigation, especially in dynamic sidebars. Hovering is less reliable than direct clicks.

- ✅ PREFERRED: DO use explicit `wait_for_selector` with increased timeout and visibility check BEFORE attempting to hover or click on elements within dynamic sections like side panels. ALWAYS consider using alternative navigation methods like `goto` if possible.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` with a regular expression for critical input fields like Username, especially without confirming element visibility or presence.

- ✅ PREFERRED: DO prioritize using more specific and stable locators, such as `input[name='username']` or `input#username`, and ALWAYS verify element visibility before interacting with it.

- ⚠️ PROHIBITED: DON'T assume a successful login without explicitly verifying the presence of a dashboard element after navigation.

- ✅ PREFERRED: DO implement explicit waits for key dashboard elements to appear after the expected navigation, ensuring the application has fully loaded before proceeding with subsequent actions.

- ⚠️ PROHIBITED: DON'T directly access internal attributes like `_selector` of Playwright Locator objects. Use the public API methods instead.

- ✅ PREFERRED: DO use `page.locator('your_selector').first().wait_for()` or `page.locator('your_selector').wait_for()` to wait for an element to be present and visible before interacting with it.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the existence of necessary modules and their correct import paths.

- ✅ PREFERRED: DO verify the project's directory structure and module import paths before running tests, especially after any changes to the project structure.

- ⚠️ PROHIBITED: DON'T use raw strings without quotes in `to_have_url` assertions. ALWAYS enclose the expected URL in single or double quotes.

- ✅ PREFERRED: DO use quoted strings when asserting the URL with `to_have_url`. For example, `expect(page).to_have_url('/dashboard')`.

- ⚠️ PROHIBITED: DON'T assume that the project structure and import paths are correct without verifying them, especially after code changes or when setting up a new environment.

- ✅ PREFERRED: DO double-check the project's directory structure and import paths to ensure that all modules are accessible and correctly referenced in the test files.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` with a regex for critical input fields without first verifying the label's presence and uniqueness on the page.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the target element is visible and interactable before attempting to fill it. Consider using `locator.wait_for()` with `state='visible'`.

- ⚠️ PROHIBITED: DON'T use locators that are ambiguous and can match multiple elements on the page without specifying which element is intended.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators or locators that include attributes, to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test runner is explicitly configured to treat the test directory as a package.

- ✅ PREFERRED: DO use absolute imports or configure the test runner (e.g., pytest) to recognize the test directory as a package by including an `__init__.py` file in the directory and any parent directories that should be considered part of the package.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the existence and accessibility of all necessary modules and packages.

- ✅ PREFERRED: DO ensure that all modules and packages are correctly placed within the project directory and that Python's import paths are configured to include the project's root directory.

- ⚠️ PROHIBITED: DON'T assume that the project structure and import paths are correct without verifying them, especially after code changes or when setting up a new environment.

- ✅ PREFERRED: DO double-check the project's directory structure and import paths to ensure that all modules are accessible and correctly referenced in the test files.

- ⚠️ PROHIBITED: DON'T use locators that are not specific enough and can match multiple elements on the page. ALWAYS aim for unique and unambiguous locators.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators (e.g., `get_by_role('button', name='Login')`) or locators that include attributes to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T rely solely on text-based locators without considering potential variations in text or the presence of multiple elements with the same text. DON'T assume elements are immediately clickable after page load; always account for potential delays in rendering or enabling.

- ✅ PREFERRED: DO use more robust locators like role-based or ID-based locators whenever possible. DO implement explicit waits with error handling to ensure elements are both present and clickable before attempting to interact with them. DO consider using visual validation to confirm the element is rendered as expected.

- ⚠️ PROHIBITED: DON'T use locators that are not specific enough and can match multiple elements on the page. ALWAYS aim for unique and unambiguous locators.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators (e.g., `get_by_role('button', name='Login')`) or locators that include attributes to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T use ambiguous locators like `text=Add` without ensuring they uniquely identify the target element.  Always validate locator uniqueness before performing actions.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators (e.g., `get_by_role`) or locators combined with `nth()` or `first()`/`last()` to target the intended element when multiple elements match the initial locator.

- ⚠️ PROHIBITED: DON'T use locators that are not specific enough and can match multiple elements on the page without explicitly targeting the desired element.

- ✅ PREFERRED: DO use more specific locators, such as `getByRole('button', { name: 'Login' })` or `locator('button:has-text("Login")')`, to uniquely identify the intended element.

- ⚠️ PROHIBITED: DON'T use locators that are ambiguous and can match multiple elements, especially when performing actions like clicking. ALWAYS ensure locators are specific enough to target a single, unique element.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators (e.g., `get_by_role('button', name='Login')`) or locators that include attributes (e.g., `locator('button.orangehrm-login-button', name='Login')`), to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after navigation; always implement explicit waits for critical elements to appear.

- ✅ PREFERRED: DO verify successful navigation by checking for a unique element on the target page before interacting with other elements.

- ⚠️ PROHIBITED: DON'T use locators that are ambiguous and can match multiple elements on the page without providing additional specificity.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators (e.g., `get_by_role('button', name='Login')`) or locators that include unique attributes, to target the intended element.

- ⚠️ PROHIBITED: DON'T assume that navigation is complete immediately after a click. ALWAYS wait for the target element to be visible or the expected URL to be reached before proceeding.

- ✅ PREFERRED: DO use `page.wait_for_load_state('networkidle')` or `page.wait_for_url()` after navigation to ensure the page is fully loaded before interacting with elements.

- ⚠️ PROHIBITED: DON'T use locators that are ambiguous and can match multiple elements on the page without providing additional specificity.

- ✅ PREFERRED: DO use more specific locators, such as role-based locators (e.g., `getByRole('button', { name: 'Login' })`) or locators that include attributes or unique identifiers, to target the intended element precisely.

- ⚠️ PROHIBITED: DON'T use regular expression quantifiers (e.g., *, +, ?) in Playwright locators without ensuring there is a preceding element to apply the quantifier to.  Carefully validate the regex syntax.

- ✅ PREFERRED: DO thoroughly validate regular expressions used in Playwright locators, especially when using quantifiers. Use online regex testers or debugging tools to confirm the regex matches the intended elements before incorporating it into the test.

- ⚠️ PROHIBITED: DON'T embed Playwright locators (like `get_by_role`) directly within CSS selector strings. Use them as standalone locators.

- ✅ PREFERRED: DO define Playwright locators separately and then use them in actions like `click()` or `fill()`.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_label` with regex for critical input fields without verifying its robustness across different page states and potential A/B tests.

- ✅ PREFERRED: DO implement explicit waits or retries with more specific locators (e.g., `input[name='username']` or `input#username`) when filling critical form fields, especially after page loads or transitions.

- ⚠️ PROHIBITED: DON'T pass the URL string directly to `expect(page.url).to_contain()`. The `expect` function requires a Playwright `Page` object.

- ✅ PREFERRED: DO use `expect(page).to_have_url()` or `expect(page).to_have_url(containing=...)` to assert the URL after navigation.

- ⚠️ PROHIBITED: DON'T assume the URL after login will always be exactly '**/dashboard'; the application might redirect to a more specific dashboard URL.

- ✅ PREFERRED: DO use a more robust URL validation, such as checking if the URL *contains* '/dashboard' or using a regular expression to match the expected pattern.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when the locator string contains references to variables (like `page`) that are not available in the evaluation context. This leads to unpredictable and hard-to-debug errors.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to dynamically construct them, ensuring that all necessary variables are properly scoped and available when the locator is used. Prefer using Playwright's built-in locator methods for dynamic selection.

- ⚠️ PROHIBITED: DON'T use `eval()` to construct locators, especially when they depend on variables defined outside the string. This makes debugging difficult and introduces security risks.

- ✅ PREFERRED: DO use f-strings or other string formatting methods to dynamically construct locators, ensuring that variables are properly scoped and accessible.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when trying to reference page-specific objects. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators as simple, static strings or use parameterized locators with proper string formatting or f-strings to inject dynamic values. Ensure all necessary objects are accessible within the scope where the locator is being used.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators that depend on the `page` object's context. `eval()` can lead to scope issues and make debugging difficult.

- ✅ PREFERRED: DO pass the `page` object directly to the locator or use string formatting to construct the locator string with the `page` object's properties.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings to reference page-specific objects. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators as simple, static strings or use parameterized locators with proper string formatting to inject dynamic values. Pass the `page` object directly to the locator method.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when referencing page-specific objects. This creates brittle and hard-to-debug locators.

- ✅ PREFERRED: DO define locators as static strings or use string formatting to inject variables if needed. Pass the `page` object directly to the locator method if dynamic context is required.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when attempting to reference page-specific objects like `page`. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators using static strings or f-strings that incorporate class attributes or configuration values. If dynamic behavior is needed, manipulate the locator string outside of the locator definition itself.

- ⚠️ PROHIBITED: DON'T use `eval()` with unescaped variables from the test's scope within locator strings. This leads to `NameError` and makes the code difficult to debug.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to inject variables into the locator string before passing it to `page.locator()`.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when referencing page-specific objects within the locator string. This creates scope issues and makes debugging difficult.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to dynamically construct them using class attributes or constructor parameters, ensuring proper scope and avoiding `eval()`.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when trying to inject the `page` object directly into the locator string. This creates scope issues and is unnecessary.

- ✅ PREFERRED: DO define locators as static strings or use f-strings for dynamic parts, passing any required variables directly to the locator method (e.g., `page.locator(f'//button[@id="{button_id}"]')`).

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when attempting to reference page-specific objects like `page` itself. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators as simple, static strings or use parameterized locators with proper string formatting. Pass the `page` object to methods that interact with the page elements, and use it directly within those methods.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when attempting to reference page-specific objects. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators as simple, static strings or use parameterized locators with proper string formatting to inject dynamic values. Ensure locators are resilient to minor UI changes.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when referencing page-specific objects within the string. This creates scope issues and makes debugging difficult.

- ✅ PREFERRED: DO construct locators using f-strings or other string formatting methods to inject variables like `page` into the locator string *before* passing it to `page.locator()`. This ensures the variables are properly scoped.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when attempting to reference page-specific objects like `page`. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators as simple, static strings or use parameterized locators with proper string formatting or f-strings to inject dynamic values. Ensure all necessary variables are within the scope of the locator definition.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when the locator string contains references to page-specific objects. This creates scope issues and makes debugging difficult.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to dynamically construct them with variables passed directly to the locator method. This ensures proper scope and readability.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when trying to inject the `page` object. This creates scope issues and makes the locator brittle and hard to debug.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to format them with known variables at definition time. If dynamic behavior is needed, use Playwright's built-in locator methods like `locator.filter()` or `locator.locator()` to refine the locator based on runtime conditions.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when the locator string contains references to page-specific objects. This creates scope issues and makes debugging difficult.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to dynamically construct them using variables available in the current scope. This ensures proper variable resolution and avoids runtime errors.

- ⚠️ PROHIBITED: DON'T use `eval()` to construct Playwright locators, especially when referencing page-specific objects within the locator string. This leads to scope issues and makes debugging difficult.

- ✅ PREFERRED: DO define locators as static strings or use f-strings for dynamic parts, passing any required page-specific objects as arguments to the locator method.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when attempting to reference page-specific objects like `page` itself. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators using static strings or f-strings that incorporate class attributes or configuration values. If dynamic behavior is needed, manipulate the locator string outside of the locator definition itself.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when trying to inject the `page` object directly into the locator string. This creates scope issues and is unnecessary.

- ✅ PREFERRED: DO define locators as static strings or use f-strings for dynamic parts, passing any required variables explicitly. Use Playwright's built-in locator methods for dynamic selection.

- ⚠️ PROHIBITED: DON'T use `eval()` with Playwright locators, especially when the locator string contains references to page-specific objects. This creates scope issues and makes debugging difficult.

- ✅ PREFERRED: DO define locators as static strings or use f-strings to dynamically construct them with variables available in the current scope.  Ensure locators are robust and avoid relying on fragile text-based selectors.

- ⚠️ PROHIBITED: DON'T use `eval()` within locator strings, especially when referencing page-specific objects like `page`. This creates scope issues and makes locators brittle and hard to maintain.

- ✅ PREFERRED: DO define locators using static strings or f-strings that incorporate class attributes or configuration values. If dynamic behavior is needed, manipulate the locator string outside of the locator definition itself.
