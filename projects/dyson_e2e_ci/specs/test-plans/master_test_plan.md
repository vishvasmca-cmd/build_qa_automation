# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be executed to ensure the stability and functionality of the website after code changes.

## Test Scope

The test scope includes:

*   **Smoke Tests:**  Verify core functionalities like searching for a product, adding it to the cart, and proceeding to checkout.
*   **Regression Tests:** Cover a broader range of scenarios, including alternative flows, negative testing, and boundary conditions.

## Test Strategy

### Smoke Suite Strategy

The smoke test suite will focus on the most critical path: searching for a specific product (Dyson V15 Detect), adding it to the cart, and navigating to the checkout page. The following checklist is applied:

1.  **Critical Path Coverage:** Covers the core user journey of product search, add-to-cart, and checkout initiation.
2.  **Positive Testing:** Focuses on successful execution of the flow with valid inputs.
3.  **No Negative Testing:**  Excludes invalid inputs or error conditions in this phase.
4.  **Minimal Data Variation:** Uses a single, representative product for testing.
5.  **Environment Stability:**  Assumes a stable test environment.
6.  **Fast Execution:** Designed for quick execution to provide rapid feedback.
7.  **Build Validation:**  Failure indicates a critical issue, potentially blocking the build.
8.  **Automated Execution:**  Automated execution as part of the CI/CD pipeline.

### Regression Suite Strategy

The regression test suite will expand upon the smoke tests to cover a wider range of scenarios and edge cases. This includes:

*   Alternative search methods (e.g., using different keywords).
*   Testing different product types.
*   Validating error messages.
*   Checking boundary conditions (e.g., maximum quantity in cart).

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:**  Windows 10/11, macOS
*   **Test Framework:** Playwright

## Test Deliverables

*   Test scripts (Playwright).
*   Test execution reports.
*   Defect reports.

## Test Schedule

*   Smoke tests will be executed with every build.
*   Regression tests will be executed on a nightly basis or as needed.
