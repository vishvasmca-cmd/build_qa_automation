import sys
import os
import json

# Add core to path
sys.path.append(os.path.join(os.getcwd(), "core"))

from feedback_agent import FeedbackAgent

log_content = """
FAILED projects/core_parabank/tests/test_main.py::test_autonomous_flow[chromium]
E           playwright._impl._errors.Error: Locator.click: Error: strict mode violation: get_by_role("link", name="Home") resolved to 2 elements:
E               1) <a href="index.htm">home</a> aka get_by_role("link", name="home", exact=True)
E               2) <a href="index.htm">Home</a> aka get_by_role("link", name="Home", exact=True)
"""

config = {
    "project_name": "core_parabank",
    "target_url": "https://parabank.parasoft.com/index.htm",
    "domain": "banking"
}

# Create dummy config file because analyze_run expects a path
with open("temp_config.json", "w") as f:
    json.dump(config, f)

agent = FeedbackAgent()
print("Running analyze_run...")
agent.analyze_run("temp_config.json", log_content, success=False)
