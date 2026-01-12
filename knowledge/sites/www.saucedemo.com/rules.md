
- ⚠️ PROHIBITED: DON'T assume the username input field is immediately available; always implement a retry mechanism or explicit wait for its presence.

- ✅ PREFERRED: DO use `page.locator('input#user-name')` to locate the username field, as it's more specific and less prone to text-based matching issues.
