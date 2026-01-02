# 🧠 Automated Spec & Feature Generation

## ✨ **Overview**

The framework now automatically converts exploration sessions into professional documentation.
After the AI explores the website (Step 1), it uses **Gemini 2.0 Flash** to synthesize:

1.  **Master Test Plan** (`specs/test-plans/master_test_plan.md`)
2.  **Gherkin Feature Files** (`specs/features/*.feature`)

---

## 🚀 **How It Works**

1.  **Exploration**: AI navigates the site, clicking and filling forms.
    *   *Output*: `outputs/trace.json`
2.  **Synthesis**: `SpecSynthesizer` reads the trace and detected domain.
3.  **Generation**:
    *   Uses LLM to understand logical features (e.g., "Registration", "Login").
    *   Writes industry-standard Gherkin scenarios.
    *   Creates a test strategy document.

---

## 📄 **Output Examples**

### **Feature File** (`specs/features/registration.feature`)
```gherkin
Feature: User Registration
  As a new user
  I want to create an account
  So that I can access banking services

  Scenario: Successful Registration
    Given I am on the home page
    When I click "Register"
    And I enter "John" into "First Name"
    And I enter "Doe" into "Last Name"
    And I submit the form
    Then I should see "Your account was created successfully"
    And I should be logged in
```

### **Test Plan** (`specs/test-plans/master_test_plan.md`)
*   **Scope**: User Registration and Login flow.
*   **Risk Analysis**: High risk of failure on dynamic locators (mitigated by AI healing).
*   **Strategy**: Autonomous regression testing via Playwright.

---

## 🛠️ **Configuration**

The synthesis happens automatically during `python run.py`.

**To Trigger Manually:**
```bash
python -c "from core.spec_synthesizer import SpecSynthesizer; SpecSynthesizer('projects/my_project', 'banking').generate_specs()"
```

---

## ✅ **Benefits**

*   **Documentation stays in sync** with actual test execution.
*   **BDD-ready**: Generated feature files can be used for collaboration.
*   **Compliance**: Auto-generated test plans satisfy audit requirements.
