# Parabank Specific Rules

## Navigation & Strict Mode
- **STRICT MODE VIOLATION**: Common links like "About Us", "Services", "Admin Page" appear in both the Header and Footer.
  - **ACTION**: When clicking these common links, ALWAYS clarify the container or use `.first`.
  - **PREFERRED**: `page.locator("#headerPanel").get_by_role("link", name="About Us")`
  - **ALTERNATIVE**: `page.get_by_role("link", name="About Us").first`

- **HOME LINK**: "Home" link also appears multiple times. Use `exact=True` or header scope.
  - **PREFERRED**: `page.get_by_role("link", name="Home", exact=True).first`

## Login
- **LOGIN SUCCESS**: Successful login redirects to `/parabank/overview.htm`.
- **REGISTRATION SIDE EFFECT**: After successful registration, the user is AUTOMATICALLY logged in. Do NOT attempt to login again immediately after registration. Verify login by checking for "Welcome [Username]" or the "Log Out" button.
- **LOGIN FAILURE**: Failure usually keeps you on `index.htm` or shows specific error text "The username and password could not be verified".

## Account History & Server Stability
- **WADL REDIRECT**: Clicking "Account History" sometimes redirects to a WADL/Service description page instead of `/account.htm`.
  - **ACTION**: Verify URL contains `/account.htm` (or `/accountactivity.htm`). If it contains `_wadl` or ends in `.xml`, it is a server-side error.
  - **RECOVERY**: Implement retry mechanism with page refresh if WADL page is encountered.

- **URL VERIFICATION**: Ensure `expect(page).to_have_url()` regex is strictly formatted to avoid partial matches on wrong pages.

- When targeting elements that may appear in both the header and footer, use more specific locators to avoid ambiguity.  Prioritize locators scoped to a specific container (e.g., header or footer) or use nth=0/1 to target the correct element.

- Before clicking 'Account History', ensure the user is logged in and the account summary page is fully loaded. Implement a visual check or state check to confirm readiness.

- When using `to_have_url` with a regular expression, ensure the regex is a properly formatted string.

- When navigating to account history, implement a retry mechanism with exponential backoff to handle potential slow server responses or intermittent network issues. Also, verify the user is logged in before attempting to navigate to the account history page.

- When navigating to account details, implement a retry mechanism with exponential backoff if the initial navigation times out. Also, verify the user is logged in before attempting to access account details.

- When navigating to account history, check for common error messages or loading indicators on the page before waiting for the final URL. The ParaBank application is known to have intermittent performance issues.

- After clicking 'Account History', check for a redirect to the API endpoint '/services/bank' and, if present, retry the click or report the error.

- Before navigating to 'Account History', ensure all page elements are fully loaded and any potential overlays or animations are complete. Consider adding a short explicit wait if necessary.

- Before navigating to 'Account History', ensure all page elements are fully loaded and any potential overlays or animations are complete. Consider adding a short delay or explicit wait condition.

- If navigation to Account History results in a redirect to '/services/bank', retry the navigation after a short delay, as this might be a transient server-side issue. Consider adding a conditional check for this redirect.

- When navigating to the ParaBank homepage, the 'Home' link may not be immediately available. Implement a retry mechanism or increase the timeout to accommodate potential delays.

- When using `get_by_role` with a regular expression for link names, especially with `re.IGNORECASE`, ensure the expression is specific enough to resolve to a single, unique element.  Consider using `exact=True` if the target link's capitalization is known and consistent, or refine the regex to be more precise.

- When locating elements with text that might have inconsistent casing, prefer exact matches or use `first` or `last` to disambiguate if multiple matches are expected.  Alternatively, disable strict mode only when necessary and with caution.

- When locating elements with text 'Home' (case-insensitive) on ParaBank, be aware that multiple elements may match. Use a more specific locator or consider using `first` or `last` to resolve ambiguity, or disable strict mode if appropriate.

