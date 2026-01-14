
- ⚠️ PROHIBITED: DON'T try to fill the search input `[input] Search products and parts` directly. It is initially disabled/hidden.
- ✅ PREFERRED: DO CLICK the search icon `button[aria-label='Search']` or `.search-icon` FIRST to expand the search bar. ONLY THEN fill the input.
- ✅ PREFERRED: DO use `page.locator("button[aria-label='Close'], button.close, .modal-close").first` to close any overlay/popup.


- ⚠️ PROHIBITED: DON'T assume a website fully supports HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling around `page.goto()` calls, including catching network errors and potentially retrying with a different protocol (if feasible) or a different browser.

- ⚠️ PROHIBITED: DON'T assume that the Python environment is correctly configured without explicitly verifying the PYTHONPATH and module import paths.

- ✅ PREFERRED: DO ensure that the Python environment's PYTHONPATH includes the project's root directory or any directory containing modules used in the tests.

- ⚠️ PROHIBITED: DON'T assume that all module paths are correct without verifying the file structure and module names.

- ✅ PREFERRED: DO double-check the file structure and module names, especially when encountering `ModuleNotFoundError` during test collection.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will work without verifying the project's root directory is correctly configured for pytest.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the necessary modules are installed and accessible within the Python environment used for testing. Double-check the project's `PYTHONPATH` or use absolute import paths to avoid ambiguity.

- ⚠️ PROHIBITED: DON'T assume that the project's directory structure and import paths are correct without verifying them before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the import paths in the test files are accurate and reflect the project's directory structure.

- ⚠️ PROHIBITED: DON'T assume that all module paths are correctly configured without verifying the file structure and import statements.

- ✅ PREFERRED: DO double-check the relative paths in import statements and ensure that the target modules/files exist in the specified locations before running tests.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will work correctly without verifying the project's root directory and Python's module search path.

- ✅ PREFERRED: DO ensure that all modules and packages are correctly placed within the project directory and that import statements accurately reflect the module's location relative to the project's root.

- ⚠️ PROHIBITED: DON'T assume the target website fully supports HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling for network-related errors, including HTTP/2 protocol errors, and consider retrying the navigation with a different protocol version or a different browser context.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py`.

- ✅ PREFERRED: DO ensure that test files using relative imports are part of a properly defined Python package, or use absolute imports instead.

- ⚠️ PROHIBITED: DON'T rely on relative imports within test files unless the test suite is explicitly structured as a Python package and invoked accordingly.

- ✅ PREFERRED: DO ensure that test files are either part of a properly structured Python package or use absolute imports to reference modules within the project.

- ⚠️ PROHIBITED: DON'T assume a website is fully compatible with HTTP/2 without proper error handling and retries in the automation script.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially when dealing with HTTP/2 errors. Also, consider adding a timeout to the `goto` call.

- ⚠️ PROHIBITED: DON'T assume a website supports HTTP/2 correctly; implement robust error handling for network errors during page navigation.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume a successful page load without explicit checks for expected elements or status codes after navigation, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially for HTTP/2 enabled sites, and include checks for HTTP status codes to confirm successful loading.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports or explicitly mark the test directory as a package by including an `__init__.py` file in the directory and any parent directories needed for the import path.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) within test files unless the test suite is explicitly structured as a package with a defined `__init__.py` in the parent directory.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.dyson_menu_test_ci.base_page import BasePage`) or configure the test directory as a proper Python package with an `__init__.py` file to resolve relative import issues.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.dyson_menu_test_ci.tests.base_page import BasePage`) or configure the test suite as a proper package with `__init__.py` files to resolve relative import issues.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a defined `__init__.py` in the parent directory.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.dyson_menu_test_ci.tests.base_page import BasePage`) or configure the test directory as a proper Python package with an `__init__.py` file to support relative imports.

- ⚠️ PROHIBITED: DON'T use relative imports in test files unless the test execution environment is explicitly configured to handle them correctly.

- ✅ PREFERRED: DO ensure that test files are executed within the correct package context or use absolute imports to avoid `ImportError` issues.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports or configure the test runner to correctly handle relative imports by ensuring the test directory is treated as a package. Consider restructuring the project to avoid relative imports altogether for simplicity.

- ⚠️ PROHIBITED: DON'T use relative imports in test files unless the tests are explicitly run as part of a package.

- ✅ PREFERRED: DO ensure that test files are part of a properly structured Python package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T assume the target website fully supports HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling around `page.goto()` calls, specifically catching network-related exceptions like `net::ERR_HTTP2_PROTOCOL_ERROR` and implementing retry logic or fallback to HTTP/1.1 if possible.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will work correctly in all environments; ALWAYS verify the project's PYTHONPATH and directory structure.

