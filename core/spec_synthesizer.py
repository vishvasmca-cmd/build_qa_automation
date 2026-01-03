
import os
import json
import yaml
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

SYSTEM_PROMPT_PLANNER = """You are a QA Architect Expert.
Your goal is to analyze a recorded user journey (trace) and the detected domain, then generate a comprehensive Test Plan and BDD Feature Files.

**CRITICAL TASK: SMOKE SUITE DESIGN**
You must design a strict "Smoke Test Suite" based on these principles (purely for test generation, ignoring deployment rules):
1. **Application Availability**: Verify load, URL, and critical assets (JS/CSS).
2. **Critical Navigation**: Main menu, Home -> Products/Search/Help.
3. **Core Business Functionality (Happy Path)**: ONE happy path per major feature (e.g. Search -> Result -> Cart). NO edge cases.
4. **Basic Data Flow**: Verify results appear (e.g. Search "shoe" -> see shoes).
5. **Authentication**: Login/Logout (Standard User only). NO invalid creds tests.
6. **API Health**: Critical endpoints return 200 (Auth, Product, Cart).
7. **Environment**: Version check, Feature flags.

Input:
1. Trace Data: A step-by-step log of actions taken (clicks, inputs, navigation).
2. Domain: The business domain (e.g., Banking, E-commerce).
3. Project Name: The name of the test project.

Output Requirements:
You must generate a structured JSON object containing:
1. "test_plan_content": A professional Markdown Test Plan.
   - Include a specific **"Smoke Suite Strategy"** section listing the 8-point checklist applied to this project.
2. "features": A list of Gherkin feature objects.
   - **MANDATORY**: One file named `smoke.feature` containing the high-level smoke scenarios derived from the trace & domain.
   - "filename": "smoke.feature"
   - "content": Standard Gherkin syntax. Tag scenarios with `@smoke`.

# ... (Gherkin rules continue)
"""

SYSTEM_PROMPT_PRE_PLANNER = """You are a Senior QA Strategist.
Your goal is to create a "Master Test Plan" for a website BEFORE any automation starts.
This plan will guide the autonomous agents on what to mine, what to verify, and how to structure the suite.

**Requirement Checklist**:
1. **Domain Information**: Detailed analysis of the site domain based on URL and goal.
2. **Smoke Suite Definition**: 
   - Basic check that the Website is UP and RUNNING.
   - Core Navigation: Ensure Menu links work.
   - Core Flow: One end-to-end "Happy Path".
3. **Security Audit (NEW)**:
   - Identify critical security headers and SSL requirements for this domain.
   - Suggest which forms or inputs should be prioritized for security probing.
4. **Strategic Mining Instructions**: Tell the agent exactly which elements or pages to prioritize.

Output a professional Markdown report.
"""

