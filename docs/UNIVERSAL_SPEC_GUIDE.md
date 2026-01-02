# 🌐 Universal Test Spec Generator

## One Command, Any Website

```bash
python core/universal_spec_generator.py <ANY_URL>
```

## How It Works

### 1️⃣ **Automatic Domain Detection**
Uses browser automation + AI to analyze:
- Page title
- Navigation structure  
- Content patterns
- Common UI elements

**Detects**:
- ✅ E-commerce (Amazon, Shopify, SauceDemo)
- ✅ Banking (ParaBank, Chase, PayPal)
- ✅ SaaS (Salesforce, HubSpot, Slack)
- ✅ Social Media (Facebook, Twitter clones)
- ✅ Healthcare (Patient portals, Telehealth)
- ✅ Education (LMS, Course platforms)
- ✅ Government (DMV, Tax portals)
- ✅ News & Media
- ✅ Entertainment (Streaming, Gaming)

### 2️⃣ **Domain-Specific Test Generation**
Based on detected domain, generates:

**E-commerce** → Product search, cart, checkout tests  
**Banking** → Account management, transfers, compliance tests  
**SaaS** → Onboarding, dashboards, CRUD operations  
**Social Media** → Profiles, posts, messaging tests  
**Healthcare** → Patient records, appointments, HIPAA compliance  

### 3️⃣ **Auto-Generated Artifacts**

```
specs/
├── {project}_spec.json          # Master specification
└── features/
    ├── user_login.feature        # Gherkin scenarios
    ├── product_search.feature
    └── checkout_flow.feature

tests/
└── pages/
    ├── login_page.py             # Page Object Model
    ├── product_page.py
    └── checkout_page.py
```

## Quick Examples

### E-commerce Site
```bash
python core/universal_spec_generator.py https://www.saucedemo.com
```

**Output**:
- ✅ Domain: E-commerce → Online Retail
- ✅ Features: Product Catalog, Shopping Cart, Checkout
- ✅ Test Suites: Smoke, Regression, Performance
- ✅ Page Objects: LoginPage, InventoryPage, CartPage

### Banking Site
```bash
python core/universal_spec_generator.py https://parabank.parasoft.com/parabank/
```

**Output**:
- ✅ Domain: Banking → Personal Banking
- ✅ Features: Registration, Fund Transfer, Bill Pay
- ✅ Compliance: FDIC, PCI-DSS checks included
- ✅ Security Tests: SQL injection, XSS prevention

### SaaS Application
```bash
python core/universal_spec_generator.py https://thinking-tester-contact-list.herokuapp.com/
```

**Output**:
- ✅ Domain: SaaS → Contact Management
- ✅ Features: User Registration, CRUD Operations
- ✅ API Tests: REST endpoint validation
- ✅ Performance: Response time < 2s assertions

## Generated Spec Structure

```json
{
  "domain": "E-commerce",
  "project_name": "Swag Labs Test Suite",
  "features": [
    {
      "feature_name": "Product Search",
      "priority": "P0",
      "user_stories": [
        "As a customer, I want to search products..."
      ],
      "scenarios": [
        {
          "scenario": "Search by product name",
          "given": "I am on the inventory page",
          "when": "I search for 'backpack'",
          "then": "Products matching 'backpack' are displayed",
          "test_data": {"search_term": "backpack"},
          "assertions": ["At least 1 product found"],
          "page_objects_needed": ["InventoryPage"]
        }
      ],
      "edge_cases": ["Empty search", "Special characters"],
      "performance_metrics": ["Search completes < 1s"]
    }
  ],
  "page_objects": [
    {
      "page_name": "InventoryPage",
      "elements": [
        {"name": "search_field", "locator": "input[type='search']"}
      ],
      "actions": ["searchProduct(term)", "addToCart(productId)"]
    }
  ]
}
```

## Workflow

```
1. Run Generator
   ↓
2. AI Analyzes Site (15-30s)
   ↓  
3. Domain Classified
   ↓
4. Domain-Specific Spec Generated
   ↓
5. Feature Files Created (Gherkin)
   ↓
6. Page Objects Generated (Python)
   ↓
7. Ready to Run!
```

## Advantages Over Manual Spec Writing

| Manual | Universal Generator |
|--------|-------------------|
| 2-3 days | 30 seconds |
| Generic scenarios | Domain-optimized |
| Miss edge cases | AI suggests 20+ edge cases |
| No compliance checks | Auto-includes (GDPR, HIPAA, etc.) |
| Static | Updates when site changes |

## Integration with Autonomous Agent

```bash
# Step 1: Generate spec
python core/universal_spec_generator.py https://example.com

# Step 2: Auto-execute tests
python run.py \
  --project example_auto \
  --url https://example.com \
  --goal "Complete user registration" \
  --domain "auto-detected"

# Knowledge Bank is automatically populated!
```

## Advanced: Multi-Site Batch Generation

```python
SITES = [
    "https://www.saucedemo.com",
    "https://parabank.parasoft.com/parabank/",
    "https://thinking-tester-contact-list.herokuapp.com/"
]

for site in SITES:
    os.system(f"python core/universal_spec_generator.py {site}")
```

## Future Enhancements

- [ ] Video tutorial generation
- [ ] Automatic test data seeding
- [ ] CI/CD pipeline templates
- [ ] Cross-browser configuration
- [ ] Load test scenario generation
- [ ] Accessibility (WCAG) test inclusion

---

**🎯 Bottom Line**: One command generates a complete, domain-aware test framework for ANY website!