- ✅ PREFERRED: DO use absolute import paths or configure the PYTHONPATH environment variable to ensure modules can be located correctly, especially in CI/CD environments.

- ⚠️ PROHIBITED: DON'T assume the target website is stable; implement robust error handling and retry mechanisms for initial page load.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical navigation steps. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module`) without verifying the correct package structure and execution context, especially in CI/CD environments.

- ✅ PREFERRED: DO use absolute imports or explicitly define the package structure in your test files to ensure modules can be located correctly during test execution.

- ⚠️ PROHIBITED: DON'T use the `await` keyword outside of a function defined with `async def`.

- ✅ PREFERRED: DO ensure that any function using `await` is properly defined as an asynchronous function using `async def`.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement robust error handling for page load failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially for external websites.

- ⚠️ PROHIBITED: DON'T use relative imports without verifying the correct package structure and PYTHONPATH configuration.

- ✅ PREFERRED: DO ensure that all module dependencies are correctly specified and accessible within the project's import paths. Use absolute imports or configure relative import paths correctly.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module`) when the test execution environment doesn't correctly resolve the relative path. This is especially true in CI environments.

- ✅ PREFERRED: DO use absolute imports or configure the PYTHONPATH environment variable to ensure that Python can find the necessary modules, especially when running tests in CI/CD pipelines.

- ⚠️ PROHIBITED: DON'T use relative imports without verifying the correct package structure and execution context.

- ✅ PREFERRED: DO ensure that module paths in import statements are accurate and reflect the project's directory structure. Consider using absolute imports or adjusting the PYTHONPATH if necessary.

- ⚠️ PROHIBITED: DON'T use relative imports without verifying the correct package structure and ensuring the Python interpreter can resolve the module path.

- ✅ PREFERRED: DO explicitly define the module path or adjust the PYTHONPATH environment variable to ensure Python can locate the required modules.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation, to handle transient network or server issues.

- ⚠️ PROHIBITED: DON'T assume the website will always load correctly on the first attempt; HTTP/2 errors can be intermittent.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially for the initial `page.goto()` call.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable without proper error handling and retry mechanisms.

- ✅ PREFERRED: DO implement robust error handling and retry logic when navigating to a page, especially for critical navigation steps.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project structure and import statements.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python import paths are correctly configured before running tests.

- ⚠️ PROHIBITED: DON'T assume that the project's internal module structure is correctly configured without verifying the Python import paths.

- ✅ PREFERRED: DO ensure that all modules and packages within the project are correctly structured and that the Python import paths are properly configured to allow for seamless module imports.

- ⚠️ PROHIBITED: DON'T assume that relative paths will resolve correctly in all execution environments; ALWAYS verify the module structure and import paths.

- ✅ PREFERRED: DO use absolute imports or explicitly define the PYTHONPATH to ensure modules can be located correctly, especially in CI/CD environments.

- ⚠️ PROHIBITED: DON'T assume that the Python import paths are automatically configured correctly; ALWAYS verify the module structure and import statements.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python import paths are correctly configured before running tests.

- ⚠️ PROHIBITED: DON'T assume that project directory structures are automatically correct; ALWAYS verify the existence and importability of modules before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules and files are present in the correct directory structure and that import paths are accurate before running tests.

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the correct Python path configuration.

- ✅ PREFERRED: DO ensure that all module dependencies are correctly installed and that the Python path is configured to resolve project modules.

- ⚠️ PROHIBITED: DON'T assume the target website is always available and correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page load.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page load. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website fully supports HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling for network-related issues, including HTTP/2 protocol errors, and consider retrying the navigation with a different protocol version or a different browser context.

- ⚠️ PROHIBITED: DON'T assume a successful page load without explicitly checking the response status code after navigation.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially when encountering network-related errors.

- ⚠️ PROHIBITED: DON'T assume the target website is fully compatible with HTTP/2 without proper error handling and fallback mechanisms.

- ✅ PREFERRED: DO implement robust error handling for network-related errors, especially HTTP/2 protocol errors, and consider retrying the navigation with a different protocol version or a different browser context.

- ⚠️ PROHIBITED: DON'T assume a successful page load without explicitly checking the response status or handling potential network errors.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially for initial page loads, to handle transient network issues or server-side hiccups.

