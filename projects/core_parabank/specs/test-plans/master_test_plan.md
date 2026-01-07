# Test Plan: core_parabank

## Domain: Banking

### Scope

This test plan covers the core functionality of the ParaBank application, focusing on account access and basic navigation. The tests are designed to ensure the application's stability and reliability.

### Test Suites

This test plan includes a Smoke Suite and a Regression Suite.

#### Smoke Suite Strategy

The Smoke Suite is designed to verify the most critical functionalities of the ParaBank application. The following checklist is applied:

1.  **Critical Paths:** Focuses on essential user flows like login and basic navigation.
2.  **Core Business Logic:** Verifies primary functionalities.
3.  **Positive Testing:** Primarily uses positive test cases.
4.  **No Negative Testing:** Excludes negative test cases unless critical for security.
5.  **No Complex Edge Cases:** Avoids complex or boundary test cases.
6.  **Fast Execution:** Ensures quick execution to provide rapid feedback.
7.  **Build Validation:** Determines whether a build is stable enough for further testing.
8.  **Limited Scope:** Covers only the most vital functionalities.

#### Regression Suite Strategy

The Regression Suite is designed to ensure that new changes have not introduced defects into existing functionality. It includes a broader range of test cases, including alternative flows, negative scenarios, and boundary conditions.

### Test Modules

#### Account Access (Criticality: Critical)

*   **Smoke Tests:**
    *   Verify successful navigation to the About Us page.
    *   Verify successful navigation to the Home page.
    *   Verify the presence of the Account History link.

*   **Regression Tests:**
    *   (Not covered in the trace, but would include MFA, password recovery, etc.)

#### Statements & History (Criticality: Medium)

*   **Smoke Tests:**
    *   (Not covered in the trace, but would include viewing recent transactions)

*   **Regression Tests:**
    *   (Not covered in the trace, but would include downloading statements, searching transactions, etc.)
