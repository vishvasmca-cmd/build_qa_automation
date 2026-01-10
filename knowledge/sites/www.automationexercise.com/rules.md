
- ⚠️ PROHIBITED: DON'T assume the 'Products' page will load within 30 seconds; implement more robust checks for page content after navigation.

- ✅ PREFERRED: DO implement explicit waits for key elements on the 'Products' page to be visible after clicking the 'Products' link to confirm successful navigation, instead of only checking the URL.

- ⚠️ PROHIBITED: DON'T assume that helper modules are automatically available; ALWAYS verify their existence and correct import paths before running tests.

- ✅ PREFERRED: DO ensure that all necessary helper modules are present and accessible by defining the correct relative or absolute paths in import statements.

- ⚠️ PROHIBITED: DON'T assume helper files are automatically accessible; ALWAYS verify the correct relative or absolute import path.

- ✅ PREFERRED: DO use explicit relative imports (e.g., `from .helpers import take_screenshot`) if the helper file is in the same directory, or configure the PYTHONPATH environment variable for absolute imports.

- ⚠️ PROHIBITED: DON'T rely on default timeouts for page load; always explicitly wait for critical elements to be visible or specific network requests to complete.

- ✅ PREFERRED: DO implement explicit waits for key elements or network requests to ensure the page is fully loaded before proceeding with interactions.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the package structure is explicitly defined and correctly initialized.

- ✅ PREFERRED: DO ensure that test files are either part of a properly structured Python package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T use relative imports within test files unless the test suite is explicitly structured as a package and invoked as such.

- ✅ PREFERRED: DO ensure that test files are either run as part of a package (using `python -m pytest`) or use absolute imports to reference modules within the project.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test runner is explicitly configured to handle them correctly, and the file structure supports it.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.automationexercise_regression.tests.e2e.base_page import BasePage`) or configure the Python path to correctly resolve relative imports in test files.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py`.

- ✅ PREFERRED: DO ensure that test files using relative imports are part of a properly structured Python package, or use absolute imports instead.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the package structure is explicitly initialized and the test runner is configured to handle them correctly.

- ✅ PREFERRED: DO use absolute imports or explicitly define the package structure and import paths to avoid `ImportError` when running tests.

- ⚠️ PROHIBITED: DON'T use relative imports within test files unless the test suite is explicitly structured as a package and the test runner is configured accordingly.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined Python package or use absolute imports to reference modules within the project.

- ⚠️ PROHIBITED: DON'T use relative imports within test files unless the test suite is explicitly structured and executed as a package.

- ✅ PREFERRED: DO ensure that test files are either executed as part of a package (using `python -m pytest`) or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.automationexercise_regression.tests.e2e.base_page import BasePage`) or configure the test directory as a proper Python package with `__init__.py` files to enable relative imports.

- ⚠️ PROHIBITED: DON'T assume the page is fully loaded and interactive immediately after navigation; always wait for a specific element or condition to ensure stability.

- ✅ PREFERRED: DO implement explicit waits for critical elements or network activity to complete before interacting with the page, especially after navigation or significant UI changes.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' link is immediately available; always implement a retry mechanism or explicit wait with a more robust selector.

- ✅ PREFERRED: DO use more specific and resilient locators, such as data attributes or a combination of attributes, to target the 'Add to cart' button. Also, DO check if the product is in stock before attempting to add it to the cart.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page load, especially when dealing with external resources or potentially slow-loading content.

- ✅ PREFERRED: DO implement explicit waits for critical elements or network requests to complete before proceeding with the test, or increase the default timeout if the application consistently takes longer to load.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page load; especially when dealing with external resources or potentially slow-loading content.

- ✅ PREFERRED: DO implement explicit waits for critical elements or network requests to complete before proceeding with interactions, or increase the default timeout if the application consistently takes longer to load.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' link is immediately available; account for potential loading delays or dynamic content.

- ✅ PREFERRED: DO implement explicit waits or retries when interacting with elements that may not be immediately available, especially after page loads or dynamic content updates.

- ⚠️ PROHIBITED: DON'T rely on the 'Add to cart' link appearing immediately; it may require a wait or a more specific selector.

- ✅ PREFERRED: DO implement explicit waits or use more robust selectors (e.g., data-testid) to ensure the 'Add to cart' link is present and visible before attempting to click it.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page load states, especially when dealing with websites known to have variable loading times or heavy resource usage.

- ✅ PREFERRED: DO implement explicit waits or increase the default timeout for page load states when network conditions are unstable or the target website is known to be slow.

- ⚠️ PROHIBITED: DON'T rely on the 'Add to cart' link appearing immediately; it might be delayed by animations or dynamic content loading.

- ✅ PREFERRED: DO implement a retry mechanism or explicit wait with a more robust selector (e.g., using data attributes) to ensure the 'Add to cart' element is present and interactable before attempting to click it.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page load, especially when dealing with external resources or potentially slow-loading content.

- ✅ PREFERRED: DO implement explicit waits for critical elements or network requests to complete before proceeding with interactions, or increase the default timeout if the application consistently requires more time to load.

- ⚠️ PROHIBITED: DON'T rely solely on the default timeout for page load; especially when dealing with external resources or potentially slow-loading content.

- ✅ PREFERRED: DO implement explicit waits for critical elements or network requests to complete before proceeding with the test, or increase the default timeout if the application consistently takes longer to load.

- ⚠️ PROHIBITED: DON'T rely solely on default timeout settings; ALWAYS explicitly set timeouts based on expected element load times and network conditions.

- ✅ PREFERRED: DO verify the project's directory structure and import statements to ensure correct relative import resolution before running tests.

- ⚠️ PROHIBITED: DON'T directly click 'Add to Cart' buttons without ensuring that any potential modal overlays are fully loaded and dismissed or that the button is not obscured.

- ✅ PREFERRED: DO implement a retry mechanism with a short delay and a check for modal presence before attempting to click 'Add to Cart' buttons. Consider explicitly dismissing the modal or waiting for it to disappear before clicking.
