import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Override default browser context arguments.
    Sets a standard viewport and user agent to avoid bot detection/rendering issues.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