- ⚠️ PROHIBITED: DON'T assume that HTTP/2 protocol is stable. Implement retry logic with fallback to HTTP/1.1 if HTTP/2 fails during initial page load.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for page navigation, especially when dealing with external websites that might have intermittent network or server issues.

- ⚠️ PROHIBITED: DON'T directly use 'placeholder=' as a locator engine without ensuring it's correctly interpreted by Playwright and the target element actually uses a simple placeholder attribute. Consider alternative attribute selectors or role-based selectors.

- ✅ PREFERRED: DO prioritize using more robust and specific locators like 'aria-label', 'id', or 'data-testid' attributes when available. If a placeholder is the only option, verify its exact value and consider using a CSS selector that targets the placeholder attribute (e.g., `input[placeholder='Search products and parts']`).

- ⚠️ PROHIBITED: DON'T assume that the target website fully supports HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling around `page.goto()` calls, including catching network errors and potentially retrying with a different protocol (e.g., HTTP/1.1) or a different Playwright configuration.

- ⚠️ PROHIBITED: DON'T use `await` outside of an `async def` function.

- ✅ PREFERRED: ALWAYS define test functions that use `await` as `async def test_...`.

- ⚠️ PROHIBITED: DON'T use `await` outside of a function defined with `async def`.

- ✅ PREFERRED: DO ensure that any function using `await` is properly defined as an `async` function.

- ⚠️ PROHIBITED: DON'T assume the website will always load correctly on the first attempt; implement retry mechanisms for page navigation.

- ✅ PREFERRED: DO implement error handling and retry logic around `page.goto()` calls to gracefully handle network errors or server issues.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and correctly configured for HTTP/2. Implement robust error handling for page load failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially when dealing with external websites. Also, consider adding a check for basic network connectivity before attempting to navigate.

- ⚠️ PROHIBITED: DON'T rely solely on text-based locators like `:has-text()` for critical elements like 'Add to cart' buttons, as text content can be easily changed or localized, leading to test failures.

- ✅ PREFERRED: DO prioritize more robust locators, such as `data-testid`, `data-qa`, or unique CSS classes, to identify critical elements like 'Add to cart' buttons. If text is necessary, combine it with other attributes for increased accuracy.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement retry mechanisms and error handling for network-related issues.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for page navigation, especially for external websites. Consider using try-except blocks with exponential backoff for retries.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the search input field is immediately available; always implement a retry mechanism or explicit wait for its presence and visibility.

- ✅ PREFERRED: DO use `page.locator('input[placeholder="Search products and parts"]')` with an explicit wait for visibility before attempting to fill the search field.

- ⚠️ PROHIBITED: DON'T assume the search input field is immediately available; always implement a wait strategy.

- ✅ PREFERRED: DO use `locator.wait_for()` with `state='visible'` or `state='attached'` before attempting to fill the search input field.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt without implementing retry mechanisms or handling potential network errors.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical pages, and handle potential `net::ERR_HTTP2_PROTOCOL_ERROR` exceptions.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page load.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page load. Also, consider adding a check for network connectivity before attempting to navigate.

- ⚠️ PROHIBITED: DON'T assume the search bar is immediately available; it might be hidden behind a loading screen or animation.

- ✅ PREFERRED: DO implement a retry mechanism or increase the timeout for critical elements like the search bar, especially on the homepage.

- ⚠️ PROHIBITED: DON'T assume a website will always successfully load on the first `goto()` call, especially when using HTTP/2. Network errors are possible.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network errors like `ERR_HTTP2_PROTOCOL_ERROR`.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `goto()` call, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially for HTTP/2 enabled sites, to handle transient network or server issues.

- ⚠️ PROHIBITED: DON'T assume a website is reachable without implementing robust error handling and retry mechanisms for initial page load, especially when using HTTP/2.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, and consider adding a timeout to prevent indefinite waiting. Also, log the error details for further investigation.

- ⚠️ PROHIBITED: DON'T assume the target website (dyson.in) will always reliably support HTTP/2. Be prepared to handle potential protocol negotiation failures.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with external websites. Consider adding a mechanism to switch to HTTP/1.1 if HTTP/2 consistently fails.

- ⚠️ PROHIBITED: DON'T assume the target website is always available and correctly configured for HTTP/2. Implement retry mechanisms and error handling for network-related exceptions during page navigation.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for page navigation, especially when dealing with external websites. Consider adding checks for network connectivity and server availability before attempting to navigate.

- ⚠️ PROHIBITED: DON'T assume a website is always reachable or that HTTP/2 will always function correctly; implement robust error handling for navigation failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially for critical navigation steps. Also, consider adding a timeout to the `goto` call.