- When navigating to account history, implement a retry mechanism with a short delay to handle potential intermittent server delays or network issues. Also, verify successful login before navigating.

- Before navigating to 'Account History', ensure that all loading elements or overlays are fully dismissed. Consider adding an explicit wait for the page to fully load before interacting with elements.

- Before clicking 'Account History', ensure the page is fully loaded and any overlays or animations are complete. Consider adding a short explicit wait for the element to be visible and stable.

- Before navigating to 'Account History', check for any pop-up messages or redirects that might interfere with the intended navigation flow. If a redirect to the web service definition page is detected, retry the navigation after a short delay.

- Before navigating to 'Account History', ensure all page elements are fully loaded and any potential overlays or animations are complete. Consider adding a short explicit wait if necessary.

- Before navigating to 'Account History', ensure the main content area is fully loaded and any overlaying elements (e.g., advertisements or loading spinners) are dismissed. Consider adding a short explicit wait for the main content to stabilize.

- Before navigating to 'Account History', ensure the main content area is fully loaded and any overlaying elements (e.g., modals, banners) are dismissed. Consider adding an explicit wait for a key element in the main content area to be visible before attempting to click 'Account History'.

- When navigating to 'Account History' on ParaBank, implement a retry mechanism with a maximum of 3 attempts.  If a WADL or XML redirect is detected during navigation, reload the page before retrying.  If navigation consistently fails after multiple retries, it indicates a potential server-side issue or a more persistent redirect problem.

- Ensure the correct project structure and module paths are used when importing modules within the project. Verify that the `PYTHONPATH` environment variable is correctly configured if the module is not in the standard library or a site-packages directory.

- ⚠️ PROHIBITED: DON'T assume that helper modules are automatically available; ALWAYS verify the module path is correct and the module exists.

- ✅ PREFERRED: DO ensure that all dependencies, including helper modules, are installed and accessible within the test environment before running tests. Verify the correct relative or absolute path is used for importing modules.

- ⚠️ PROHIBITED: DON'T assume that helper modules are automatically available; ALWAYS verify their presence and correct path within the project structure.

- ✅ PREFERRED: DO ensure that all necessary modules, especially helper functions and custom libraries, are correctly placed within the project and that import paths are accurate before running tests.

- ⚠️ PROHIBITED: DON'T assume that helper modules are available without explicitly checking their presence and import path.

- ✅ PREFERRED: DO ensure all required modules and dependencies are correctly installed and the import paths are properly configured before running the tests.

- ⚠️ PROHIBITED: DON'T assume the navigation to registration page is immediate; always account for potential delays in network response or server processing.

- ✅ PREFERRED: DO use explicit waits with `page.locator('locator').click()` and `page.wait_for_url('**/register.htm')` to ensure the element is clickable and the page has loaded completely.

- ⚠️ PROHIBITED: DON'T assume that navigation is complete simply because 'load' or 'domcontentloaded' events have fired. Ensure all network activity has ceased when relying on page content loaded via asynchronous requests.

- ✅ PREFERRED: DO explicitly wait for key elements to appear on the page after navigation, rather than relying solely on load state events. This provides a more robust indication of page readiness.

- ⚠️ PROHIBITED: DON'T use a backslash to escape a literal '.' character in CSS ID selectors within playwright locators. The backslash is interpreted as an escape sequence, and the '.' is treated as a class selector instead of part of the ID.

- ✅ PREFERRED: DO use the correct CSS selector syntax. If the element ID contains a literal '.', ensure it is properly represented in the locator string, or use alternative locator strategies like data-testid attributes if available and more robust.

- ⚠️ PROHIBITED: DON'T escape special characters like '.' in CSS selectors (IDs or classes) unless they are truly meant to be escaped. Instead, use the correct CSS selector syntax or alternative locator strategies.

- ✅ PREFERRED: DO inspect the HTML source code carefully to determine the correct CSS selector or use alternative locator strategies like `data-testid` or `data-test-id` attributes when available, or use XPath if necessary.

