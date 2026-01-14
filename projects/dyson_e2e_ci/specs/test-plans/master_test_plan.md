# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The scope of this test plan covers the core functionality of the Dyson India website, including:

*   Homepage interactions (popup handling)
*   Product search and navigation
*   Product Detail Page (PDP) verification
*   Add to Cart functionality
*   Checkout process

## Test Suites

### Smoke Suite

The smoke suite is a minimal set of tests designed to verify the most critical functions of the system. These tests are executed frequently to ensure that the core functionality is working as expected. If any of these tests fail, the build is considered unstable and should be rejected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user flows like product search, adding to cart, and initiating checkout.
2.  **Core Business Logic:** Focuses on verifying the core e-commerce functionality (search, product display, cart operations).
3.  **Positive Testing:** Primarily focuses on happy path scenarios (e.g., successful search, adding product to cart).
4.  **No Negative Testing:** Excludes negative scenarios (e.g., invalid search terms) in the smoke suite.
5.  **No Complex Edge Cases:** Avoids complex scenarios or boundary conditions.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Independent Tests:** Tests are independent of each other to minimize dependencies and ensure reliable results.
8.  **Stable Locators:** Uses stable locators to avoid test failures due to UI changes.

### Regression Suite

The regression suite is a comprehensive set of tests designed to ensure that new changes have not introduced any regressions in existing functionality. This suite covers a wider range of scenarios, including alternative flows, negative scenarios, and boundary conditions.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright
*   Test Data: Use a combination of static and dynamic test data.

## Test Execution

*   Smoke tests will be executed on every build.
*   Regression tests will be executed on a nightly basis or before major releases.

## Test Reporting

*   Test results will be reported using Playwright's built-in reporting capabilities.
*   Failed tests will be investigated and fixed promptly.
