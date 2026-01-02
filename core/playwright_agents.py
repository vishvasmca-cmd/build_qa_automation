"""
Enhanced Test Generation using Playwright's Native Tools

Architecture:
1. Planner Agent: Analyzes spec → Creates test plan
2. Builder Agent: Uses Playwright Codegen → Records actions
3. Executor Agent: Runs tests → Captures traces
4. Healer Agent: Analyzes failures → Suggests fixes
"""

import asyncio
import subprocess
import os
import json
from playwright.async_api import async_playwright

class PlaywrightPlanner:
    """
    Planning Agent: Creates test strategy from goal
    """
    def __init__(self, url, goal, domain):
        self.url = url
        self.goal = goal
        self.domain = domain
    
    def create_test_plan(self):
        """
        Generates structured test plan
        Returns:
            {
                "steps": [
                    {"action": "navigate", "target": url},
                    {"action": "click", "target": "Login button"},
                    {"action": "fill", "target": "username", "value": "..."},
                    {"action": "assert", "target": "url", "expected": "dashboard"}
                ],
                "checkpoints": ["Login success", "Dashboard loads"],
                "cleanup": ["Logout", "Close browser"]
            }
        """
        # LLM generates plan based on goal + domain knowledge
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)
        
        prompt = f"""
You are a Test Planning Agent.

Create a detailed test plan for:
Domain: {self.domain}
URL: {self.url}
Goal: {self.goal}

Output JSON with this structure:
{{
  "test_name": "descriptive_name",
  "steps": [
    {{"step": 1, "action": "navigate", "target": "{self.url}"}},
    {{"step": 2, "action": "click", "target": "CSS selector or text", "description": "Click login button"}},
    {{"step": 3, "action": "fill", "target": "input[name='username']", "value": "testuser"}},
    {{"step": 4, "action": "assert", "type": "url", "expected": "dashboard"}}
  ],
  "test_data": {{
    "username": "test@example.com",
    "password": "Pass123"
  }}
}}

Be specific with selectors. Use data-test attributes when mentioning forms.
"""
        
        resp = llm.invoke(prompt)
        plan = json.loads(resp.content.replace("```json", "").replace("```", "").strip())
        return plan

class PlaywrightBuilder:
    """
    Builder Agent: Uses Playwright Codegen to record test
    """
    def __init__(self, url, plan):
        self.url = url
        self.plan = plan
    
    def generate_with_codegen(self, output_file):
        """
        Opens Playwright Codegen in headed mode
        User can manually perform actions
        Playwright records them automatically
        
        Alternative: Use plan to guide automated recording
        """
        print("🎬 Starting Playwright Codegen...")
        print(f"   Target: {self.url}")
        print(f"   Output: {output_file}")
        print(f"\n📋 Follow this plan:")
        for step in self.plan['steps']:
            print(f"   {step['step']}. {step['action'].upper()}: {step.get('description', step.get('target', ''))}")
        
        # Option 1: Manual recording (user-guided)
        cmd = [
            "playwright",
            "codegen",
            self.url,
            "--target", "python-pytest",
            "--output", output_file,
            "--viewport-size", "1280,720"
        ]
        
        subprocess.run(cmd)
        
        print(f"✅ Test recorded to {output_file}")
        return output_file
    
    async def generate_programmatic(self, output_file):
        """
        Automated recording based on plan
        Uses Playwright API to record actions
        """
        async with async_playwright() as p:
            # Enable trace recording
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            
            # Start tracing
            await context.tracing.start(screenshots=True, snapshots=True, sources=True)
            
            page = await context.new_page()
            
            test_code = []
            test_code.append("import pytest")
            test_code.append("from playwright.sync_api import Page, expect\n")
            test_code.append("def test_auto_generated(page: Page):")
            
            for step in self.plan['steps']:
                action = step['action']
                target = step.get('target', '')
                value = step.get('value', '')
                
                if action == 'navigate':
                    await page.goto(target)
                    test_code.append(f'    page.goto("{target}")')
                
                elif action == 'click':
                    # Record the click
                    test_code.append(f'    page.locator("{target}").click()')
                
                elif action == 'fill':
                    test_code.append(f'    page.locator("{target}").fill("{value}")')
                
                elif action == 'assert':
                    if step['type'] == 'url':
                        test_code.append(f'    expect(page).to_have_url("{step["expected"]}")')
                
                # Small delay for visualization
                await asyncio.sleep(0.5)
            
            # Stop tracing and save
            await context.tracing.stop(path=f"{output_file}.zip")
            await browser.close()
            
            # Write generated test
            with open(output_file, 'w') as f:
                f.write('\n'.join(test_code))
            
            return output_file