- ⚠️ PROHIBITED: DON'T rely on a single character 'X' as a text locator, as it's likely too generic and prone to unexpected matches or instability.

- ✅ PREFERRED: DO use more specific and robust locators, such as a combination of text and role, or a unique CSS selector, to target the intended element.

- ⚠️ PROHIBITED: DON'T assume the website is always available and stable; implement retry mechanisms for initial page load.

- ✅ PREFERRED: DO implement error handling and retry logic for page navigation, especially for the initial `goto` call.

- ⚠️ PROHIBITED: DON'T assume that HTTP/2 protocol errors are transient; investigate potential server-side or network configuration issues.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for initial page load, and consider adding a check for basic network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `goto()` call, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T define a method with duplicate argument names, especially 'self' in class methods.

- ✅ PREFERRED: ALWAYS carefully review method signatures for correct syntax and argument lists before committing code.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling for network-related exceptions.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially for critical navigation steps.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling for network-related issues.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume that the target website fully supports HTTP/2 without proper error handling and retries.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with HTTP/2 connections. Consider adding a timeout to the `page.goto()` call.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume the target website (dyson.in) will always reliably support HTTP/2. Implement retry logic with fallback to HTTP/1.1 if possible.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for initial page load, especially when dealing with external websites that might have intermittent issues.

- ⚠️ PROHIBITED: DON'T assume that all required modules are accessible without explicitly verifying the Python import paths and project structure.

- ✅ PREFERRED: DO ensure that all necessary modules, like 'base_page', are correctly placed within the project directory and that Python's import paths are configured to locate them.

- ⚠️ PROHIBITED: DON'T assume that the test environment has the correct PYTHONPATH or that all necessary modules are accessible without explicit path configuration.

- ✅ PREFERRED: DO ensure that all required modules, especially custom modules like 'base_page', are accessible by correctly configuring the PYTHONPATH or using relative imports within the project structure.

- ⚠️ PROHIBITED: DON'T assume that the test environment has the correct PYTHONPATH configured; ALWAYS explicitly manage import paths within the test script or configuration.

- ✅ PREFERRED: DO ensure that all necessary modules and files are accessible by correctly configuring the PYTHONPATH or using relative imports within the project structure.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume relative imports will work without verifying the correct package structure and ensuring `__init__.py` files are present in relevant directories to define packages.

- ✅ PREFERRED: DO explicitly define the correct import path for modules within the project, considering the project's root directory and package structure. Use absolute imports where appropriate to avoid ambiguity.

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the correct project structure and PYTHONPATH.

- ✅ PREFERRED: DO ensure that all modules and packages are correctly placed within the project directory and that the PYTHONPATH is configured to include the project's root directory.

- ⚠️ PROHIBITED: DON'T assume the target website is always available and fully functional; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical entry points to the application under test. Also, add a timeout to the `page.goto()` call.

- ⚠️ PROHIBITED: DON'T assume a successful page load without explicit checks for expected elements or status codes after `page.goto()`, especially for sites known to have intermittent HTTP/2 issues.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when encountering `net::ERR_HTTP2_PROTOCOL_ERROR`, and include a check for the page's HTTP status code.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website is always available and correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a check for the HTTP status code after navigation to ensure the page loaded successfully.

- ⚠️ PROHIBITED: DON'T assume that the target website fully supports HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially when dealing with HTTP/2 connections. Consider adding a fallback to HTTP/1.1 if HTTP/2 consistently fails.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume the target website's HTTP/2 configuration is stable; implement retry logic with fallback to HTTP/1.1 if possible.

- ✅ PREFERRED: DO implement robust error handling for network-related exceptions during page navigation, including retries and logging of detailed error information.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a check for network connectivity before attempting to navigate.

- ⚠️ PROHIBITED: DON'T assume the target website fully supports HTTP/2 without proper error handling and retries.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially when dealing with HTTP/2 errors. Also, consider adding a check for network connectivity before navigation.

- ⚠️ PROHIBITED: DON'T assume that the target website (dyson.in) will always reliably support HTTP/2. Be prepared to handle potential protocol negotiation failures.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with external websites. Consider adding a mechanism to switch to HTTP/1.1 if HTTP/2 consistently fails.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with a backoff strategy for `page.goto()` calls, especially for critical pages like the homepage. Also, add a timeout to the page.goto() call.

