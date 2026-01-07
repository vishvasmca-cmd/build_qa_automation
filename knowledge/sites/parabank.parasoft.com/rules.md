# Parabank Specific Rules

## Navigation & Strict Mode
- **STRICT MODE VIOLATION**: Common links like "About Us", "Services", "Admin Page" appear in both the Header and Footer.
  - **ACTION**: When clicking these common links, ALWAYS clarify the container or use `.first`.
  - **PREFERRED**: `page.locator("#headerPanel").get_by_role("link", name="About Us")`
  - **ALTERNATIVE**: `page.get_by_role("link", name="About Us").first`

## Login
- **LOGIN SUCCESS**: Successful login redirects to `/parabank/overview.htm`.
- **LOGIN FAILURE**: Failure usually keeps you on `index.htm` or shows specific error text "The username and password could not be verified".
