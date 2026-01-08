
- ⚠️ PROHIBITED: DON'T assume the 'Products' page will load within 30 seconds; implement more robust checks for page content after navigation.

- ✅ PREFERRED: DO implement explicit waits for key elements on the 'Products' page to be visible after clicking the 'Products' link to confirm successful navigation, instead of only checking the URL.

- ⚠️ PROHIBITED: DON'T assume that helper modules are automatically available; ALWAYS verify their existence and correct import paths before running tests.

- ✅ PREFERRED: DO ensure that all necessary helper modules are present and accessible by defining the correct relative or absolute paths in import statements.

- ⚠️ PROHIBITED: DON'T assume helper files are automatically accessible; ALWAYS verify the correct relative or absolute import path.

- ✅ PREFERRED: DO use explicit relative imports (e.g., `from .helpers import take_screenshot`) if the helper file is in the same directory, or configure the PYTHONPATH environment variable for absolute imports.
