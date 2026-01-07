# Test Plan: core_automation_exercise

## Introduction
This document outlines the test plan for the core_automation_exercise project, focusing on the e-commerce domain. The plan details the scope, strategy, and specific test cases to ensure the quality and functionality of the application.

## Test Scope
The testing will cover the following modules:
- Product Catalog
- Shopping Cart

## Test Strategy
The testing will be conducted using a combination of smoke and regression testing. Smoke tests will verify the critical functionalities, while regression tests will ensure that new changes do not introduce defects into existing features.

### Smoke Suite Strategy
The smoke suite will adhere to the following 8-point checklist:
1.  **Critical Paths Only:** Focus on the most essential workflows (e.g., product search, add to cart).
2.  **Positive Testing:** Primarily use valid inputs and expected outcomes.
3.  **Prioritized Scenarios:** Select tests based on business impact.
4.  **Limited Data Set:** Use a small, representative set of data.
5.  **No Edge Cases:** Avoid complex or unusual scenarios.
6.  **Fast Execution:** Ensure tests run quickly to provide rapid feedback.
7.  **Automated Execution:** Automate smoke tests for continuous integration.
8.  **Build Acceptance:** Passing smoke tests is a prerequisite for build acceptance.

## Test Suites

### Smoke Suite
The smoke suite will include the following test cases:
- Navigate to Products page
- Search for a product ('Dress')
- Add the product to the cart

### Regression Suite
The regression suite will include the following test cases:
- (Not defined in this trace, but would be included based on the 'Regression' definition)

## Test Environment
- Browser: Chrome (latest version)
- Operating System: Windows 10

## Test Deliverables
- Test Plan Document
- Automated Test Scripts (Selenium with Playwright)
- Test Execution Reports