class PlaywrightExecutor:
    """
    Executor Agent: Runs tests and captures detailed traces
    """
    def __init__(self, test_file):
        self.test_file = test_file
    
    def execute_with_trace(self, trace_path):
        """
        Runs test with full Playwright tracing
        Generates trace.zip that can be viewed in Trace Viewer
        """
        print(f"🧪 Executing test: {self.test_file}")
        
        # Pytest with trace
        cmd = [
            "pytest",
            self.test_file,
            f"--tracing=on",
            f"--output={trace_path}",
            "-v",
            "--headed"  # Show browser
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")
            print(result.stdout)
        
        return result.returncode == 0, trace_path
    
    def open_trace_viewer(self, trace_path):
        """
        Opens Playwright Trace Viewer for debugging
        """
        print(f"🔍 Opening Trace Viewer...")
        subprocess.run(["playwright", "show-trace", trace_path])

class PlaywrightHealer:
    """
    Healer Agent: Analyzes failures and suggests fixes
    """
    def __init__(self, test_file, trace_path):
        self.test_file = test_file
        self.trace_path = trace_path
    
    def analyze_failure(self):
        """
        Reads trace, identifies issue, suggests fix
        Uses LLM to interpret Playwright errors
        """
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Read test file
        with open(self.test_file, 'r') as f:
            test_code = f.read()
        
        # Read pytest output (would come from executor)
        # For now, placeholder
        error = "Timeout waiting for locator('#login-button')"
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
        
        prompt = f"""
You are a Test Healing Agent.

Test Code:
{test_code}

Error:
{error}

Suggest a fix. Output JSON:
{{
  "issue": "Locator '#login-button' not found",
  "root_cause": "Selector is fragile, element may have different ID",
  "suggested_fix": "Use get_by_role('button', name='Login') instead",
  "alternative_selectors": [
    "get_by_text('Login')",
    "[data-test='login']",
    "button:has-text('Login')"
  ]
}}
"""
        
        resp = llm.invoke(prompt)
        fix = json.loads(resp.content.replace("```json", "").replace("```", "").strip())
        return fix

# Main Orchestrator using Playwright Agents
async def run_playwright_pipeline(project, url, goal, domain):
    """
    Orchestrates Planner → Builder → Executor → Healer
    """
    print("=" * 70)
    print("🎭 Playwright Native Agent Pipeline")
    print("=" * 70)
    
    output_dir = f"projects/{project}"
    os.makedirs(f"{output_dir}/tests", exist_ok=True)
    os.makedirs(f"{output_dir}/traces", exist_ok=True)
    
    # Step 1: Plan
    print("\n[Step 1/4] 📋 Planning...")
    planner = PlaywrightPlanner(url, goal, domain)
    plan = planner.create_test_plan()
    
    # Save plan
    with open(f"{output_dir}/test_plan.json", 'w') as f:
        json.dump(plan, f, indent=2)
    print(f"✅ Plan saved: {output_dir}/test_plan.json")
    
    # Step 2: Build (choose method)
    print("\n[Step 2/4] 🏗️ Building Test...")
    builder = PlaywrightBuilder(url, plan)
    
    test_file = f"{output_dir}/tests/test_generated.py"
    
    # Option A: Manual Codegen (user records)
    # builder.generate_with_codegen(test_file)
    
    # Option B: Programmatic (automated)
    await builder.generate_programmatic(test_file)
    
    print(f"✅ Test generated: {test_file}")
    
    # Step 3: Execute
    print("\n[Step 3/4] 🧪 Executing Test...")
    executor = PlaywrightExecutor(test_file)
    
    trace_path = f"{output_dir}/traces/execution.zip"
    success, trace = executor.execute_with_trace(trace_path)
    
    # Step 4: Heal (if failed)
    if not success:
        print("\n[Step 4/4] 🔧 Healing...")
        healer = PlaywrightHealer(test_file, trace_path)
        fix = healer.analyze_failure()
        
        print(f"\n📊 Diagnosis:")
        print(f"   Issue: {fix['issue']}")
        print(f"   Cause: {fix['root_cause']}")
        print(f"   Fix: {fix['suggested_fix']}")
        print(f"\n🔄 Alternative Selectors:")
        for alt in fix['alternative_selectors']:
            print(f"   - {alt}")
        
        # Optionally: Auto-apply fix and retry
    
    # Open trace viewer
    print(f"\n🔍 View detailed trace:")
    print(f"   playwright show-trace {trace_path}")
    
    return success

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python playwright_agents.py <project> <url> <goal> [domain]")
        sys.exit(1)
    
    project = sys.argv[1]
    url = sys.argv[2]
    goal = sys.argv[3]
    domain = sys.argv[4] if len(sys.argv) > 4 else "auto"
    
    asyncio.run(run_playwright_pipeline(project, url, goal, domain))
