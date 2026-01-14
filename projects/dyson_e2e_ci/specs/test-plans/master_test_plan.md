# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated using Playwright and follow a Behavior-Driven Development (BDD) approach with Gherkin syntax.

## Scope

The scope of this test plan includes:

*   Smoke tests to verify core functionality.
*   Regression tests to ensure existing functionality remains intact after changes.

## Test Suites

### Smoke Suite

The smoke suite will cover the most critical user flows to ensure the basic functionality of the Dyson India website is working as expected. These tests are designed to be executed quickly and efficiently to provide rapid feedback on the stability of the application.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** The smoke tests cover essential paths like searching for a product, adding it to the cart, and proceeding to checkout.
2.  **Core Business Logic:** The tests validate the core e-commerce logic, such as adding products to the cart and navigating to the checkout page.
3.  **No Negative Testing:** The smoke tests focus on happy path scenarios and do not include negative testing.
4.  **No Complex Edge Cases:** The smoke tests avoid complex edge cases and focus on the most common user flows.
5.  **Speed of Execution:** The smoke tests are designed to be executed quickly to provide rapid feedback.
6.  **Independence:** Each smoke test should be independent of other tests.
7.  **Minimal Setup:** The setup required for each smoke test should be minimal.
8.  **Clear Assertions:** The assertions in the smoke tests should be clear and easy to understand.

### Regression Suite

The regression suite will cover a broader range of scenarios, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. These tests are designed to ensure that changes to the application do not introduce regressions or break existing functionality.

## Test Cases

Test cases will be defined in Gherkin syntax and stored in feature files. Each feature file will represent a specific area of functionality, and each scenario will represent a specific test case.

## Test Environment

*   Browser: Chromium, Firefox, and WebKit
*   Operating System: Windows, macOS, and Linux
*   Test Framework: Playwright
*   Programming Language: JavaScript/TypeScript

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Test results will be reported in a clear and concise manner.