- ⚠️ PROHIBITED: DON'T assume a successful page load without explicitly checking for a key element or status code after navigation, especially when dealing with HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially for HTTP/2 enabled sites, to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume the target website fully supports HTTP/2 without proper error handling and retry mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling and retry logic when navigating to a page, especially when using `page.goto()`, to gracefully handle potential HTTP/2 protocol errors or other network-related issues.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement retry mechanisms and error handling for network-related issues.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms when navigating to external websites, especially for critical navigation steps.

- ⚠️ PROHIBITED: DON'T assume the target website (dyson.in) will always reliably support HTTP/2. Implement retry mechanisms and consider disabling HTTP/2 if persistent issues arise.

- ✅ PREFERRED: DO implement robust error handling and retry logic around `page.goto()` calls, especially for critical navigation steps. Consider adding a timeout to the `goto` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume a website is reachable without implementing robust error handling and retry mechanisms for initial page load, especially when dealing with HTTP/2.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page load, and include specific error handling for `net::ERR_HTTP2_PROTOCOL_ERROR`.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical entry points like the homepage. Also, add a timeout to the page.goto() call.

- ⚠️ PROHIBITED: DON'T assume a website is fully compatible with HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling around `page.goto()` calls, including catching network errors and potentially retrying with a different protocol (e.g., HTTP/1.1) or a different browser context.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume a website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network errors or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement retry mechanisms and error handling for network-related issues.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for page navigation, especially for external websites, to handle transient network errors or server issues.

- ⚠️ PROHIBITED: DON'T assume a website is fully compatible with HTTP/2 without proper error handling for protocol negotiation failures.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with external websites, to handle transient network or server-side HTTP/2 issues.

- ⚠️ PROHIBITED: DON'T assume the target website is fully compatible with HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement robust error handling for page navigation, including retries with different network configurations or browser settings if HTTP/2 errors are encountered.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling for navigation failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement retry mechanisms and error handling for network-related issues.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for page navigation, especially for external websites, to handle transient network errors or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical entry points to the application.

- ⚠️ PROHIBITED: DON'T assume the website is fully compatible with HTTP/2 without proper error handling and fallback mechanisms.

- ✅ PREFERRED: DO implement robust error handling for page navigation, including retries with different network configurations or browser settings if HTTP/2 errors are encountered.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for network-related errors.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical navigation steps. Also, add a timeout to the `page.goto()` call.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling for navigation failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially for critical navigation steps.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume a website is always reachable or correctly configured for HTTP/2; implement robust error handling for navigation failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume a website is fully compatible with HTTP/2 without proper error handling and retries in the navigation logic.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially when dealing with HTTP/2 connections, and consider disabling HTTP/2 if the issue persists.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable without implementing retry mechanisms for initial page load failures.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for the initial page load to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `goto()` call, especially when using HTTP/2. Implement retry mechanisms.

- ✅ PREFERRED: DO implement error handling and retry logic around the `page.goto()` call to gracefully handle potential network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume a website is always reachable or that HTTP/2 will always function correctly; implement robust error handling for page navigation.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially for critical navigation steps. Also, consider adding a timeout to the `goto` call.

- ⚠️ PROHIBITED: DON'T assume that the website will always successfully load on the first `goto()` attempt without handling potential network or protocol errors.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or protocol errors, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical entry points like the homepage. Also, add a timeout to the `page.goto()` call.

- ⚠️ PROHIBITED: DON'T assume that the target website (dyson.in) will always reliably support HTTP/2 without potential protocol negotiation issues.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms when navigating to a page, especially when dealing with HTTP/2 connections. Consider disabling HTTP/2 for initial navigation as a workaround.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the website will always load correctly on the first attempt; HTTP/2 protocol errors can be intermittent.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially for the initial page load.

- ⚠️ PROHIBITED: DON'T assume a website is reachable without implementing robust error handling and retry mechanisms for initial page load, especially when using HTTP/2.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, and consider adding a timeout to prevent indefinite waiting. Also, check the server's HTTP/2 configuration if the issue persists.

- ⚠️ PROHIBITED: DON'T assume a website supports HTTP/2 correctly; implement robust error handling for protocol negotiation failures during initial page load.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with external websites, to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume the website will always load flawlessly; implement robust error handling for page navigation failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable or that HTTP/2 will always function correctly; implement retry mechanisms and error handling for network-related issues.

