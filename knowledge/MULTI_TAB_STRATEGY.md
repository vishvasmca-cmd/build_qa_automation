# 🌐 Multi-Tab & External Link Strategy

## **The "Stay on Target" Policy**

The Autonomous Agent is designed to explore a specific application (the "Target URL").
Modern web apps often link to external sites (Support, Social Media, Corporate Pages) which open in new tabs.
If the Agent wanders into these, it gets lost and fails to complete the workflow.

## **How It Works**

To handle this efficiently and generically, the implementation follows these rules:

1.  **Automatic Detection**: 
    The agent listens for `context.expect_page()` events during every CLICK action.

2.  **Domain Verification**:
    When a new tab opens, the agent compares its domain to your `Target URL`.
    
    *   **Allowed**: Subdomains or same domain.
    *   **Blocked**: Different domains (e.g. going from `parabank.com` to `facebook.com` or `parasoft.com`).

3.  **Action**:
    *   **External Site**: The agent **automatically closes the tab** and returns focus to the main application. Logs: `🛑 External Tab detected. Closing.`
    *   **Internal New Page**: The agent **switches focus** to the new tab and continues exploration.

## **Code Implementation**

Located in `core/explorer.py`:

```python
# Generic Multi-Tab Handler
if base_domain not in new_domain:
    print(f"🛑 External Tab detected ({new_page.url}). Closing.")
    await new_page.close()
    result["new_page"] = None # Stay on old page
else:
    result["new_page"] = new_page # Switch to new page
```

## **Strict Mode Handling**

If a locator matches multiple elements (e.g. "Home" link in header AND footer), standard Playwright errors out ("Strict Mode Violation").
The Agent now handles this generically:
*    Catches the error.
*   Retries the action on the **first** matching element (`locator.first.click()`).
