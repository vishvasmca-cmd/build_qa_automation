"""
Universal Domain-Aware Test Specification Generator

Automatically detects website domain and generates appropriate test specs
Works for ANY website: E-commerce, Banking, SaaS, Social Media, Healthcare, etc.
"""

import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

DOMAIN_DETECTION_PROMPT = """
You are a Domain Classification Expert for web applications.

Analyze the following website information and classify it:

URL: {url}
Page Title: {title}
Main Content: {content_sample}
Navigation Links: {nav_links}

**OUTPUT FORMAT** (JSON):
{{
  "primary_domain": "E-commerce | Banking | SaaS | Social Media | Healthcare | Education | Government | News | Entertainment",
  "sub_domain": "More specific category (e.g., 'Online Retail', 'Personal Banking', 'CRM Software')",
  "confidence": "High | Medium | Low",
  "key_features_detected": ["List of main features visible"],
  "reasoning": "Brief explanation of classification"
}}

Classify this website.
"""

UNIVERSAL_SPEC_PROMPT = """
You are a Senior QA Architect with expertise across all software domains.

Generate a comprehensive test specification for this {domain} application.

**Website Context**:
- Domain: {domain}
- Sub-domain: {sub_domain}  
- Detected Features: {features}

**DOMAIN-SPECIFIC REQUIREMENTS**:

**For E-commerce**:
- Product search & filtering
- Add to cart workflow
- Checkout & payment
- Order tracking
- User reviews

**For Banking**:
- Account management (registration, login)
- Fund transfers
- Bill payments
- Transaction history
- Security (2FA, encryption)
- Compliance (FDIC, PCI-DSS)

**For SaaS**:
- User onboarding
- Feature trials
- Dashboard interactions
- Data CRUD operations
- Subscription management
- API integrations

**For Social Media**:
- User profiles
- Content posting
- Feed interactions (like, share, comment)
- Messaging
- Privacy settings

**For Healthcare**:
- Patient registration
- Appointment booking
- Medical records access
- HIPAA compliance
- Prescription management

**OUTPUT FORMAT** (JSON):
{{
  "domain": "{domain}",
  "project_name": "Descriptive name",
  "features": [
    {{
      "feature_name": "Feature name",
      "priority": "P0 | P1 | P2",
      "user_stories": ["As a user, I want to..."],
      "scenarios": [
        {{
          "scenario": "Scenario description",
          "given": "Given step",
          "when": "When step", 
          "then": "Then step",
          "test_data": {{"key": "value"}},
          "assertions": ["List of assertions"],
          "page_objects_needed": ["LoginPage", "DashboardPage"]
        }}
      ],
      "edge_cases": ["List of edge cases to test"],
      "security_considerations": ["Security aspects"],
      "performance_metrics": ["Response time < 2s", "Page load < 3s"]
    }}
  ],
  "page_objects": [
    {{
      "page_name": "LoginPage",
      "url_pattern": "/login",
      "elements": [
        {{
          "name": "username_field",
          "locator": "input[name='username']",
          "type": "input"
        }}
      ],
      "actions": ["login(username, password)", "clickForgotPassword()"]
    }}
  ],
  "test_suites": [
    {{
      "suite_name": "Smoke Tests",
      "features": ["List of critical features"],
      "execution_time_estimate": "5-10 minutes"
    }}
  ]
}}

Generate specification for this website.
"""

