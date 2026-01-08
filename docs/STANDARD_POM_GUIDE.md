# Standard Playwright POM Generation Guide

This document defines the **Mandatory Standard** for generating Playwright automation projects.
**ALL** future code generation must strictly adhere to this file structure and coding style.

## 1. Directory Structure
The project **MUST** follow this exact directory layout. Do not invent new folders (like `utils` or `helpers`) unless explicitly requested.

```text
projects/
  <project_name>/
    ├── __init__.py                # Empty file
    ├── config.json                # Test configuration and plans
    ├── pages/                     # Page Object Models
    │   ├── __init__.py            # Empty file
    │   ├── base_page.py           # Base class (Mandatory)
    │   ├── home_page.py           # Main landing page (Mandatory)
    │   ├── login_page.py          # Login/Logout functionality (Mandatory)
    │   └── <feature>_page.py      # App-specific pages (e.g., cart_page.py)
    ├── tests/
    │   ├── __init__.py            # Empty file
    │   └── e2e/
    │       ├── __init__.py        # Empty file
    │       ├── conftest.py        # Pytest fixtures
    │       └── test_main.py       # Linear test execution
    └── outputs/                   # (Gitignored) Artifacts like screenshots
```

---

## 2. Step-by-Step Generation Instructions

### Step 1: Configuration (`config.json`)
Create `config.json` at the project root.
*   **Must** include `paths` for trace, test, and report.
*   **Must** include `master_plan` with test scenarios.

```json
{
  "project_name": "<project_name>",
  "target_url": "https://example.com",
  "paths": {
    "trace": "projects/<project_name>/outputs/trace.json",
    "test": "projects/<project_name>/tests/e2e/test_main.py",
    "report": "projects/<project_name>/outputs/playwright-report"
  },
  "master_plan": "# Test Plan..."
}
```

### Step 2: The Base Page (`pages/base_page.py`)
This is the parent class. **Copy this exactly.**

```python
from playwright.sync_api import Page, expect

class BasePage:
    """
    Base Page Object class that all other pages inherit from.
    Contains common methods and the shared Page instance.
    """
    def __init__(self, page: Page):
        """Initialize with a Playwright Page instance."""
        self.page = page

    def navigate(self, url: str):
        """Navigate to the specified URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()
```

### Step 3: Page Objects (`pages/<name>_page.py`)
*   **Inheritance**: Must inherit from `BasePage`.
*   **Locators**: Use `@property` for all locators. Use strictly standard Playwright locators (`get_by_role`, `get_by_text`, `locator`).
*   **Actions**: Methods should represent user actions, not implementation details.
*   **Documentation**: Include one docstring per class and method.

**Template:**
```python
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    """Page Object for the Login page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # --- Locators ---
    @property
    def username_input(self):
        """Locator for username field."""
        return self.page.get_by_placeholder("Username")

    @property
    def login_button(self):
        """Locator for login ID."""
        return self.page.get_by_role("button", name="Log in")

    # --- Actions ---
    def login(self, user: str, password: str):
        """Perform full login flow."""
        self.username_input.fill(user)
        # ... fill logic ...
        self.login_button.click()
```

### Step 4: Login Page (`pages/login_page.py`)
**Mandatory File**. Handles authentication.

```python
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object for Login/Logout pages.
    """
    def __init__(self, page: Page):
        super().__init__(page)

    # Locators
    @property
    def email_input(self):
        return self.page.locator("form[action='/login'] input[name='email']")

    @property
    def password_input(self):
        return self.page.get_by_placeholder("Password")

    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Login")

    @property
    def logout_link(self):
        return self.page.get_by_role("link", name="Logout")

    # Actions
    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def logout(self):
        self.logout_link.click()
```

### Step 5: Test Configuration (`tests/e2e/conftest.py`)
Define the browser viewport here to ensure consistent screenshotting and headless rendering.

```python
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
```

### Step 5: The Test Execution (`tests/e2e/test_main.py`)
*   **Single Entry Point**: Logic should be in `test_autonomous_flow`.
*   **Fixture**: Use `page` fixture (NOT `browser`).
*   **Linear Flow**: Instantiate pages at top, then call actions sequentially.
*   **No Utils**: Do not import helper functions. Use `home_page.navigate(...)`.
*   **Reporting**: Use standard `page.screenshot` for final state.

**Template:**
```python
import sys
import os
from playwright.sync_api import Page
# Add project root to path if needed for imports
sys.path.append(os.getcwd())

from projects.<project_name>.pages.home_page import HomePage
from projects.<project_name>.pages.login_page import LoginPage

def test_autonomous_flow(page: Page):
    """
    Linear regression test for <project_name>.
    """
    # 1. Initialize Pages
    home = HomePage(page)
    login = LoginPage(page)

    # 2. Sequential Logic
    print("Navigating...")
    home.navigate("https://example.com")
    
    print("Logging in...")
    home.go_to_login()
    login.login("user", "pass")
    
    # 3. Final Artifact
    print("Taking screenshot...")
    page.screenshot(path="projects/<project_name>/outputs/final_state.png")
```

---

## 3. Reporting
Run tests using the standard Playwright tracing flag.
Do not use custom HTML reporters.

```bash
pytest projects/<project_name>/tests/e2e/test_main.py --tracing=on
```
