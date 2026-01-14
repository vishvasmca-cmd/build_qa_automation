# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will cover core functionalities such as product search, adding to cart, and proceeding to checkout.

## Scope

The scope of this test plan includes:

*   Smoke testing of critical path: Searching for a product, adding it to the cart, and navigating to the checkout page.
*   Regression testing to ensure existing functionalities are not broken due to recent changes (future).

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS (latest versions)
*   Test Framework: Playwright
*   Test Data: Using valid product names and checkout information.

## Test Suites

### Smoke Suite Strategy

The Smoke Suite is designed to verify the core functionality of the Dyson India website. The following checklist is applied:

1.  **Critical Paths Only:** Focuses on the most essential user flows (search, add to cart, checkout).
2.  **Positive Testing:** Primarily uses valid inputs and scenarios.
3.  **Minimal Data:** Uses a small, representative set of test data.
4.  **Fast Execution:** Designed to run quickly to provide rapid feedback.
5.  **Build Validation:** Failure indicates a critical issue that blocks the build.
6.  **No Edge Cases:** Excludes complex or unusual scenarios.
7.  **Core Business Logic:** Validates the primary revenue-generating flows.
8.  **Limited Scope:** Covers only the most vital functionalities.

### Regression Suite

The Regression Suite will cover a broader range of scenarios, including alternative flows, negative testing, and edge cases (future).

## Test Cases

### Smoke Suite

1.  **Search and Add to Cart:**
    *   Objective: Verify the ability to search for a product, add it to the cart, and proceed to checkout.
    *   Steps:
        1.  Open the Dyson India website.
        2.  Close the 'Subscribe' popup (if present).
        3.  Search for "Dyson V15 Detect".
        4.  Click on the first product result.
        5.  Verify the 'Add to Cart' button is visible.
        6.  Click 'Add to Cart'.
        7.  Verify the cart drawer opens.
        8.  Click 'Checkout'.
        9.  Verify that the checkout page is reached.

### Regression Suite (Future)

*   To be defined in future iterations.

## Test Deliverables

*   Test Plan Document
*   Test Scripts (Playwright)
*   Test Results Report

## Roles and Responsibilities

*   QA Architect: Responsible for creating and maintaining the test plan, designing test suites, and providing guidance on test automation.
*   QA Engineer: Responsible for writing and executing test scripts, analyzing test results, and reporting defects.

## Test Schedule

*   Smoke tests will be executed with each build.
*   Regression tests will be executed on a regular basis (e.g., weekly or after major releases).
