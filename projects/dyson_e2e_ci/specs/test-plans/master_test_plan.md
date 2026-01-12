# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will ensure the core functionality of the website is working as expected, with a focus on the happy path scenarios for smoke tests and a broader range of scenarios for regression tests.

## Scope

The scope of this test plan includes:

*   **Smoke Tests:** Verify critical path functionality, such as searching for a product, adding it to the cart, and proceeding to checkout.
*   **Regression Tests:** Cover a wider range of scenarios, including alternative flows, negative scenarios, and boundary conditions.

## Test Suites

### Smoke Suite

The smoke suite will focus on the most critical functionalities of the Dyson website. The primary goal is to quickly verify the stability of the application after deployment or code changes.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like product search and checkout.
2.  **Core Business Logic:** Focuses on testing the primary revenue-generating flows.
3.  **Positive Testing:** Primarily includes happy path scenarios.
4.  **No Negative Testing:** Excludes negative scenarios unless critical for security.
5.  **No Complex Edge Cases:** Avoids complex or less common scenarios.
6.  **Fast Execution:** Tests are designed to execute quickly.
7.  **Independent Tests:** Each test should be independent and not rely on the state of others.
8.  **High Priority:** Failures in smoke tests indicate critical issues.

#### Smoke Test Cases

1.  **Search and Add to Cart:**
    *   Verify that a user can search for a product (e.g., Dyson V15 Detect).
    *   Verify that the user can add the product to the cart.
    *   Verify that the cart drawer opens after adding the product.
    *   Verify that the user can navigate to the checkout page.

### Regression Suite

The regression suite will cover a broader range of scenarios to ensure that new changes have not introduced any regressions in existing functionality.

#### Regression Test Cases

1.  **Search Functionality:**
    *   Search with valid and invalid keywords.
    *   Verify search suggestions.
    *   Verify search results page.
2.  **Product Details Page (PDP):**
    *   Verify product information (name, price, description).
    *   Verify product images.
    *   Verify 'Add to Cart' button functionality.
    *   Verify product reviews.
3.  **Cart Functionality:**
    *   Verify adding products to the cart.
    *   Verify updating product quantities in the cart.
    *   Verify removing products from the cart.
    *   Verify cart total calculation.
    *   Verify applying discount codes.
4.  **Checkout Functionality:**
    *   Verify entering shipping information.
    *   Verify selecting a shipping method.
    *   Verify entering billing information.
    *   Verify payment processing.
    *   Verify order confirmation page.
5.  **Account Management:**
    *   Verify user registration.
    *   Verify user login and logout.
    *   Verify updating user profile information.
    *   Verify password reset.

## Test Environment

*   **Browsers:** Chrome, Firefox, Safari
*   **Operating Systems:** Windows, macOS, Linux
*   **Devices:** Desktop, Mobile, Tablet

## Test Data

*   Use a combination of valid and invalid data for testing.
*   Create test accounts with different roles and permissions.
*   Use different payment methods for testing the checkout process.

## Test Execution

*   Execute smoke tests after each build.
*   Execute regression tests on a regular basis (e.g., nightly or weekly).
*   Use a test management tool to track test results and defects.

## Defect Management

*   Report defects in a bug tracking system (e.g., Jira).
*   Provide detailed information about the defect, including steps to reproduce, expected results, and actual results.
*   Assign defects to the appropriate developers for resolution.

## Metrics

*   **Test Coverage:** Percentage of code covered by tests.
*   **Test Pass Rate:** Percentage of tests that pass.
*   **Defect Density:** Number of defects per line of code.
*   **Defect Resolution Time:** Time taken to resolve defects.
