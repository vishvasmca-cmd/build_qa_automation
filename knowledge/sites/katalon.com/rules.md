
- ⚠️ PROHIBITED: DON'T use `get_by_text` without ensuring uniqueness, especially when the text is common across multiple page sections (e.g., header and mobile menu).

- ✅ PREFERRED: DO use more specific locators, such as chaining with parent elements or using `nth()` to target the desired element when `get_by_text` returns multiple matches. Consider using `data-testid` attributes for reliable targeting.

- ⚠️ PROHIBITED: DON'T assume that all dependent modules are available in the PYTHONPATH or current working directory without explicitly verifying their presence and accessibility.

- ✅ PREFERRED: DO ensure that all required modules are installed and that the PYTHONPATH is correctly configured to include the locations of these modules, or use relative/absolute imports correctly.

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the correct directory structure and module placement.

- ✅ PREFERRED: DO ensure that all modules required by a test file are correctly placed within the project directory and that import statements accurately reflect their location.

- ⚠️ PROHIBITED: DON'T use `get_by_text` with a regex that can match multiple elements without scoping it to a specific container (e.g., header, mobile menu).

- ✅ PREFERRED: DO scope `get_by_text` locators to specific containers (e.g., `header.get_by_text("Products")` or `mobile_menu.get_by_text("Products")`) to ensure they resolve to a single, unambiguous element. Alternatively, use `first` or `last` to select a specific element from the matched set, but only if the order is consistent.

- ⚠️ PROHIBITED: DON'T rely on footer links appearing immediately; the footer may load asynchronously or be hidden initially.

- ✅ PREFERRED: DO use explicit waits with `page.locator(...).wait_for()` to ensure the footer and its elements are fully loaded and visible before attempting to interact with them.

- ⚠️ PROHIBITED: DON'T rely on footer links appearing immediately; the footer may load asynchronously or be obscured by other elements.

- ✅ PREFERRED: DO use explicit waits with `page.locator(...).wait_for()` to ensure the footer and its elements are fully loaded and visible before attempting to interact with them.

- ⚠️ PROHIBITED: DON'T rely solely on default timeouts for mobile navigation elements; they are often subject to animations and dynamic loading.

- ✅ PREFERRED: DO implement explicit waits with increased timeout or retry mechanisms for mobile navigation elements to ensure they are fully visible and interactive before attempting to interact with them.

- ⚠️ PROHIBITED: DON'T use locators that rely solely on text content without considering the context or container, especially when the text is common across multiple elements.

- ✅ PREFERRED: DO use more specific locators that include contextual information (e.g., parent element, CSS class, or ARIA label) to uniquely identify the target element.

- ⚠️ PROHIBITED: DON'T assume that all page objects automatically inherit or implement screenshot methods; explicitly define or inherit them.

- ✅ PREFERRED: DO verify that all required methods (like `take_screenshot`) are correctly defined and implemented in the corresponding page object classes before using them in tests.

- ⚠️ PROHIBITED: DON'T use `get_by_text` with a broad regex like `re.compile(r"products", re.IGNORECASE)` without ensuring it uniquely identifies the target element. Avoid ambiguous text matches that exist in multiple locations (e.g., main header and mobile menu).

- ✅ PREFERRED: DO use more specific locators, such as combining `get_by_label` with `get_by_text` or using `nth()` to target a specific element when multiple matches are expected. Consider using `data-testid` or `data-test-id` attributes for more robust and maintainable locators.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are correctly spelled when called.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are correctly spelled when called.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are consistent across the project.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; ALWAYS verify the method exists before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are spelled correctly when calling them.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object classes have the necessary methods defined and that the method names are correctly spelled.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; ALWAYS verify the method exists in the page object class before calling it.

- ✅ PREFERRED: DO implement a base screenshot method in the `BasePage` class that can be inherited by all page objects, or ensure each page object explicitly defines its own `take_screenshot` method if needed.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are correctly spelled when called.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object classes have the necessary methods defined and that the method names are spelled correctly when calling them.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; ALWAYS verify the method exists in the class definition before calling it.

