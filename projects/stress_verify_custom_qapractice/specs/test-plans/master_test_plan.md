# Test Plan: JavaScript Alerts Interaction

## 1. Introduction

This test plan outlines the testing strategy for verifying the functionality of JavaScript alerts on the testpages.herokuapp.com website. The focus is on ensuring that alerts, confirm boxes, and prompt boxes are displayed correctly and that user interactions with these elements are handled as expected.

## 2. Scope

The scope of this test plan includes:

*   Verifying the display of JavaScript alerts.
*   Verifying the display of JavaScript confirm boxes.
*   Verifying the display of JavaScript prompt boxes.
*   Validating user interaction with alerts (e.g., clicking 'OK').
*   Validating user interaction with confirm boxes (e.g., clicking 'OK' or 'Cancel').
*   Validating user interaction with prompt boxes (e.g., entering text and clicking 'OK' or 'Cancel').

## 3. Test Strategy

We will employ both smoke and regression testing strategies to ensure comprehensive coverage.

### Smoke Suite Strategy

The smoke suite will focus on the core functionality of displaying and interacting with JavaScript alerts. The following 8-point checklist has been applied to define the smoke suite:

1.  **Critical Paths:** Tests cover the main flow of displaying and interacting with alerts, confirm boxes, and prompt boxes.
2.  **Core Business Logic:**  Ensures the basic functionality of displaying and interacting with JavaScript alerts is working.
3.  **Positive Testing:** Focuses on successful scenarios (e.g., alert displays, confirm box accepts).
4.  **No Negative Testing:**  Negative scenarios (e.g., invalid input in prompt boxes) are excluded from the smoke suite.
5.  **No Complex Edge Cases:**  Complex scenarios or boundary conditions are not included in the smoke suite.
6.  **Minimal Test Data:** Uses a minimal set of test data to verify the core functionality.
7.  **Fast Execution:**  Smoke tests are designed to execute quickly to provide rapid feedback.
8.  **Build Validation:**  The smoke suite is used to validate new builds before further testing.

### Regression Suite Strategy

The regression suite will cover a broader range of scenarios, including alternative flows, negative scenarios, and boundary conditions. This will ensure that existing functionality remains intact after changes are made.

## 4. Test Environment

The tests will be executed on the following environment:

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   Test Framework: Playwright

## 5. Test Cases

The following test cases will be executed:

*   **Smoke Tests:**
    *   Verify that clicking "Show alert box" displays an alert.
    *   Verify that clicking "Show confirm box" displays a confirm box.

*   **Regression Tests:**
    *   Verify that clicking "Show prompt box" displays a prompt box.
    *   Verify that clicking "OK" on the alert box closes the alert.
    *   Verify that clicking "OK" on the confirm box closes the confirm box and returns 'true'.
    *   Verify that clicking "Cancel" on the confirm box closes the confirm box and returns 'false'.
    *   Verify that entering text in the prompt box and clicking "OK" closes the prompt box and returns the entered text.
    *   Verify that clicking "Cancel" on the prompt box closes the prompt box and returns 'null'.

## 6. Test Deliverables

The following deliverables will be produced:

*   Test Plan
*   Test Cases
*   Test Results
*   Defect Reports

## 7. Entry Criteria

The following criteria must be met before testing can begin:

*   The application must be deployed to the test environment.
*   The test environment must be configured correctly.
*   The test data must be prepared.

## 8. Exit Criteria

The following criteria must be met before testing can be considered complete:

*   All test cases have been executed.
*   All defects have been resolved.
*   The test results have been reviewed and approved.
