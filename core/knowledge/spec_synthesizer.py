
import os
import json
import yaml
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Import robust LLM wrapper
# Import robust LLM wrapper
from core.lib.llm_utils import SafeLLM, try_parse_json

# Import Metrics Logger
# Import Metrics Logger
from core.lib.metrics_logger import logger

load_dotenv()

# Initialize LLM with Exponential Backoff
llm = SafeLLM(model="gemini-2.0-flash", temperature=0.2)

try:
    from .strategy_loader import FrameworkStrategyLoader
    from .rag_retriever import RAGRetriever
except (ImportError, ValueError):
    from strategy_loader import FrameworkStrategyLoader
    from rag_retriever import RAGRetriever

SYSTEM_PROMPT_PLANNER = """You are a QA Architect Expert.
Your goal is to analyze a recorded user journey (trace) and the detected domain, then generate a comprehensive Test Plan and BDD Feature Files.

**STRATEGIC GUIDANCE (Review Carefully)**:
{strategy_context}

**CRITICAL TASK: TEST SUITE DESIGN**
Based on the defined strategies above, design the test suite:
1. **Smoke Suite**: Follow the 'Smoke' definition provided in the strategy.
2. **Regression Suite**: Follow the 'Regression' definition provided in the strategy.


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
        self.strategy_loader = FrameworkStrategyLoader()
        self.rag_retriever = RAGRetriever()

    def generate_master_plan(self, url, testing_type, goal):
        """Phase 1: Generate Plan BEFORE mining starts."""
        start_time = __import__('time').time()
        print(f"📋 Creating Strategic Test Plan for {url}...")
        
        # Ensure parameters are strings to avoid NoneType errors
        url = str(url or "")
        goal = str(goal or "")
        testing_type = str(testing_type or "smoke")
        
        security_requirement = ""
        if goal and "security check" in goal.lower():
            security_requirement = """
3. **Security Audit (NEW)**:
   - Identify critical security headers and SSL requirements for this domain.
   - Suggest which forms or inputs should be prioritized for security probing."""

        # 1. Detect Domain
        if self.domain == 'generic':
            self.domain = self.strategy_loader.detect_domain(url)
            print(f"🌍 Detected Domain: {self.domain.upper()}")

        # 2. Load Strategy Context
        strategy_context = self.strategy_loader.load_strategy(self.domain)

        # 3. Retrieve RAG Knowledge
        rag_nodes = self.rag_retriever.retrieve(url=url, domain=self.domain)
        rag_knowledge = self.rag_retriever.format_for_prompt(rag_nodes)

        prompt_instructions = f"""You are a Senior Test Manager (10+ Years Experience).
Your goal is to define a "Master Test Strategy" for a critical business application BEFORE any automation starts.
This document will serve as the blueprint for the entire engineering team (Senior QAs, Test Architects, SDETs).

**STRATEGIC KNOWLEDGE BANK**:
{strategy_context}

**HISTORIC LEARNED PATTERNS (RAG)**:
{rag_knowledge}

**YOUR MANDATE**:
Analyze the request and generate a strategic plan covering these four pillars:

### 1. 🔍 RISK ASSESSMENT & PLANNING
- **Analyze the Domain**: Understand the business criticality (e.g., if E-commerce, Checkout is P0).
- **Determine Risk Profile**: Identify what happens if the system fails (financial loss, data breach, trust loss).
- **Define Testing Scope**: Clearly separate "In Scope" vs "Out of Scope".

### 2. 🏗️ TESTING STRATEGY (The "How")
- **Smoke Suite (Sanity)**: Define the absolute minimum "Health Check" (Login + Main Page Load).
- **Regression Suite (Deep Dive)**:
    {f'   - Negative Testing: Invalid inputs, boundary values, timeouts.' if testing_type and 'regression' in testing_type.lower() else ''}
    {f'   - Edge Cases: Concurrency, network failures, empty states.' if testing_type and 'regression' in testing_type.lower() else ''}
    {f'   - Security: OWASP Top 10 basics (SQLi, XSS check inputs).' if (goal and 'security' in goal.lower()) or (testing_type and 'regression' in testing_type.lower()) else ''}
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
        except Exception as e:
            logger.log_failure("SpecSynthesizer", e, {"action": "master_plan"})
            print(f"❌ Error during Pre-Planning: {e}")
            return None
        
        duration = __import__('time').time() - start_time
        logger.log_event("SpecSynthesizer", "generate_master_plan", duration, cost=0.002)
        return plan_content

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
            # Inject Strategy Context into Planner Prompt
            # Retrieve RAG Knowledge
            url = ""
            if isinstance(trace_data, dict) and "trace" in trace_data:
                trace_list = trace_data["trace"]
                if trace_list and len(trace_list) > 0:
                    url = trace_list[0].get("url", "")
            elif isinstance(trace_data, list) and len(trace_data) > 0:
                url = trace_data[0].get("url", "")
            
            rag_nodes = self.rag_retriever.retrieve(url=url, domain=self.domain)
            rag_knowledge = self.rag_retriever.format_for_prompt(rag_nodes)
            
            strategy_context = self.strategy_loader.load_strategy(self.domain)
            system_prompt = SYSTEM_PROMPT_PLANNER.replace("{strategy_context}", strategy_context)
            system_prompt += f"\n\n{rag_knowledge}"

            resp = llm.invoke([
                ("system", system_prompt),
                ("human", user_msg)
            ])
            
            # Clean and parse JSON
            return try_parse_json(resp.content)
        except Exception as e:
            import traceback
            traceback.print_exc()
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
