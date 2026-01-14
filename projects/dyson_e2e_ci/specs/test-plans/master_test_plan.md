# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website (https://www.dyson.in/). The tests will be automated using Playwright and follow a Behavior-Driven Development (BDD) approach with Gherkin syntax.

## Test Scope

The test scope includes critical user journeys such as:

*   Searching for a product
*   Adding a product to the cart
*   Proceeding to checkout

## Test Strategy

The testing strategy is divided into two main suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite will focus on verifying the core functionality of the application. The following checklist is applied to define the smoke tests for this project:

1.  **Critical Paths:** Tests cover essential user flows like product search, add to cart, and checkout initiation.
2.  **Core Business Logic:** Focuses on verifying the basic functionality of adding items to the cart and navigating to the checkout page.
3.  **Positive Testing:** Only positive scenarios are considered (e.g., successful product search, adding to cart).
4.  **No Negative Testing:** Negative scenarios like invalid input or error handling are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios or edge cases are not included in the smoke suite.
6.  **Fast Execution:** Smoke tests are designed to execute quickly to provide rapid feedback on build stability.
7.  **Independent Tests:** Each smoke test should be independent and not rely on the state of other tests.
8.  **Minimal Data Setup:** Data setup is kept to a minimum to reduce test complexity and execution time.

### Regression Suite Strategy

The Regression Suite will provide comprehensive coverage of the application's functionality, including alternative flows, negative scenarios, and edge cases. This suite will be executed to ensure that new changes have not introduced regressions.

## Test Suites

1.  **Smoke Suite:**
    *   Objective: Verify critical path functionality.
    *   Scope: Product search, add to cart, checkout initiation.
    *   Execution Frequency: After each build.

2.  **Regression Suite:**
    *   Objective: Ensure no regressions are introduced by new changes.
    *   Scope: All functionalities, including alternative flows, negative scenarios, and edge cases.
    *   Execution Frequency: Before each release.

## Test Environment

*   Browser: Chromium
*   Operating System: Windows/macOS/Linux (cross-platform)
*   Test Framework: Playwright
*   Programming Language: JavaScript

## Test Deliverables

*   Test scripts (Playwright/JavaScript)
*   Test execution reports
*   Defect reports

## Test Metrics

*   Test pass/fail rate
*   Defect density
*   Test execution time

