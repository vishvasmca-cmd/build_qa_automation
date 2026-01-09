
- Before running tests, verify the SSL certificate of the target website. If the certificate is invalid, the test should be skipped or a warning should be raised.

- Before running tests, verify the SSL certificate of the target website. If an invalid certificate is detected, either skip the test or configure Playwright to bypass SSL certificate validation for the specific domain in the test environment.

- Always import necessary modules (e.g., `re` for regular expressions) at the beginning of the file to avoid `NameError` exceptions during test execution.

- Before asserting the page title, check for SSL certificate errors and handle them gracefully (e.g., by retrying or skipping the test).

- If the page title contains 'Invalid SSL certificate', the test should either be skipped or the SSL certificate issue should be resolved before proceeding.

- Always import necessary modules (e.g., `re` for regular expressions) at the beginning of the test file to avoid `NameError` exceptions.

- Always import necessary modules (e.g., `re` for regular expressions) at the beginning of the test file to avoid `NameError` exceptions.

- Always import necessary modules (e.g., `re` for regular expressions) at the beginning of the test file to avoid `NameError` exceptions during runtime.

- Before proceeding with any tests, validate the SSL certificate of the target website. If the certificate is invalid, halt the test execution and report the issue.

- Before proceeding with any tests, always validate the SSL certificate of the target website. If the certificate is invalid, halt the test execution and report the issue.

- Before running tests, verify the SSL certificate of the target website. If the certificate is invalid, halt the test execution or use a different environment with a valid certificate.

- ⚠️ PROHIBITED: DON'T use the `ignore_https_errors` argument when launching a browser with Playwright, as it is deprecated and will cause a TypeError.

- ✅ PREFERRED: DO check the Playwright documentation for the correct arguments to use when launching a browser, and update your code accordingly. Consider using a different approach to handle HTTPS errors, such as configuring the browser context or using a proxy.

- ⚠️ PROHIBITED: DON'T assume that all module dependencies are automatically resolved; ALWAYS verify the correct project structure and import paths.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python interpreter can locate them by correctly structuring the project and setting up the PYTHONPATH environment variable if needed.

- ⚠️ PROHIBITED: DON'T proceed with the test if an SSL certificate error is detected on the page. The application under test is not trustworthy.

- ✅ PREFERRED: DO ensure the test environment has a valid and trusted SSL certificate configured before running tests that require secure connections.

- ⚠️ PROHIBITED: DON'T assume the Magento instance has a valid SSL certificate in the test environment. ALWAYS handle potential SSL errors gracefully.

- ✅ PREFERRED: DO implement a mechanism to bypass or accept invalid SSL certificates when running tests against environments with self-signed or misconfigured SSL certificates.

- ⚠️ PROHIBITED: DON'T proceed with the test flow if the initial SSL certificate check fails. Halt execution and report the error immediately.

- ✅ PREFERRED: DO implement robust SSL certificate validation and handling at the beginning of the test flow, including retries or bypassing validation in controlled test environments if necessary.

- ⚠️ PROHIBITED: DON'T assume the test environment automatically trusts the target website's SSL certificate; ALWAYS explicitly handle potential SSL certificate validation issues.

- ✅ PREFERRED: DO implement robust SSL certificate validation handling, including options to bypass validation in controlled test environments or to use a trusted certificate authority.

- ⚠️ PROHIBITED: DON'T assume the SSL certificate is valid without explicitly handling potential SSL errors or configuring the browser to trust the certificate.

- ✅ PREFERRED: DO implement robust SSL certificate validation or bypass mechanisms in the test setup, especially when testing against environments with self-signed or untrusted certificates.

- ⚠️ PROHIBITED: DON'T proceed with the test flow if the initial SSL certificate check fails. Halt execution and report the error immediately.

- ✅ PREFERRED: DO implement a robust SSL certificate validation mechanism within the test setup, potentially including custom certificate handling or ignoring SSL errors in controlled environments only.

- ⚠️ PROHIBITED: DON'T assume a valid SSL certificate is present; ALWAYS implement robust SSL error handling and certificate validation bypass mechanisms when testing against potentially misconfigured environments.

- ✅ PREFERRED: DO implement a mechanism to bypass or accept invalid SSL certificates during test execution, especially in non-production environments, or configure the test environment to trust the certificate.

- ⚠️ PROHIBITED: DON'T assume the SSL certificate is valid without explicitly handling potential SSL errors or exceptions during the initial navigation step.

- ✅ PREFERRED: DO implement robust SSL certificate validation and error handling, including retries or bypassing certificate checks in controlled test environments where appropriate.