async def detect_domain(url):
    """Automatically detect website domain using browser automation"""
    print(f"\n🔍 Analyzing website: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Extract page information
            title = await page.title()
            content = await page.inner_text("body")
            content_sample = content[:1000]  # First 1000 chars
            
            # Extract navigation links
            nav_links = await page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('nav a, header a, .menu a'));
                    return links.map(a => a.textContent.trim()).slice(0, 20);
                }
            """)
            
            await browser.close()
            
            print(f"   Title: {title}")
            print(f"   Nav Links: {nav_links[:5]}...")
            
        except Exception as e:
            print(f"   ⚠️ Could not load page: {e}")
            await browser.close()
            return None
    
    # Use LLM to classify
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)
    
    prompt = DOMAIN_DETECTION_PROMPT.format(
        url=url,
        title=title,
        content_sample=content_sample,
        nav_links=", ".join(nav_links)
    )
    
    resp = llm.invoke(prompt)
    domain_info = json.loads(resp.content.replace("```json", "").replace("```", "").strip())
    
    print(f"\n✅ Domain Detected:")
    print(f"   Primary: {domain_info['primary_domain']}")
    print(f"   Sub-domain: {domain_info['sub_domain']}")
    print(f"   Confidence: {domain_info['confidence']}")
    print(f"   Reasoning: {domain_info['reasoning']}")
    
    return domain_info

def generate_universal_spec(url, domain_info):
    """Generate test spec based on detected domain"""
    print(f"\n📋 Generating {domain_info['primary_domain']} test specification...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    
    prompt = UNIVERSAL_SPEC_PROMPT.format(
        domain=domain_info['primary_domain'],
        sub_domain=domain_info['sub_domain'],
        features=", ".join(domain_info['key_features_detected'])
    )
    
    resp = llm.invoke(prompt)
    spec_json = resp.content.replace("```json", "").replace("```", "").strip()
    
    try:
        spec = json.loads(spec_json)
        return spec
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parse error: {e}")
        print(f"Raw response: {spec_json[:500]}...")
        return None

def create_page_objects(spec, output_dir="tests/pages"):
    """Generate Page Object Model classes"""
    os.makedirs(output_dir, exist_ok=True)
    
    for page_obj in spec.get("page_objects", []):
        page_name = page_obj["page_name"]
        file_name = re.sub(r'(?<!^)(?=[A-Z])', '_', page_name).lower()
        file_path = os.path.join(output_dir, f"{file_name}.py")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f'''"""
{page_name} - Page Object Model
Auto-generated from domain specification
"""

from playwright.sync_api import Page, expect

class {page_name}:
    def __init__(self, page: Page):
        self.page = page
        self.url_pattern = "{page_obj.get('url_pattern', '/')}"
    
    # Locators
''')
            
            for element in page_obj.get("elements", []):
                elem_name = element["name"].upper()
                f.write(f'    {elem_name} = "{element["locator"]}"\n')
            
            f.write("\n    # Actions\n")
            for action in page_obj.get("actions", []):
                # Parse action signature
                func_name = action.split("(")[0]
                params = action.split("(")[1].replace(")", "")
                
                f.write(f'''    def {func_name}(self{"," if params else ""} {params}):
        """Execute {func_name} action"""
        # TODO: Implement action logic
        pass
    
''')
        
        print(f"✅ Created: {file_path}")

def create_domain_features(spec, output_dir="specs/features"):
    """Create feature files with domain-specific scenarios"""
    os.makedirs(output_dir, exist_ok=True)
    
    for feature in spec["features"]:
        # Sanitize file name
        feature_name = re.sub(r'[^\w\s-]', '', feature["feature_name"])
        feature_name = re.sub(r'[-\s]+', '_', feature_name).lower()
        feature_file = os.path.join(output_dir, f"{feature_name}.feature")
        
        with open(feature_file, "w", encoding="utf-8") as f:
            f.write(f"Feature: {feature['feature_name']}\n")
            f.write(f"  Priority: {feature['priority']}\n\n")
            
            # User stories
            for story in feature.get("user_stories", []):
                f.write(f"  {story}\n")
            f.write("\n")
            
            # Scenarios
            for scenario in feature["scenarios"]:
                f.write(f"  Scenario: {scenario['scenario']}\n")
                f.write(f"    Given {scenario['given']}\n")
                f.write(f"    When {scenario['when']}\n")
                f.write(f"    Then {scenario['then']}\n")
                
                for assertion in scenario.get("assertions", []):
                    f.write(f"    And {assertion}\n")
                f.write("\n")
        
        print(f"✅ Created: {feature_file}")

async def main(url):
    """Main orchestration"""
    print("=" * 70)
    print("🌐 Universal Test Specification Generator")
    print("=" * 70)
    
    # Step 1: Detect domain
    domain_info = await detect_domain(url)
    if not domain_info:
        print("❌ Could not detect domain. Exiting.")
        return
    
    # Step 2: Generate spec
    spec = generate_universal_spec(url, domain_info)
    if not spec:
        print("❌ Could not generate spec. Exiting.")
        return
    
    # Step 3: Save spec
    os.makedirs("specs", exist_ok=True)
    project_name = spec.get("project_name", "website").lower().replace(" ", "_")
    spec_file = f"specs/{project_name}_spec.json"
    
    with open(spec_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    print(f"\n✅ Spec saved: {spec_file}")
    
    # Step 4: Generate artifacts
    print("\n📝 Generating test artifacts...")
    create_domain_features(spec)
    create_page_objects(spec)
    
    print("\n🎉 Test framework generated successfully!")
    print(f"\nNext steps:")
    print(f"1. Review: {spec_file}")
    print(f"2. Customize: tests/pages/*.py")
    print(f"3. Implement: specs/features/*.feature")
    print(f"4. Run: pytest tests/")

if __name__ == "__main__":
    import asyncio
    import sys
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        # Default test URLs
        print("Usage: python universal_spec_generator.py <URL>")
        print("\nExample URLs to try:")
        print("  python universal_spec_generator.py https://parabank.parasoft.com/parabank/")
        print("  python universal_spec_generator.py https://www.saucedemo.com")
        print("  python universal_spec_generator.py https://thinking-tester-contact-list.herokuapp.com/")
        sys.exit(1)
    
    asyncio.run(main(target_url))
