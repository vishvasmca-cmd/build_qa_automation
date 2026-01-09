
- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially on dynamic sites with ongoing background requests.

- ✅ PREFERRED: DO implement more specific and targeted waits for key elements or API calls to complete, rather than relying on general load states.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially on pages with many asynchronous resources. It can be unreliable.

- ✅ PREFERRED: DO implement more specific and targeted waits for key elements or resources to load, rather than relying on general load states.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially for dynamic websites with many asynchronous requests.

- ✅ PREFERRED: DO implement more specific and targeted waits for key elements or resources to be available before proceeding with interactions.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially on dynamic sites with continuous background requests.

- ✅ PREFERRED: DO implement more specific and targeted waits for key elements or events that signify the page is ready for interaction, rather than a general 'networkidle' wait.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially on pages with many asynchronous resources. It can be unreliable.

- ✅ PREFERRED: DO implement more specific and targeted waits for key elements or resources to load, rather than relying on generic load states.

- ⚠️ PROHIBITED: DON'T rely solely on 'networkidle' for page load completion, especially on pages with potentially long-running or unreliable network requests.

- ✅ PREFERRED: DO implement more specific and targeted waits for critical elements or resources to be available before proceeding with interactions.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined package or use absolute imports to reference modules within the project.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in the parent directory.

- ✅ PREFERRED: DO ensure that test files using relative imports are part of a properly structured Python package, or use absolute imports instead.

- ⚠️ PROHIBITED: DON'T rely on relative imports within test files unless the test suite is executed from the project root directory using `pytest` command.

- ✅ PREFERRED: DO ensure that test files are part of a properly structured Python package and that pytest is invoked from the project root to correctly resolve relative imports. Alternatively, use absolute imports.

- ⚠️ PROHIBITED: DON'T run individual test files that rely on relative imports directly. ALWAYS execute tests from the project root using pytest.

- ✅ PREFERRED: DO ensure that tests using relative imports are run as part of a package by invoking pytest from the project's root directory.