class SpecSynthesizer:
    def __init__(self, project_dir, domain="generic"):
        self.project_dir = project_dir
        self.domain = domain
        self.trace_path = os.path.join(project_dir, "outputs", "trace.json")
        self.specs_dir = os.path.join(project_dir, "specs")
        self.features_dir = os.path.join(self.specs_dir, "features")
        self.plans_dir = os.path.join(self.specs_dir, "test-plans")

    def generate_master_plan(self, url, testing_type, goal):
        """Phase 1: Generate Plan BEFORE mining starts."""
        print(f"📋 Creating Strategic Test Plan for {url}...")
        
        security_requirement = ""
        if "security check" in goal.lower():
            security_requirement = """
3. **Security Audit (NEW)**:
   - Identify critical security headers and SSL requirements for this domain.
   - Suggest which forms or inputs should be prioritized for security probing."""

        prompt_instructions = f"""You are a Senior Test Manager (10+ Years Experience).
Your goal is to define a "Master Test Strategy" for a critical business application BEFORE any automation starts.
This document will serve as the blueprint for the entire engineering team (Senior QAs, Test Architects, SDETs).

**YOUR MANDATE**:
Analyze the request and generate a strategic plan covering these four pillars:

### 1. 🔍 RISK ASSESSMENT & PLANNING
- **Analyze the Domain**: Understand the business criticality (e.g., if E-commerce, Checkout is P0).
- **Determine Risk Profile**: Identify what happens if the system fails (financial loss, data breach, trust loss).
- **Define Testing Scope**: Clearly separate "In Scope" vs "Out of Scope".

### 2. 🏗️ TESTING STRATEGY (The "How")
- **Smoke Suite (Sanity)**: Define the absolute minimum "Health Check" (Login + Main Page Load).
- **Regression Suite (Deep Dive)**:
    {'   - Negative Testing: Invalid inputs, boundary values, timeouts.' if 'regression' in testing_type else ''}
    {'   - Edge Cases: Concurrency, network failures, empty states.' if 'regression' in testing_type else ''}
    {'   - Security: OWASP Top 10 basics (SQLi, XSS check inputs).' if 'security' in goal.lower() or 'regression' in testing_type else ''}
- **Data Strategy**: How should we handle test data? (Static? Dynamic generation?)

### 3. 🏛️ ARCHITECTURE GUIDANCE (For the Test Architect)
- **Framework Recommendation**: Recommend a Page Object Model structure.
- **Resilience Strategy**: Define how to handle flakiness (e.g., "Use Polling Assertions", "Implement Self-Healing").

### 4. ⚔️ EXECUTION & MINING INSTRUCTIONS (For the Senior QA)
- **Mining Targets**: List exact pages/flows the autonomous agent must explore FIRST.
- **Verification Criteria**: What defines "Success"? (e.g., "HTTP 200 AND 'Welcome' text visible").

Output a professional, executive-level Markdown report suitable for stakeholders and engineers.
"""
        
        user_msg = f"""
        Target URL: {url}
        Business Domain: {self.domain}
        Testing Type: {testing_type}
        User Goal: {goal}
        """

        try:
            resp = llm.invoke([
                ("system", prompt_instructions),
                ("human", user_msg)
            ])
            
            plan_content = resp.content
            
            # Save to folder
            os.makedirs(self.plans_dir, exist_ok=True)
            plan_path = os.path.join(self.plans_dir, "master_test_plan.md")
            with open(plan_path, "w", encoding="utf-8") as f:
                f.write(plan_content)
                
            print(f"✅ Master Test Plan created: {plan_path}")
            return plan_content
        except Exception as e:
            print(f"❌ Error during Pre-Planning: {e}")
            return None

    def generate_specs(self):
        """Main entry point to generate all specs."""
        if not os.path.exists(self.trace_path):
            print(f"⚠️ Trace file not found at {self.trace_path}. Skipping spec generation.")
            return

        print(f"🧠 Synthesizing Specs & Test Plans based on exploration...")
        
        # Load Data
        with open(self.trace_path, "r") as f:
            trace_data = json.load(f)
            
        # Call LLM
        response = self._synthesize_with_llm(trace_data)
        
        if not response:
            print("❌ Failed to synthesize specs.")
            return

        # Write Output
        self._write_files(response)
        print("✅ Spec Generation Complete!")

    def _synthesize_with_llm(self, trace_data):
        user_msg = f"""
        Project: {os.path.basename(self.project_dir)}
        Domain: {self.domain}
        
        Trace Data:
        {json.dumps(trace_data, indent=2)}
        """
        
        try:
            resp = llm.invoke([
                ("system", SYSTEM_PROMPT_PLANNER),
                ("human", user_msg)
            ])
            
            # Clean and parse JSON
            content = resp.content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            print(f"❌ Error during LLM synthesis: {e}")
            return None

    def _write_files(self, data):
        # 1. Create Directories
        os.makedirs(self.features_dir, exist_ok=True)
        os.makedirs(self.plans_dir, exist_ok=True)
        
        # 2. Write Test Plan
        plan_path = os.path.join(self.plans_dir, "master_test_plan.md")
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write(data.get("test_plan_content", "# Test Plan\nNo content generated."))
        print(f"   📄 Test Plan: {plan_path}")
        
        # 3. Write Features
        for feature in data.get("features", []):
            filename = feature.get("filename", "unknown.feature")
            content = feature.get("content", "")
            
            feat_path = os.path.join(self.features_dir, filename)
            with open(feat_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   🥒 Feature: {feat_path}")