- ✅ PREFERRED: DO ensure that all page object classes have the necessary methods defined and that the method names are spelled correctly when calling them.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object classes have the necessary methods defined and that the method names are consistent across the project.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO implement a base screenshot method in the `BasePage` class that all page objects can inherit, or ensure each page object explicitly defines its own `take_screenshot` method if needed.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are correctly spelled when called.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object classes have the necessary methods defined and that the method names are correctly spelled.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; ALWAYS verify the method exists in the class definition before calling it.

- ✅ PREFERRED: DO ensure that all page object classes have the necessary methods defined and that the method names are spelled correctly when calling them.

- ⚠️ PROHIBITED: DON'T assume that all page objects have a `take_screenshot` method; ALWAYS verify its existence before calling it.

- ✅ PREFERRED: DO ensure that all page object methods are correctly defined and spelled, and that the correct page object is being used.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object classes have the necessary methods defined and that the method names are correctly spelled when called.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume all page objects have a `take_screenshot` method; verify its existence before calling it.

- ✅ PREFERRED: DO ensure all page object methods are correctly defined and spelled, and that the calling code uses the correct method name.

- ⚠️ PROHIBITED: DON'T assume that all module paths are correctly configured without verifying the project's directory structure.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that their paths are correctly specified in the Python environment and within the test files.

- ⚠️ PROHIBITED: DON'T assume tests will be automatically discovered; ALWAYS explicitly define test paths or discovery patterns in the pytest configuration.

- ✅ PREFERRED: DO verify that test files are named according to pytest's naming conventions (e.g., `test_*.py` or `*_test.py`) and are located in a directory that pytest is configured to search.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are automatically resolved; ALWAYS verify the correct import paths and project structure.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python interpreter can locate them by correctly configuring the PYTHONPATH or using relative imports within the project.

- ⚠️ PROHIBITED: DON'T use `@pytest.mark.asyncio` without first ensuring a compatible async test runner plugin (e.g., `pytest-asyncio`) is installed and configured.

- ✅ PREFERRED: DO install and configure an async test runner plugin (e.g., `pytest-asyncio`) when writing asynchronous tests with pytest.

- ⚠️ PROHIBITED: DON'T use `async def` test functions without first installing and configuring a pytest plugin that supports asynchronous testing, such as `pytest-asyncio`.

- ✅ PREFERRED: DO ensure that your pytest environment is properly configured for asynchronous testing by installing a suitable plugin (e.g., `pytest-asyncio`) and correctly marking asynchronous tests with `@pytest.mark.asyncio`.

- ⚠️ PROHIBITED: DON'T assume that base class methods are automatically inherited or available without explicit definition in the derived class.

- ✅ PREFERRED: DO explicitly define or inherit necessary methods (like `goto`) in page object classes to ensure they are available for use in tests.

- ⚠️ PROHIBITED: DON'T rely solely on the default 'networkidle' state for page load, especially for complex websites like Katalon, as it can be unreliable.

- ✅ PREFERRED: DO implement explicit waits for key elements to be visible or specific network requests to complete after navigation to ensure the page is fully loaded before proceeding with the test.

- ⚠️ PROHIBITED: DON'T use `@pytest.mark.asyncio` without ensuring a compatible async plugin (e.g., `pytest-asyncio`) is installed and configured.

- ✅ PREFERRED: DO verify that the necessary pytest plugins for handling asynchronous tests are installed and correctly configured before running tests containing async functions.

- ⚠️ PROHIBITED: DON'T assume that all module paths are correctly configured without verifying the project's directory structure and Python's import resolution.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python import paths are correctly configured to reflect the project's directory structure.

- ⚠️ PROHIBITED: DON'T use `@pytest.mark.asyncio` without first ensuring a compatible async test runner plugin (e.g., `pytest-asyncio`) is installed and configured.

- ✅ PREFERRED: DO verify that the necessary pytest plugins for handling asynchronous tests are installed and properly configured before running tests containing async functions.

