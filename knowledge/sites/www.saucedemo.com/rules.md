
- ⚠️ PROHIBITED: DON'T assume the username input field is immediately available; always implement a retry mechanism or explicit wait for its presence.

- ✅ PREFERRED: DO use `page.locator('input#user-name')` to locate the username field, as it's more specific and less prone to text-based matching issues.

- ⚠️ PROHIBITED: DON'T rely solely on `has_text` filter for input fields, especially when the text might be a placeholder or subject to change.

- ✅ PREFERRED: DO use more robust and specific locators, such as `input[name='username']` or `input#username`, and verify element visibility before interacting with it.
