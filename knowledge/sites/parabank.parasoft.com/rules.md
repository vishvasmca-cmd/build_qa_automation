# Parabank Workflow Rules

## 1. Complex Workflow: Register -> Transfer
When executing the full "Register to Transfer" flow, you must follow this sequence strictly due to session handling quirks:

1.  **Registration**:
    -   Use a **UNIQUE** username every time (append random digits).
    -   After clicking "Register", wait for `text="Your account was created successfully"`.
    -   **CRITICAL**: You are *already logged in* after registration. DO NOT try to log in again.

2.  **Open New Account**:
    -   Navigate to "Open New Account".
    -   Wait for the account type dropdown to load.
    -   Click "Open New Account" button.
    -   Wait for `text="Account Opened!"`.
    -   **Capture**: Store the **New Account ID** if possible, but at minimum wait for the success message.

3.  **Transfer Funds**:
    -   Navigate to "Transfer Funds".
    -   **Wait**: The "From Account" and "To Account" dropdowns load via AJAX. You **MUST** wait for `locator("#fromAccountId option")` to be present.
    -   Input Amount (e.g., "100").
    -   Click "Transfer".
    -   Assert `text="Transfer Complete!"`.

- ⚠️ PROHIBITED: DON'T assume the 'Register' link click will immediately result in navigation to the registration page; the server might need time to process the request.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for critical navigation events like clicking the 'Register' link, to handle intermittent server delays.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py`.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined Python package or use absolute imports to reference modules in other directories.

- ⚠️ PROHIBITED: DON'T assume the relative path between test files and page object modules will remain constant across different execution environments or project structures. ALWAYS verify the path.

- ✅ PREFERRED: DO use absolute imports or explicitly define the Python path to ensure modules can be located correctly, especially when running tests from different directories or environments.

- ⚠️ PROHIBITED: DON'T assume that the project's directory structure and import paths are correct without verifying them before running the tests.

- ✅ PREFERRED: DO ensure that all modules and packages are correctly placed within the project directory and that import statements accurately reflect the project's structure.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the Python path configuration.

- ✅ PREFERRED: DO ensure that all modules and packages are correctly placed within the project directory and that the Python path is configured to include the project's root directory or any necessary subdirectories.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will always resolve correctly without verifying the project's root directory and module locations.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory, and that the necessary files exist in the specified locations.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will always resolve correctly without verifying the project's root directory and module locations.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory, and that the necessary modules are present in the expected locations.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py`.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined Python package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T use generic class-based locators like ".button" without ensuring they uniquely identify the target element. ALWAYS aim for specificity.

- ✅ PREFERRED: DO use more specific locators, such as `get_by_role` with appropriate name or `nth` to target the desired element when multiple elements match a general locator.

- ⚠️ PROHIBITED: DON'T assume the relative path between test files and page object modules is correct without verifying the file structure.

- ✅ PREFERRED: DO explicitly verify the relative path between test files and page object modules, and ensure the page object modules exist in the specified location.

- ⚠️ PROHIBITED: DON'T assume that relative paths will resolve correctly without verifying the project's directory structure and the location of the imported modules.

- ✅ PREFERRED: DO explicitly verify the existence and location of all imported modules, especially when using relative paths, before running tests.

- ⚠️ PROHIBITED: DON'T assume that module paths are correct without verifying the file structure and import statements.

- ✅ PREFERRED: DO double-check the file paths and module names in import statements to ensure they accurately reflect the project's directory structure.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in the parent directory.

- ✅ PREFERRED: DO ensure that test files using relative imports are part of a properly structured Python package, or use absolute imports instead to avoid `ImportError`.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined Python package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T rely solely on the default 30-second timeout for critical button clicks; ALWAYS implement explicit waits with shorter, more appropriate timeouts based on expected page load times and element visibility.

- ✅ PREFERRED: DO verify the button's presence, enabled state, and visibility before attempting to click it. Use `locator.is_visible()`, `locator.is_enabled()`, and `locator.is_stable()` to ensure the button is ready for interaction.

- ⚠️ PROHIBITED: DON'T use ambiguous locators like `input.button` that can resolve to multiple elements without specifying which one is intended.

- ✅ PREFERRED: DO use more specific locators, such as `get_by_role` with a name or `nth` to target the desired element when multiple elements match a general locator.

- ⚠️ PROHIBITED: DON'T run test files with relative imports directly; ALWAYS execute tests from the project root or use absolute imports.

- ✅ PREFERRED: DO ensure that test files using relative imports are part of a properly structured Python package and are executed from the package root, or refactor relative imports to absolute imports.

- ⚠️ PROHIBITED: DON'T assume that submit buttons are immediately clickable after page load; ALWAYS implement explicit waits or use `locator.wait_for_element_state('enabled')` before attempting to click.

- ✅ PREFERRED: DO use `locator.wait_for_element_state('stable')` or `locator.wait_for_element_state('visible')` before interacting with elements, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in the parent directory.

- ✅ PREFERRED: DO ensure that test files are either part of a properly structured package or use absolute imports to reference modules within the project.

- ⚠️ PROHIBITED: DON'T rely solely on `wait_for_url` immediately after clicking a link; the navigation might be delayed due to network conditions or client-side processing.

- ✅ PREFERRED: DO verify the element that triggers the navigation is actually visible and enabled before clicking it. Also, consider adding a small delay before `wait_for_url` to allow for initial processing.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available and interactable upon page load. ALWAYS implement a wait strategy.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` before attempting to interact with the username field to ensure it's fully loaded and ready.

- ⚠️ PROHIBITED: DON'T assume that the username field is immediately available upon page load; always implement a wait strategy.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='attached'` before attempting to fill the username field to ensure it's ready for interaction.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a Python package and executed as such.

- ✅ PREFERRED: DO ensure that test files either use absolute imports or are executed as part of a properly structured Python package when using relative imports.

- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; the page might be loading or have dynamic content.

- ✅ PREFERRED: DO use `locator('[name='username']').wait_for()` before attempting to fill the username field to ensure it's present and visible.

- ⚠️ PROHIBITED: DON'T assume dropdown options are immediately available; always implement a wait strategy before interacting with dropdowns.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` before attempting to select an option from a dropdown, especially when the dropdown is dynamically populated.

- ⚠️ PROHIBITED: DON'T assume dropdown options are immediately available; ALWAYS wait for the dropdown to be populated before attempting to select an option.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` before interacting with dropdowns, especially after page loads or dynamic content updates.

- ⚠️ PROHIBITED: DON'T assume that dropdown elements are immediately available and interactive upon page load. ALWAYS implement explicit waits.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` before interacting with dropdown elements to ensure they are fully loaded and ready for interaction.

- ⚠️ PROHIBITED: DON'T assume dropdowns are immediately available; ALWAYS check their state before interacting.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` before interacting with dropdowns, especially after page loads or navigations.

- ⚠️ PROHIBITED: DON'T assume that dropdown options are immediately available; always wait for the dropdown to be fully populated and interactable before attempting to select an option.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='attached'` or `state='visible'` before interacting with dropdown elements to ensure they are fully loaded and ready for interaction.