- ⚠️ PROHIBITED: DON'T escape special characters (periods) in CSS selectors unless you are certain they are part of the literal ID or class name. Inspect the HTML source to confirm the correct ID.

- ✅ PREFERRED: ALWAYS use the correct CSS selector syntax for IDs (e.g., '#elementId') and ensure that special characters are handled correctly without unnecessary escaping. Prefer using exact text matches where possible to avoid issues with dynamic content.

- ⚠️ PROHIBITED: DON'T use a backslash to escape periods within a CSS ID selector. The period is already a literal character in this context. If the intention is to target elements with classes, ensure the correct syntax is used (e.g., `.customer.address.city` for elements with those classes).

- ✅ PREFERRED: DO use the correct CSS selector syntax to target elements. If targeting by ID, a single '#' followed by the ID is sufficient. If targeting by multiple classes, use '.' to denote each class (e.g., `.class1.class2`). Always verify the target element's actual attributes in the browser's developer tools.

- ⚠️ PROHIBITED: NEVER use a backslash to escape special characters within a CSS selector string unless it's genuinely needed for escaping special CSS characters (and the backslash is properly escaped itself).

- ✅ PREFERRED: ALWAYS ensure special characters like periods (`.`) within CSS selectors are correctly handled. If a period is part of the ID or class name, it should be used directly without escaping, unless it conflicts with CSS syntax. If escaping is truly required, double-check the syntax and escape the backslash itself.

- ⚠️ PROHIBITED: DON'T use escaped dots (`\.`) within CSS selectors when the intention is to match a literal dot in the element's ID or class. The escape character is unnecessary and leads to incorrect element targeting.

- ✅ PREFERRED: DO ensure that dots (`.`) in CSS selectors are treated as literal characters by either removing the escape character or, if the dot is part of a class name, using class-based selectors (e.g., `.customer.address.street`). Verify your locators using browser developer tools before incorporating them into your tests.

- ⚠️ PROHIBITED: DON'T use unescaped periods (`.`) in CSS selectors when the period is intended to be part of the element's ID or class name.  Playwright interprets `.` as a CSS class selector if not escaped.

- ✅ PREFERRED: DO escape the period character (`.`) in CSS selectors with a backslash (`\.`) when the period is part of the ID or class name. This ensures Playwright treats the period literally.

- ⚠️ PROHIBITED: DON'T rely on default timeouts for critical input fields without verifying their presence and readiness. Implicit waits can lead to unpredictable delays.

- ✅ PREFERRED: DO explicitly wait for input fields to be visible and enabled before attempting to fill them, using `locator.wait_for()` with a shorter, more reasonable timeout (e.g., 5-10 seconds) and a clear error message if the timeout is exceeded.

- ⚠️ PROHIBITED: DON'T use unescaped periods in CSS selectors when targeting elements with IDs containing periods. Playwright will interpret the period as a class selector instead of a literal part of the ID.

