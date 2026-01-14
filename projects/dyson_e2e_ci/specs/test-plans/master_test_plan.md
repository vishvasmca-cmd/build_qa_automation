# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will cover core functionalities such as product search, adding to cart, and proceeding to checkout.

## Test Scope

The testing will cover the following areas:

*   Homepage
*   Product Listing Page (PLP)
*   Product Detail Page (PDP)
*   Cart
*   Checkout

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to verify the core functionality of the Dyson India website. It focuses on the happy path scenarios and critical business flows. The following checklist is applied to this project's Smoke Suite:

1.  **Critical Path Coverage:** Tests cover essential user journeys like product search and checkout.
2.  **Core Functionality:** Focuses on testing the primary functions of the application.
3.  **Positive Testing:** Primarily includes positive test cases, ensuring the system works as expected under normal conditions.
4.  **Minimal Complexity:** Scenarios are kept simple and straightforward.
5.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
6.  **Build Validation:** Failure of any smoke test indicates a critical issue, potentially rejecting the build.
7.  **Limited Data Variation:** Uses a small, representative set of test data.
8.  **No Edge Cases:** Excludes complex edge cases or error handling scenarios.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes have not introduced any regressions in existing functionality. This suite covers a wider range of scenarios, including alternative flows, negative test cases, and boundary conditions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each feature file will contain scenarios that cover a specific area of the application.

## Test Environment

*   Browser: Chromium
*   Operating System: Windows/macOS/Linux (cross-platform)
*   Test Framework: Playwright

## Test Data

Test data will be used to simulate different user inputs and scenarios. This data will include:

*   Valid and invalid search queries
*   Product names and SKUs
*   Shipping addresses
*   Payment information

## Test Deliverables

Tests will be executed automatically as part of the CI/CD pipeline. The test results will be reported in a clear and concise manner.

## Metrics

The following metrics will be used to track the progress and effectiveness of the testing efforts:

*   Number of tests executed
*   Number of tests passed
*   Number of tests failed
*   Test execution time
*   Defect density

