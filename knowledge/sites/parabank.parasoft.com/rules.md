# Parabank Specific Rules

## Navigation & Strict Mode
- **STRICT MODE VIOLATION**: Common links like "About Us", "Services", "Admin Page" appear in both the Header and Footer.
  - **ACTION**: When clicking these common links, ALWAYS clarify the container or use `.first`.
  - **PREFERRED**: `page.locator("#headerPanel").get_by_role("link", name="About Us")`
  - **ALTERNATIVE**: `page.get_by_role("link", name="About Us").first`

- **HOME LINK**: "Home" link also appears multiple times. Use `exact=True` or header scope.
  - **PREFERRED**: `page.get_by_role("link", name="Home", exact=True).first`

## Login
- **LOGIN SUCCESS**: Successful login redirects to `/parabank/overview.htm`.
- **LOGIN FAILURE**: Failure usually keeps you on `index.htm` or shows specific error text "The username and password could not be verified".

## Account History & Server Stability
- **WADL REDIRECT**: Clicking "Account History" sometimes redirects to a WADL/Service description page instead of `/account.htm`.
  - **ACTION**: Verify URL contains `/account.htm` (or `/accountactivity.htm`). If it contains `_wadl` or ends in `.xml`, it is a server-side error.
  - **RECOVERY**: Implement retry mechanism with page refresh if WADL page is encountered.

- **URL VERIFICATION**: Ensure `expect(page).to_have_url()` regex is strictly formatted to avoid partial matches on wrong pages.

- When targeting elements that may appear in both the header and footer, use more specific locators to avoid ambiguity.  Prioritize locators scoped to a specific container (e.g., header or footer) or use nth=0/1 to target the correct element.

- Before clicking 'Account History', ensure the user is logged in and the account summary page is fully loaded. Implement a visual check or state check to confirm readiness.

- When using `to_have_url` with a regular expression, ensure the regex is a properly formatted string.

- When navigating to account history, implement a retry mechanism with exponential backoff to handle potential slow server responses or intermittent network issues. Also, verify the user is logged in before attempting to navigate to the account history page.

- When navigating to account details, implement a retry mechanism with exponential backoff if the initial navigation times out. Also, verify the user is logged in before attempting to access account details.

- When navigating to account history, check for common error messages or loading indicators on the page before waiting for the final URL. The ParaBank application is known to have intermittent performance issues.

<<<<<<< Updated upstream
- After clicking 'Account History', check for a redirect to the API endpoint '/services/bank' and, if present, retry the click or report the error.

- Before navigating to 'Account History', ensure all page elements are fully loaded and any potential overlays or animations are complete. Consider adding a short explicit wait if necessary.

- Before navigating to 'Account History', ensure all page elements are fully loaded and any potential overlays or animations are complete. Consider adding a short delay or explicit wait condition.
=======
- If navigation to Account History results in a redirect to '/services/bank', retry the navigation after a short delay, as this might be a transient server-side issue. Consider adding a conditional check for this redirect.

- When navigating to the ParaBank homepage, the 'Home' link may not be immediately available. Implement a retry mechanism or increase the timeout to accommodate potential delays.
>>>>>>> Stashed changes

- When using `get_by_role` with a regular expression for link names, especially with `re.IGNORECASE`, ensure the expression is specific enough to resolve to a single, unique element.  Consider using `exact=True` if the target link's capitalization is known and consistent, or refine the regex to be more precise.

- When locating elements with text that might have inconsistent casing, prefer exact matches or use `first` or `last` to disambiguate if multiple matches are expected.  Alternatively, disable strict mode only when necessary and with caution.

- When locating elements with text 'Home' (case-insensitive) on ParaBank, be aware that multiple elements may match. Use a more specific locator or consider using `first` or `last` to resolve ambiguity, or disable strict mode if appropriate.

- When navigating to account history, implement a retry mechanism with a short delay to handle potential intermittent server delays or network issues. Also, verify successful login before navigating.

- Before navigating to 'Account History', ensure that all loading elements or overlays are fully dismissed. Consider adding an explicit wait for the page to fully load before interacting with elements.

- Before clicking 'Account History', ensure the page is fully loaded and any overlays or animations are complete. Consider adding a short explicit wait for the element to be visible and stable.