- ✅ PREFERRED: DO escape periods in CSS selectors with a backslash (`\`) when targeting elements with IDs containing periods (e.g., `#customer\.address\.zipCode` should be `#customer\.address\.zipCode`).

- ⚠️ PROHIBITED: DON'T use a backslash (`\`) to escape periods (`.`) within CSS selectors when targeting element IDs.  This is unnecessary and leads to incorrect locator resolution.

- ✅ PREFERRED: DO use the correct CSS selector syntax, ensuring that special characters like periods are properly escaped if truly needed (though unnecessary here).  Alternatively, consider using alternative locator strategies like data attributes for more robust element selection.

- ⚠️ PROHIBITED: DON'T assume a successful navigation immediately after clicking a link. ALWAYS await for the URL or a specific element on the target page to ensure the navigation is complete.

- ✅ PREFERRED: DO increase the default timeout or configure wait_for_url to wait longer if the application is known to be slow. ALSO, consider adding a retry mechanism to handle intermittent network issues.

- ⚠️ PROHIBITED: DON'T assume that the username field is immediately available after the page loads. ALWAYS implement a mechanism (e.g., `wait_for_selector` or `wait_for_element_state`) to ensure it is present before attempting to interact with it.

- ✅ PREFERRED: DO use `wait_for_selector('[name="username"]')` with an explicit timeout (e.g., 5000ms) BEFORE attempting to fill the username field. This ensures the element is present and interactable.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; ALWAYS implement a short wait or use `locator.wait_for()` with explicit visibility check before attempting to fill the field.

- ✅ PREFERRED: DO use `locator.wait_for(state='visible', timeout=5000)` before attempting to interact with form elements. It guarantees the element exists and ready for user input.

- ⚠️ PROHIBITED: DON'T assume that the 'Confirm Password' field is immediately available and interactable upon page load. ALWAYS implement a check for element visibility and/or state before attempting to fill it.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='stable'` before attempting to interact with a locator. This will ensure that the element is both present and in a stable state to prevent timing issues.

- ⚠️ PROHIBITED: DON'T assume the 'Register' link click will immediately result in navigation; instead, verify the navigation event.

- ✅ PREFERRED: DO implement explicit waits using `page.wait_for_load_state('networkidle')` OR `page.wait_for_function()` after clicking the 'Register' link to ensure the page has fully loaded before proceeding.

- ⚠️ PROHIBITED: DON'T assume successful registration without explicitly verifying a success message or redirect to the expected URL.

- ✅ PREFERRED: DO implement explicit checks for registration success, such as waiting for a specific success message element or verifying the presence of elements expected only on the logged-in homepage. Also, increase the timeout for page navigation.

- ⚠️ PROHIBITED: DON'T rely solely on `wait_for_url` after registration. Instead, verify successful registration (e.g., by checking for a confirmation message) before proceeding to login and expecting the URL change.

- ✅ PREFERRED: DO implement explicit checks for success messages or UI elements after each critical step (e.g., registration, login) to confirm the action completed successfully before proceeding.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are automatically resolvable without explicitly configuring the Python environment or project structure.

- ✅ PREFERRED: DO ensure that all required modules (e.g., 'pages' in this case) are installed and that the Python environment is correctly configured to resolve module dependencies using appropriate import paths or package management.

- ⚠️ PROHIBITED: DON'T assume that all necessary modules are available in the PYTHONPATH; ALWAYS verify the project structure and import statements.

- ✅ PREFERRED: DO ensure the 'pages' directory (containing base_page.py) exists and is accessible from the test directory by either placing 'pages' within the same directory or including the parent directory in PYTHONPATH.

- ⚠️ PROHIBITED: DON'T assume that project structure from previous runs is automatically preserved; ALWAYS verify the presence and correct relative paths of ALL required modules before execution, especially after project re-creation or environment changes.

- ✅ PREFERRED: DO use explicit relative or absolute imports that correctly point to the required modules and verify the PYTHONPATH environment variable for non-standard module locations.

- ⚠️ PROHIBITED: DON'T assume that the `pages` directory is automatically included in the Python path; ALWAYS explicitly verify the import paths in your test files.

- ✅ PREFERRED: DO ensure that the `pages` directory (or any directory containing modules to be imported) is either in the same directory as the test file or is added to the Python path.

- ⚠️ PROHIBITED: DON'T assume that all required modules are automatically accessible; ALWAYS verify module paths and project structure, especially when using relative imports.

- ✅ PREFERRED: DO ensure that all necessary modules are correctly installed and that their paths are correctly configured so that the Python interpreter can find them.

- ⚠️ PROHIBITED: DON'T assume that modules are accessible without explicitly verifying the PYTHONPATH or project structure.

- ✅ PREFERRED: DO ensure that all required modules (e.g., 'pages') are within the Python path or use relative imports correctly to avoid ModuleNotFoundError.