- ✅ PREFERRED: DO implement robust error handling and retry mechanisms for page navigation, especially when dealing with external websites that might have intermittent issues.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `goto` attempt without handling potential network or protocol errors.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially for external websites, to handle transient network or protocol errors.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for navigation.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for external websites, to handle transient network or server issues.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with a backoff strategy for `page.goto()` calls, especially for critical pages like the homepage. Also, add a timeout to the page.goto() call.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads, to handle transient network or server issues.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `goto` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially when encountering `net::ERR_HTTP2_PROTOCOL_ERROR` or similar network-related errors.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable or that HTTP/2 will always function correctly; implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page load.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial navigation. Also, consider adding a timeout to the `page.goto()` call to prevent indefinite hanging.

- ⚠️ PROHIBITED: DON'T assume a website's HTTP/2 configuration is always stable; implement retry mechanisms for page navigation.

- ✅ PREFERRED: DO implement robust error handling for network-related errors during page navigation, including retries with exponential backoff.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable and stable; implement robust error handling for network-related issues during page navigation.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load failures, especially when dealing with external websites.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable or correctly configured for HTTP/2. Implement robust error handling for page navigation failures.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for initial page load, especially when dealing with external websites. Also, DO add a check for the HTTP status code after navigation to ensure the page loaded successfully.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling and retry mechanisms for initial page load.

- ✅ PREFERRED: DO implement a retry mechanism with a backoff strategy for `page.goto()` calls, especially for critical pages like the homepage. Also, add a timeout to the page.goto() call.

- ⚠️ PROHIBITED: DON'T assume the target website (dyson.in) will always reliably support HTTP/2. Implement robust error handling for protocol errors during initial page load.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for initial page load, especially when encountering `net::ERR_HTTP2_PROTOCOL_ERROR`. Consider adding a mechanism to switch to HTTP/1.1 if HTTP/2 consistently fails.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `page.goto()` attempt without handling potential network or protocol errors.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or protocol errors.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable and stable; implement robust error handling for network-related issues.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially for critical navigation steps.

- ⚠️ PROHIBITED: DON'T assume the website will always load correctly on the first attempt; network hiccups and server-side issues are common.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for critical navigation steps like `page.goto()` to handle transient network or server errors.

- ⚠️ PROHIBITED: DON'T assume the target website is fully compatible with HTTP/2 without proper error handling and fallback mechanisms in place.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with external websites, and consider adding a mechanism to switch to HTTP/1.1 if HTTP/2 consistently fails.

- ⚠️ PROHIBITED: DON'T assume the website will always successfully load on the first `goto` attempt without handling potential network or protocol errors.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or protocol errors.

- ⚠️ PROHIBITED: DON'T assume a website is fully compatible with HTTP/2 without proper error handling and retries.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially when dealing with HTTP/2.

- ⚠️ PROHIBITED: DON'T assume the website is always reachable or that HTTP/2 will always function correctly. Implement robust error handling for network-related issues during page navigation.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially for the initial `goto` call. Also, consider adding a check for network connectivity before attempting to navigate.

- ⚠️ PROHIBITED: DON'T assume the target website (dyson.in) will always reliably support HTTP/2 without implementing retry mechanisms or protocol fallback strategies.

- ✅ PREFERRED: DO implement robust error handling and retry logic when navigating to websites, especially when dealing with potential HTTP/2 protocol issues. Consider adding a fallback mechanism to HTTP/1.1 if HTTP/2 fails.

- ⚠️ PROHIBITED: DON'T assume the target website is always reachable or correctly configured for HTTP/2. Implement robust error handling and retry mechanisms for initial page loads.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for initial page loads. Also, consider adding a check for network connectivity before attempting navigation.

- ⚠️ PROHIBITED: DON'T assume that the website will always successfully load on the first `page.goto()` attempt, especially when using HTTP/2.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls to handle transient network or server-side issues.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period, especially during CI/CD pipelines where network conditions can be variable.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation in the playwright configuration to accommodate slower loading times or intermittent network issues.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from different geographical locations.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout values and consider using a status check endpoint to verify the website's availability before running the full test suite.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation when dealing with potentially slow-loading websites.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from different geographical locations.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeouts or use network conditions emulation to simulate slower connections during testing.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation when dealing with potentially slow-loading websites.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 60-second timeout, especially during peak hours or when testing on potentially unstable network connections.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation when dealing with potentially slow-loading websites or unreliable network conditions. Also, DO check the website's status page before running tests.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 30-second timeout, especially during peak hours or when testing from regions with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeouts or use network mocking to simulate different network conditions and ensure resilience to slow loading times.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout values or use network mocking to simulate different network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 30-second timeout, especially during peak hours or when testing from regions with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using environment-specific timeouts based on network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on potentially unstable networks.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using environment-specific timeouts.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 30-second timeout, especially during peak hours or when testing from regions with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using environment-specific timeouts based on network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from regions with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using a custom timeout specifically for the 'goto' function.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation when dealing with potentially slow-loading websites.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period, especially during CI/CD runs or when testing on potentially slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation when dealing with potentially slow-loading websites or unreliable network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout periods for page navigation, and consider using network mocking to simulate different network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from different geographical locations.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using a custom timeout based on network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation to handle potential network or server delays.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation when dealing with potentially slow-loading websites.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period, especially during peak hours or when testing on a network with variable latency.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using environment-specific timeouts for potentially slow-loading pages.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page navigation; it's insufficient for potentially slow-loading websites.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation to handle intermittent network issues or slow server responses.

