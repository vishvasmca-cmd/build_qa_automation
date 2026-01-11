
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