- ⚠️ PROHIBITED: DON'T rely solely on role-based locators like 'get_by_role' without considering potential ambiguity or dynamic content loading. AVOID hardcoded timeouts without proper error handling.

- ✅ PREFERRED: DO implement explicit waits with expected conditions (e.g., element to be visible and enabled) before attempting to interact with elements. DO use more specific locators (e.g., ID, data attributes) when available to reduce ambiguity and improve reliability.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately available after page load; always implement proper waiting mechanisms.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='attached'` before attempting to interact with elements, especially after navigation or dynamic content updates.

- ⚠️ PROHIBITED: DON'T directly import 'test' from 'playwright.sync_api'. Rely on pytest-playwright's fixture injection.

- ✅ PREFERRED: DO ensure pytest-playwright is correctly installed and configured, and access the 'page' fixture provided by it in your test functions.

- ⚠️ PROHIBITED: DON'T explicitly import 'test' from 'playwright.sync_api' when using pytest-playwright.

- ✅ PREFERRED: DO rely on pytest-playwright to automatically inject the 'page' fixture and other Playwright fixtures into your test functions.

- ⚠️ PROHIBITED: DON'T use `@pytest.mark.asyncio` without ensuring a compatible async plugin (e.g., `pytest-asyncio`) is installed and configured in the pytest environment.

- ✅ PREFERRED: DO verify that the necessary pytest plugins for handling asynchronous tests are installed and properly configured before running tests containing async functions.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are correctly configured without verifying the PYTHONPATH or project structure.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the PYTHONPATH is correctly configured to include the project's root directory.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are correctly resolved without verifying the PYTHONPATH or project structure.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the PYTHONPATH is correctly configured to include the project's root directory or any relevant subdirectories containing the required modules.

- ⚠️ PROHIBITED: DON'T use `@pytest.mark.asyncio` without installing a compatible async test runner plugin like `pytest-asyncio`.

- ✅ PREFERRED: DO install and configure an async test runner plugin (e.g., `pytest-asyncio`) when testing asynchronous code with pytest.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are correctly configured before running tests; ALWAYS verify the import paths.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python import paths are correctly configured before running tests.

- ⚠️ PROHIBITED: DON'T forget to `await` asynchronous functions, especially those responsible for triggering navigation events.

- ✅ PREFERRED: DO verify that navigation events are correctly triggered and awaited, and that URL matching logic is accurate and robust.

- ⚠️ PROHIBITED: DON'T assume that the page object modules are correctly located without verifying the import paths in the test files.

- ✅ PREFERRED: DO ensure that the 'pages' directory is in the Python path or use relative imports to correctly locate page object modules.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are correctly resolved without verifying the PYTHONPATH or relative import paths.

- ✅ PREFERRED: DO ensure that all necessary modules are accessible by correctly configuring the PYTHONPATH or using relative imports within the test files.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are correctly configured without verifying the PYTHONPATH or relative import paths.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the PYTHONPATH is correctly configured to resolve import statements before running tests.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are automatically resolved; ALWAYS verify the correct import paths and project structure.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python interpreter can locate them by correctly configuring the PYTHONPATH or using relative imports within the project.

- ⚠️ PROHIBITED: DON'T assume that base class methods are automatically available in derived classes without explicit inheritance or implementation.

- ✅ PREFERRED: DO verify that all required methods are defined or inherited correctly in Page Object classes before using them in tests.

- ⚠️ PROHIBITED: DON'T assume the relative path in import statements is correct without verifying the file structure and module location.

- ✅ PREFERRED: DO double-check and validate the file paths in import statements, especially when using relative paths, to ensure the modules are correctly located and accessible.

- ⚠️ PROHIBITED: DON'T use `@pytest.mark.asyncio` without ensuring a compatible async plugin (e.g., `pytest-asyncio`) is installed and configured in the testing environment.

- ✅ PREFERRED: DO verify that the necessary pytest plugins for handling asynchronous tests are installed and properly configured before running tests that contain async functions.