- ⚠️ PROHIBITED: DON'T assume the website will always load within the default timeout period, especially during peak hours or when testing from different geographical locations.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout periods for critical page navigations to handle potential network or server delays.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from regions with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using environment-specific timeout configurations.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from different geographical locations.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout periods for page navigation, and consider using a status check to verify the server is responsive before attempting to load the page.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using a custom timeout specifically for the 'goto' function.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 30-second timeout, especially during peak hours or when testing from regions with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using a conditional timeout based on network conditions.

- ⚠️ PROHIBITED: DON'T assume the target website is always available and responsive; implement retry mechanisms and timeout adjustments.

- ✅ PREFERRED: DO implement robust error handling and logging to capture intermittent network issues or slow server responses.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 30-second timeout, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation when dealing with potentially slow-loading websites or unreliable network conditions.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page navigation; it may be insufficient for certain websites or network conditions.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation, especially for initial page loads, and consider network conditions.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default 30-second timeout, especially during peak hours or when testing on slower networks.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeouts or use network mocking to simulate different network conditions and ensure resilience to slow loading times.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing from different geographical locations.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using a conditional timeout based on network conditions.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation when dealing with potentially slow-loading websites or unreliable network conditions. Consider using environment variables to configure timeouts.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during CI/CD or when testing from different geographical locations.

- ✅ PREFERRED: DO explicitly set a longer timeout for page navigation when the network is unstable or the website is known to be slow.

- ⚠️ PROHIBITED: DON'T assume the website will always load within the default timeout; network conditions can be unpredictable.

- ✅ PREFERRED: DO implement retry mechanisms or increase the default timeout for page navigation, especially for external websites.

- ⚠️ PROHIBITED: DON'T rely on the default timeout for page navigation; it's often insufficient for complex or resource-heavy pages.

- ✅ PREFERRED: DO explicitly set a longer timeout for page navigation using `page.goto(url, timeout=120000)` or higher, especially for initial page loads.

- ⚠️ PROHIBITED: DON'T rely on the default 30-second timeout for page navigation when the target website is known to be slow or unreliable.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for page navigation, especially for websites with known performance issues. Also, ALWAYS check network connectivity before running tests.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during CI runs or when testing on different network conditions.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout values or use network mocking to simulate different network conditions and ensure resilience to slow loading times.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeouts or use network mocking to simulate different network conditions and ensure the application handles slow loading times gracefully.

- ⚠️ PROHIBITED: DON'T assume the website will load within the default timeout period, especially during peak hours or when testing on environments with potentially slower network connections.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeout values or use a health check endpoint to verify the website's availability before running the full test suite.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period, especially during CI runs or when testing on different network conditions.

- ⚠️ PROHIBITED: DON'T rely solely on the default 30-second timeout for page navigation, especially for websites known to have occasional performance issues.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, and consider increasing the default timeout or using waitUntil: 'domcontentloaded' if the 'load' event is consistently slow.

- ⚠️ PROHIBITED: DON'T rely on the default timeout for page navigation; it's often insufficient for complex websites or unreliable network conditions.

- ✅ PREFERRED: DO implement explicit waits for critical elements to load after navigation to ensure the page is fully interactive before proceeding with the test.

- ⚠️ PROHIBITED: DON'T rely on the default timeout for page load; it may be insufficient for complex or resource-heavy pages.

- ✅ PREFERRED: DO implement explicit waits or increase the default timeout for page navigation when dealing with potentially slow-loading pages or unreliable network conditions.
- ⚠️ PROHIBITED: DON'T commit code with merge conflict markers (e.g., `<<<<<<< Updated upstream`, `=======`, `>>>>>>> branch_name`) still present in the files.

