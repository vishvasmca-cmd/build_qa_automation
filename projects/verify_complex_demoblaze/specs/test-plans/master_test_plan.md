# Test Plan: Demoblaze Purchase Flow

## Introduction

This document outlines the test plan for verifying the purchase flow on the Demoblaze e-commerce website. The plan includes smoke and regression test suites to ensure the application's functionality and stability.

## Scope

This test plan covers the following functionality:

*   Product browsing and selection
*   Adding products to the cart
*   Checkout process
*   Order placement

## Test Suites

### Smoke Suite

The smoke suite verifies the core functionality of the application. It focuses on the happy path scenarios to ensure that the system is working as expected.

#### Smoke Suite Strategy

The following 8-point checklist was applied when designing the Smoke Suite for this project:

1.  **Critical Paths:** The smoke tests cover the most critical path of purchasing a product.
2.  **Core Business Logic:** The tests validate the core business logic of adding items to the cart and initiating the checkout process.
3.  **Positive Testing:** The smoke tests focus on positive scenarios, such as successfully adding an item to the cart and proceeding to checkout.
4.  **No Negative Testing:** Negative testing (e.g., invalid credit card) is excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios and edge cases are reserved for the regression suite.
6.  **Fast Execution:** The smoke tests are designed to execute quickly to provide rapid feedback on the application's health.
7.  **Independent Tests:** Each smoke test is independent and can be run in any order.
8.  **Minimal Data:** The smoke tests use a minimal set of data to reduce complexity and execution time.

### Regression Suite

The regression suite covers a wider range of scenarios, including alternative flows, negative scenarios, and edge cases. It ensures that recent changes have not broken existing functionality.

## Test Cases

Test cases will be written based on the scenarios outlined in the feature files.

## Test Environment

*   Browser: Chrome
*   Operating System: Windows/macOS/Linux
*   Test Framework: Playwright

## Test Data

Test data will be created to cover various scenarios, including valid and invalid data for the checkout process.

## Entry/Exit Criteria

*   Entry Criteria: Test environment is set up and test data is available.
*   Exit Criteria: All test cases in the smoke suite have passed, and a sufficient number of regression tests have been executed with acceptable results.
