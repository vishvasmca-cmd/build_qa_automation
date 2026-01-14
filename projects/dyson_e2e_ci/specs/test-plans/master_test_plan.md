# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The tests will cover key functionalities such as:

*   Navigating the homepage
*   Searching for products
*   Adding products to the cart
*   Initiating the checkout process

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. These tests are designed to be quick and efficient, providing a high level of confidence in the stability of the system.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover essential user flows like product search and checkout initiation.
2.  **Core Business Logic:** Focuses on testing the primary functions related to product discovery and purchase.
3.  **Positive Testing:** Only happy path scenarios are included in the smoke suite.
4.  **No Negative Testing:** Negative scenarios are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex or less common scenarios are not included.
6.  **Speed and Efficiency:** Tests are designed to be executed quickly.
7.  **Build Validation:** Failure of any smoke test indicates a critical issue and may reject the build.
8.  **Limited Scope:** The suite covers a minimal set of functionalities.

### Regression Suite

The regression suite will provide comprehensive coverage of the application, including alternative flows, negative scenarios, and edge cases. These tests will ensure that new changes have not introduced any regressions.

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10
*   **Test Framework:** Playwright

## Test Data

Test data will be used to simulate various user scenarios and ensure that the application behaves as expected. This data will include:

*   Valid search queries (e.g., Dyson V15 Detect)

## Test Deliverables

*   Test Plan Document
*   Test Automation Scripts (Playwright)
*   Test Execution Reports