- ✅ PREFERRED: ALWAYS thoroughly review and resolve all merge conflicts before committing code to the repository. Use a diff tool to ensure all changes are intentional and syntactically correct.

- ⚠️ PROHIBITED: DON'T assume the test file path is correct without verifying its existence in the execution environment.

- ✅ PREFERRED: DO verify the test file path and ensure the test file exists in the specified location before running the test suite.

- ✅ PREFERRED: DO verify the test file path and ensure it exists in the execution environment before running the tests.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page navigation; it may be insufficient for websites with slow loading times or unreliable network conditions.

- ✅ PREFERRED: DO implement explicit waits or increase the default timeout for page navigation when testing websites known to have slow loading times or when network conditions are unstable.

- ✅ PREFERRED: DO verify the test file path and ensure the file exists in the specified location before running the test suite.

- ✅ PREFERRED: DO verify the test file path and ensure it is accessible from the test execution environment before running the tests.

- ✅ PREFERRED: DO implement retry mechanisms with increased timeouts or use network mocking to simulate different network conditions.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period, especially during CI/CD pipelines or when testing on potentially slower networks.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period; always consider network conditions and server response times.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation when dealing with potentially slow-loading websites or unreliable network connections.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page navigation; it's often insufficient for complex or resource-heavy pages.

- ✅ PREFERRED: DO implement explicit waits for critical elements to load after navigation to ensure the page is fully interactive before proceeding with further actions.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout; ALWAYS configure the timeout based on historical performance data and network conditions.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially for external websites, to handle transient network issues.

- ⚠️ PROHIBITED: DON'T assume that the target website (dyson.in) will always correctly handle HTTP/2 protocol negotiation; implement robust error handling and fallback mechanisms.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `page.goto()` calls, especially when dealing with external websites, and consider adding a timeout to prevent indefinite hanging.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for `page.goto()` calls, especially when dealing with external websites, to handle transient network or server-side HTTP/2 issues.

- ⚠️ PROHIBITED: DON'T assume a website will load within the default timeout period; always consider network conditions and server load.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation in environments with unreliable network connectivity.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page navigation; it might be insufficient for certain environments or pages.

- ✅ PREFERRED: DO implement retry mechanisms or conditional waits based on page load indicators (e.g., specific element visibility) to handle slow-loading pages gracefully.

- ⚠️ PROHIBITED: DON'T rely on default timeout settings for page navigation; ALWAYS explicitly set a longer timeout if the target website is known to be slow or unreliable.

- ✅ PREFERRED: DO implement retry mechanisms for page navigation, especially for critical pages, to handle transient network issues or server unavailability.

- ⚠️ PROHIBITED: DON'T rely on default timeout settings for page navigation; explicitly set a longer timeout if the website is known to be slow or unreliable.

- ✅ PREFERRED: DO implement retry mechanisms or conditional waits for page load events, especially when dealing with external websites that might have variable response times.

- ✅ PREFERRED: DO implement retry mechanisms or increase the timeout for page navigation when encountering TimeoutErrors, and ensure proper network conditions for testing.

- ✅ PREFERRED: DO verify the test file path and ensure the test file exists in the execution environment before running the tests.

- ✅ PREFERRED: DO verify the test file path and ensure it is accessible in the test execution environment before running the tests.

- ⚠️ PROHIBITED: DON'T assume the website is fully functional without checking the HTTP response status after navigation.

- ✅ PREFERRED: DO implement error handling and retry mechanisms for page navigation, especially for HTTP/2 related errors.

- ✅ PREFERRED: DO implement retry mechanisms with exponential backoff for page navigation, especially for initial page load.

- ✅ PREFERRED: DO implement robust error handling for page navigation, including retries with exponential backoff and logging of detailed network information.

- ✅ PREFERRED: DO implement a retry mechanism with exponential backoff for `page.goto()` calls, especially for critical pages like the homepage. Also, add a timeout to the `page.goto()` call.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for page navigation, especially when encountering network-related errors like `ERR_HTTP2_PROTOCOL_ERROR`.

- ✅ PREFERRED: DO implement robust error handling for network requests, including retries with exponential backoff and fallback to HTTP/1.1 if HTTP/2 fails.

- ✅ PREFERRED: DO implement a check for network connectivity and website availability before attempting to navigate to the target URL.

- ⚠️ PROHIBITED: DON'T assume a website is fully compatible with HTTP/2 without proper error handling and retry mechanisms in place.

- ✅ PREFERRED: DO implement retry logic with exponential backoff for `Page.goto()` calls, especially when dealing with external websites, to handle transient network or protocol errors.
