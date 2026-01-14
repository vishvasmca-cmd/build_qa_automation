# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E-commerce website, focusing on end-to-end testing. The goal is to ensure the core functionalities of the website are working as expected.

## Scope

The testing will cover critical user flows, including:

*   Handling popups
*   Searching for products
*   Adding products to the cart
*   Navigating to the checkout page

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the most critical functionalities of the Dyson website. The following checklist has been applied to define the scope of the Smoke Suite:

1.  **Critical Paths:** Focus on the most common and essential user journeys (e.g., product search, add to cart, checkout).
2.  **Core Business Logic:** Verify the primary revenue-generating flows are functional.
3.  **Positive Testing:** Primarily focus on happy path scenarios.
4.  **No Negative Testing:** Exclude negative test cases unless they represent critical security concerns.
5.  **No Complex Edge Cases:** Avoid complex or less common scenarios.
6.  **Minimal Data Variation:** Use a limited set of test data for simplicity.
7.  **Fast Execution:** Ensure the suite can be executed quickly to provide rapid feedback.
8.  **Build Validation:** The Smoke Suite must pass for a build to be considered stable.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes haven't introduced any regressions in existing functionality. This suite will include:

*   Alternative flows
*   Negative scenarios
*   Boundary analysis
*   Cross-module interactions
*   Validation messages

## Test Cases

Test cases will be written in Gherkin syntax and organized into feature files.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS
*   Test Framework: Playwright

## Test Data

Test data will be managed within the test framework and will include:

*   Search queries
*   Product information

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Results will be reported to a central dashboard.

## Metrics

*   Test pass/fail rate
*   Test execution time
*   Defect density
