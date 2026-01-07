
- Before filling the username field, ensure the page is fully loaded and the username input field is visible and enabled. Consider adding a wait_for_selector before attempting to fill the field.

- Before interacting with elements in the footer (like the 'OrangeHRM, Inc' link), ensure any overlaying elements or animations have completed to prevent click interception or unexpected behavior.

- Before clicking 'Forgot your password?', ensure the element is visible and stable. Consider waiting for network activity to settle or for a specific element to load before attempting to click.

- When clicking the 'OrangeHRM, Inc' link, implement a retry mechanism with a short delay between attempts, as the element might become momentarily unresponsive despite appearing stable.

- Before attempting to click 'Forgot your password', ensure that any overlaying elements (e.g., modals, banners) are dismissed or that the element is fully visible and interactable. Consider adding a short explicit wait for the element to be visible and enabled.

- If a link is visible, enabled and stable but click action times out, try to use JavaScript click or force click.

- When navigating to the password reset page, implement a retry mechanism with exponential backoff to handle potential slow server responses or intermittent network issues. Also, verify that the password reset link is correctly configured and reachable.

- Before interacting with elements in the top navigation bar, ensure the page has fully loaded and any initial animations or transitions have completed. Consider using `locator.wait_for()` with `state='visible'` or `state='stable'` before attempting to click.

- When interacting with elements in the OrangeHRM header, especially navigation links, implement retry logic with exponential backoff to handle potential intermittent loading issues or animations that might delay element availability. Consider using more robust locators than full XPaths.

- When navigating to the login page, implement a retry mechanism with exponential backoff to handle potential network or server delays. Also, verify the page content instead of relying solely on URL matching, as redirects might occur.

- Before clicking 'Forgot your password?', ensure no overlays or modals are present that might obscure the element or prevent it from being interacted with. Check for dynamic content loading that might delay the appearance of the element.

- Before clicking 'Forgot your password?', ensure no modal dialogs or overlays are present that might obscure the element. Also, consider adding a short wait or retry mechanism specifically for this element.

- Before attempting to click 'Forgot your password?', ensure the element is both visible and enabled. Consider adding a short explicit wait with error handling.

- When asserting URL changes after an action, use a precise and complete URL string or a more accurate regular expression to avoid false negatives due to minor URL variations.

- When navigating to the password reset page, anticipate potential delays in network activity and consider increasing the default timeout or explicitly waiting for a specific element to load before proceeding.

- When navigating to the password reset page, anticipate potential delays in resource loading. Increase the default timeout or implement a more robust loading check than 'networkidle', such as waiting for a specific element to be present.

- Before clicking 'Forgot your password', ensure no modal dialogs or overlays are present that might obscure the link. If a modal is present, dismiss it before proceeding.

<<<<<<< Updated upstream
- Before clicking the 'Forgot your password' link, ensure no modal dialogs or overlays are present that might obscure the element. If a modal is present, dismiss it before attempting to click the link.

- When asserting URL patterns, ensure the pattern accurately reflects the expected URL structure, including any prefixes or suffixes. Prefer exact match when possible.

- When asserting the current URL, prefer exact string matching or a more specific regex over glob patterns, especially when the expected substring is present in the actual URL.
=======
- Before filling the username field on the OrangeHRM login page, ensure the page is fully loaded and the username field is visible. Consider adding a wait_for_selector or wait_for_load_state before attempting to fill the field.
>>>>>>> Stashed changes

- After submitting a password reset request, verify that the application redirects to a confirmation page or displays a success message before redirecting to the login page. Do not immediately expect a redirect to the login page.

- After submitting a password reset request, always check for the success message on the same page before assuming a redirect or further action is needed.

- After submitting a password reset request, explicitly wait for the 'Reset Password link sent successfully' message to appear before proceeding with assertions.  Consider using a longer timeout or a more robust locator strategy.

- When navigating to the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- When navigating to a new page, especially the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- When navigating to a new page, especially the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- Before attempting to fill the 'Username' field, explicitly wait for the form or relevant section to be fully loaded. Consider using a more robust locator strategy if labels are unreliable.

- When navigating to the OrangeHRM login page, implement a retry mechanism with exponential backoff to handle potential delays in redirection. Also, check for common blocking elements like modals or banners before waiting for the URL.

- When navigating to a new page, especially the login page, increase the timeout to accommodate potential server delays or network latency. Consider implementing a retry mechanism with exponential backoff.

- When navigating to an external URL, implement a retry mechanism with exponential backoff to handle potential network instability or temporary website unavailability. Also, verify the target URL before navigation.

- When interacting with elements in the top navigation bar of OrangeHRM, implement a retry mechanism with exponential backoff to handle potential loading delays or intermittent visibility issues. Before clicking, explicitly wait for the element to be both visible and enabled.

- When clicking on elements within the OrangeHRM header/navigation, implement a retry mechanism with exponential backoff, as network conditions or server-side processing might cause intermittent delays. Also, consider using more resilient locators based on text content or ARIA roles instead of brittle XPaths.

- When asserting the presence of text on a page in Playwright, use `expect(page.locator('body')).to_have_text('expected text')` or `expect(page.locator('selector')).to_have_text('expected text')` instead of `expect(page).to_have_text('expected text')`.

- When asserting the success message after a password reset request, use a more specific locator to target the message element, avoiding the surrounding HTML structure.

- When asserting the presence of specific text after an action that triggers a page update (like submitting a password reset request), target a more specific locator than the entire 'body' to avoid interference from surrounding HTML and whitespace. Also, trim the actual value before comparison.
