
- Before running tests, verify the SSL certificate of the target website. If the certificate is invalid, the test should be skipped or a warning should be raised.

- Before running tests, verify the SSL certificate of the target website. If an invalid certificate is detected, either skip the test or configure Playwright to bypass SSL certificate validation for the specific domain in the test environment.
