# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user workflows on the Dyson India website. The primary goal is to ensure the core functionality of the e-commerce platform remains stable and reliable with each new deployment.

## Scope

The testing will cover essential user journeys, including:

*   Handling popups
*   Searching for products
*   Adding products to the cart
*   Navigating to the checkout page

## Test Suites

This test plan defines two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick and efficient way to verify the stability of the core functionalities. The following checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover the most critical user paths (e.g., search, add to cart, checkout).
2.  **Core Business Logic:** Focuses on testing the primary revenue-generating flows.
3.  **Positive Testing:** Primarily focuses on happy path scenarios.
4.  **No Negative Testing:** Excludes negative test cases unless they involve critical security concerns.
5.  **No Complex Edge Cases:** Avoids complex or less common scenarios.
6.  **Minimal Test Set:** Aims for a small, manageable set of tests.
7.  **Fast Execution:** Tests should execute quickly to provide rapid feedback.
8.  **Build Acceptance:** Failure of any smoke test indicates a critical issue and should reject the build.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes haven't introduced defects into existing functionality. This suite will include:

*   Alternative flows
*   Negative scenarios
*   Boundary analysis
*   Cross-module interactions
*   Validation messages

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS
*   **Test Framework:** Playwright

## Test Cases

Test cases will be written in Gherkin syntax and organized into feature files.

## Smoke Suite Test Cases

*   Verify the ability to close the initial subscription popup.
*   Verify the ability to search for a product ('Dyson V15 Detect').
*   Verify the ability to add the searched product to the cart.
*   Verify the ability to navigate to the checkout page from the cart.

## Regression Suite Test Cases (Examples)

*   Verify search functionality with different search terms.
*   Verify error handling when adding out-of-stock items to the cart.
*   Verify the cart updates correctly when changing quantities.
*   Verify the display of appropriate validation messages during checkout (e.g., missing address).

## Test Data

Test data will be created and managed to support both smoke and regression testing. This includes:

*   Valid and invalid search terms
*   Product inventory data
*   Valid and invalid user credentials
*   Payment information

## Metrics

*   Number of tests executed
*   Number of tests passed
*   Number of tests failed
*   Test execution time
*   Defect density

## Tools

*   Playwright: For test automation
*   GitHub: For version control
*   CI/CD pipeline: For automated test execution
