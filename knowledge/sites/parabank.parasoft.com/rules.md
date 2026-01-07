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
