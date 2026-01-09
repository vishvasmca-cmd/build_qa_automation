
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
