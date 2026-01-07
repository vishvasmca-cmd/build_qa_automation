
- Before running tests, verify the SSL certificate of the target website. If the certificate is invalid, the test should be skipped or a warning should be raised.

- Before running tests, verify the SSL certificate of the target website. If an invalid certificate is detected, either skip the test or configure Playwright to bypass SSL certificate validation for the specific domain in the test environment.

- Always import necessary modules (e.g., `re` for regular expressions) at the beginning of the file to avoid `NameError` exceptions during test execution.

- Before asserting the page title, check for SSL certificate errors and handle them gracefully (e.g., by retrying or skipping the test).

- If the page title contains 'Invalid SSL certificate', the test should either be skipped or the SSL certificate issue should be resolved before proceeding.

- Always import necessary modules (e.g., `re` for regular expressions) at the beginning of the test file to avoid `NameError` exceptions.
