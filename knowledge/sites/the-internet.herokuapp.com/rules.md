
- ⚠️ PROHIBITED: DON'T assume successful login based solely on immediate element visibility; always verify the user's logged-in state through a more robust mechanism (e.g., checking user profile data).

- ✅ PREFERRED: DO implement explicit waits or retries for elements that appear after asynchronous operations, such as login, to ensure they are fully rendered and visible before assertion.

- ⚠️ PROHIBITED: DON'T define methods without parentheses, even if they don't take arguments.

- ✅ PREFERRED: ALWAYS ensure that all method definitions include parentheses, even if they are empty (e.g., `def username_input():`).

- ⚠️ PROHIBITED: DON'T assume a successful login solely based on URL redirection; ALWAYS verify the presence of a unique element on the target page (e.g., the Logout button) to confirm a successful login.

- ✅ PREFERRED: DO implement explicit waits for key elements (like the Logout button) to appear after navigation, especially after login, to account for potential delays in page rendering.

- ⚠️ PROHIBITED: DON'T define methods without parentheses, even if they don't take arguments beyond 'self'.

- ✅ PREFERRED: ALWAYS ensure that all method definitions include parentheses, e.g., `def username_input(self):`.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the file paths and import statements.

- ✅ PREFERRED: DO verify the project's directory structure and import statements before running tests to ensure all modules are accessible.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the import paths in the test files.

- ✅ PREFERRED: DO verify the project's directory structure and import paths to ensure that all modules can be found during test execution.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the import paths in the test files.

- ✅ PREFERRED: DO verify the project's directory structure and import paths to ensure that all modules can be found during test execution.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the project's root directory is correctly configured for pytest.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the project's root directory is correctly configured for pytest to resolve imports.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the project's root directory is correctly configured for pytest.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the project's root directory is correctly configured for pytest to resolve imports.

- ⚠️ PROHIBITED: DON'T assume that the project structure is correct without verifying the file paths and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and import statements to ensure that all modules are accessible.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the project's root directory is correctly configured for pytest.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the project's root directory is correctly configured for pytest to resolve imports.

- ⚠️ PROHIBITED: DON'T assume that the project's directory structure and import paths are correct without verifying them before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the import paths in the test files are accurate and reflect the project's directory structure.
