
- ⚠️ PROHIBITED: DON'T assume a navigation will complete within the default timeout, especially after clicking a button that triggers a complex server-side operation.

- ✅ PREFERRED: DO explicitly set a longer timeout for navigation events when the target page is known to be slow or dependent on external services.

- ⚠️ PROHIBITED: DON'T rely on immediate navigation after an action; always anticipate potential delays due to network latency or server-side processing.

- ✅ PREFERRED: DO implement explicit waits or retries when navigating to pages, especially when the navigation is triggered by an action that might take time to process.

- ⚠️ PROHIBITED: DON'T use relative imports (e.g., `from .module import X`) in test files unless the test runner is explicitly configured to handle them correctly. Prefer absolute imports or configure pytest to recognize the package structure.

- ✅ PREFERRED: DO use absolute imports (e.g., `from projects.stress_verify_custom_qapractice.tests.e2e.base_page import BasePage`) or configure pytest to recognize the package structure by adding an `__init__.py` file to the `projects/stress_verify_custom_qapractice/tests/e2e` directory and any parent directories that need to be treated as packages.
