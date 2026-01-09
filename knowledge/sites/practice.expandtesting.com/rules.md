
- ⚠️ PROHIBITED: DON'T assume the page is fully loaded immediately after navigation; ALWAYS wait for a specific element or condition to be met before interacting with the page.

- ✅ PREFERRED: DO implement explicit waits for critical elements to appear or for specific network requests to complete, instead of relying solely on load state events.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially on pages with numerous or potentially unreliable external resources. Consider more specific wait conditions.

- ✅ PREFERRED: DO implement more robust page load checks, such as waiting for specific elements to be visible or for key API calls to complete, instead of relying solely on 'networkidle'.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' as a load state, especially on pages with dynamic content or frequent background requests. It can lead to flaky tests due to unpredictable network activity.

- ✅ PREFERRED: DO use more specific and targeted wait conditions, such as waiting for a particular element to be visible or a specific API request to complete, instead of relying solely on 'networkidle'.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test files are explicitly part of a Python package with a properly initialized `__init__.py`.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.verify_custom_expandtesting.base_page import BasePage`) or configure the Python path to correctly resolve relative imports when dealing with test files in a modular project structure.

- ⚠️ PROHIBITED: DON'T use relative imports in test files unless the test execution environment is explicitly configured to handle them correctly.

- ✅ PREFERRED: DO ensure that test files are executed from the root of the project or package, or use absolute imports to avoid relative import errors.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will always resolve correctly without verifying the project's root directory and Python's module search path.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the necessary modules are located in the expected directories relative to the project's root.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are correctly configured without verifying the import paths and file existence.

- ✅ PREFERRED: DO verify the correct relative or absolute import paths for all modules and ensure that the required files exist in the specified locations before running tests.

- ⚠️ PROHIBITED: DON'T assume that relative paths will always resolve correctly; ALWAYS verify the module path.

- ✅ PREFERRED: DO use absolute paths or Python's package structure to ensure correct module resolution.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the import paths in the test files.

- ✅ PREFERRED: DO double-check the project's directory structure and ensure that all import paths in the test files are accurate before running the tests.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the file paths and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and import statements to ensure that all modules are accessible before running the tests.

- ⚠️ PROHIBITED: DON'T assume that the project structure and import paths are correct without verifying them before running the tests.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the import paths in the test files are accurate and reflect the actual project structure.
