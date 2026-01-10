
- ⚠️ PROHIBITED: DON'T assume immediate navigation after clicking the signup button; always account for potential delays due to network latency or server-side processing.

- ✅ PREFERRED: DO implement explicit waits with increased timeout or retry logic after clicking navigation-triggering elements, especially for signup/login flows.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test runner is explicitly configured to handle the package structure correctly.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.verify_custom_thinking_tester.base_page import BasePage`) or configure the test runner to recognize the package structure when using relative imports.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project's directory structure and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and import statements to ensure that all modules are accessible and correctly referenced.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project's directory structure and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and import statements to ensure that all modules are accessible and correctly referenced.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project structure and import statements.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the required modules exist in the specified locations before running the tests.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correctly configured in the CI environment without verifying the PYTHONPATH or similar environment variables.

- ✅ PREFERRED: DO explicitly define the PYTHONPATH or use relative imports within the project to ensure modules can be located correctly, especially in CI/CD environments.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the import paths in the test files.

- ✅ PREFERRED: DO double-check the project's directory structure and ensure that all import statements correctly reflect the location of the modules.

- ⚠️ PROHIBITED: DON'T assume that the file structure is correct without verifying the file paths in the import statements.

- ✅ PREFERRED: DO double-check the file paths in import statements and ensure that the referenced modules exist in the specified locations.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the file structure and naming conventions.

- ✅ PREFERRED: DO double-check the project's directory structure and module naming to ensure correct import paths before running tests.

- ⚠️ PROHIBITED: DON'T assume that the file structure is correct without verifying the file paths in the import statements.

- ✅ PREFERRED: DO double-check the file paths in import statements and ensure that the required modules exist in the specified locations.

- ⚠️ PROHIBITED: DON'T assume that the project structure and import paths are correct without verifying them before each test run, especially after changes to the codebase.

- ✅ PREFERRED: DO verify the project's directory structure and module import paths to ensure that all necessary modules can be imported correctly before running tests.
