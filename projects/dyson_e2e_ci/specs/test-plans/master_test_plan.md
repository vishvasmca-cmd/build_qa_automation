# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover the following areas:

*   Homepage
*   Product Search
*   Product Detail Page (PDP)
*   Shopping Cart
*   Checkout

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the Dyson India website. These tests are designed to be executed quickly and efficiently to ensure that the application is in a stable state.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** The smoke suite includes the most critical user paths, such as searching for a product, adding it to the cart, and proceeding to checkout.
2.  **Core Business Logic:** The tests cover the core business logic related to product search and the checkout process.
3.  **Positive Testing:** The smoke tests primarily focus on positive scenarios, ensuring that the happy path flows work as expected.
4.  **No Negative Testing:** Negative testing is excluded from the smoke suite to maintain its focus on core functionality.
5.  **No Complex Edge Cases:** Complex edge cases are not included in the smoke suite.
6.  **Speed of Execution:** The smoke tests are designed to be executed quickly to provide rapid feedback on the application's stability.
7.  **Minimal Data Requirements:** The smoke tests use a minimal set of data to reduce setup and execution time.
8.  **Independence:** Smoke tests are designed to be independent of each other to minimize dependencies and improve reliability.

### Regression Suite

The regression suite will provide comprehensive test coverage to ensure that new changes do not introduce regressions into existing functionality. This suite will include a wider range of scenarios, including alternative flows, negative tests, and boundary conditions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each test case will include a clear description of the scenario, preconditions, steps, and expected results.

## Test Environment

The tests will be executed in a dedicated test environment that closely mirrors the production environment. This will help to ensure that the test results are accurate and reliable.

## Test Execution

The tests will be executed automatically as part of the continuous integration (CI) pipeline. This will provide rapid feedback on the quality of the application and help to identify and resolve issues early in the development cycle.
