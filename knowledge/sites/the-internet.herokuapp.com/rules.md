
- ⚠️ PROHIBITED: DON'T assume successful login based solely on immediate element visibility; always verify the user's logged-in state through a more robust mechanism (e.g., checking user profile data).

- ✅ PREFERRED: DO implement explicit waits or retries for elements that appear after asynchronous operations, such as login, to ensure they are fully rendered and visible before assertion.

- ⚠️ PROHIBITED: DON'T define methods without parentheses, even if they don't take arguments.

- ✅ PREFERRED: ALWAYS ensure that all method definitions include parentheses, even if they are empty (e.g., `def username_input():`).
