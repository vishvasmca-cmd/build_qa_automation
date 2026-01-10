
- ⚠️ PROHIBITED: DON'T assume the 'Enter Country' field is immediately available; it might be dynamically loaded or require a specific state to be visible.

- ✅ PREFERRED: DO implement explicit waiting mechanisms (e.g., `wait_for_selector`, `wait_for_element_state`) before attempting to interact with the 'Enter Country' field to ensure it's fully loaded and visible.

- ⚠️ PROHIBITED: DON'T rely on partial text matches or generic class names like `.ui-menu-item div` when targeting elements in dynamically generated lists. These are prone to ambiguity.

- ✅ PREFERRED: DO use exact text matches, unique attributes (e.g., IDs), or chain locators to precisely target the desired element in dynamic lists. Leverage `nth()` or `first()` if necessary after narrowing down the selection.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test runner is explicitly configured to handle them correctly. Prefer absolute imports or adjust the PYTHONPATH.

- ✅ PREFERRED: DO ensure that all modules and packages are correctly structured and that import paths are resolvable by the test runner. Use absolute imports or configure the test environment to correctly resolve relative imports.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import Class`) in test files unless the test execution environment is explicitly configured to support them and the package structure is correctly initialized with `__init__.py` files.

- ✅ PREFERRED: DO use absolute imports (e.g., `from project.package.module import Class`) or configure the PYTHONPATH environment variable to ensure the test runner can correctly resolve module dependencies.

- ⚠️ PROHIBITED: DON'T use relative imports within test files unless the test suite is explicitly structured as a package with proper `__init__.py` files and the test runner is invoked from the package root.

- ✅ PREFERRED: DO ensure that test files either use absolute imports or, if relative imports are necessary, that the test suite is correctly structured as a Python package and the test runner is invoked from the package root.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports or configure the test runner to correctly handle relative imports by ensuring the test directory is treated as a package. Consider restructuring the project or modifying the import statements.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports or configure the test runner to correctly handle relative imports by ensuring the test directory is treated as a package.

- ⚠️ PROHIBITED: DON'T use relative imports in test files unless the test execution environment is explicitly configured to handle them correctly.

- ✅ PREFERRED: DO ensure that test files are executed from the package root or use absolute imports to avoid `ImportError` related to relative paths.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.verify_custom_rahulshetty.base_page import BasePage`) or configure the test runner to correctly handle relative imports by structuring the project as a package.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports or configure the test runner to correctly handle relative imports by ensuring the test directory is treated as a package.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test runner is explicitly configured to handle them correctly.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.verify_custom_rahulshetty.base_page import BasePage`) or configure the test runner to recognize the package structure for relative imports.

- ⚠️ PROHIBITED: DON'T run individual test files that rely on relative imports directly. ALWAYS execute tests from the project root using pytest.

- ✅ PREFERRED: DO ensure that all test files are part of a properly structured Python package with a `__init__.py` file in each directory if relative imports are used.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package and executed accordingly.

- ✅ PREFERRED: DO ensure that test files either use absolute imports or are executed as part of a properly defined Python package when using relative imports.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py`.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined Python package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package and executed accordingly.

- ✅ PREFERRED: DO ensure that test files either use absolute imports or are executed as part of a properly defined Python package to resolve import errors.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package and executed as such.

- ✅ PREFERRED: DO ensure that test files are either executed as part of a properly structured package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py`.

- ✅ PREFERRED: DO ensure that test files are either part of a properly defined Python package or use absolute imports to reference modules.

- ⚠️ PROHIBITED: DON'T use relative imports within test files unless the test suite is explicitly structured and executed as a Python package.

- ✅ PREFERRED: DO use absolute imports or configure the test runner to correctly handle relative imports when working with test modules that rely on them.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) when running tests outside of a package context.  Prefer absolute imports or configure the test runner to treat the directory as a package.

- ✅ PREFERRED: DO ensure that test files are part of a properly structured Python package or use absolute imports to avoid relative import errors.  Alternatively, adjust the PYTHONPATH or use pytest's `--import-mode` option.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package with a proper `__init__.py` file in each directory.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.verify_custom_rahulshetty.tests.base_page import BasePage`) or configure the test runner to correctly handle relative imports by structuring the project as a package.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test suite is explicitly structured as a package and executed accordingly.

- ✅ PREFERRED: DO ensure that test files either use absolute imports or are executed as part of a properly defined Python package when using relative imports.

- ⚠️ PROHIBITED: DON'T use relative imports within test files unless the test suite is explicitly structured as a package and executed from the package root.

- ✅ PREFERRED: DO ensure that test files either use absolute imports or that the test execution environment correctly sets up the package context for relative imports to resolve correctly.
