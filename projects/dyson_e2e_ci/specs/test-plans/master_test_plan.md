# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as:

*   Handling popups
*   Product search
*   Product Detail Page (PDP) verification
*   Add to Cart functionality
*   Checkout process

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. It will include tests that cover the happy path scenarios for the most critical user flows.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like product search, adding to cart, and initiating checkout.
2.  **Core Business Logic:** Focuses on verifying the basic functionality of adding items to the cart and proceeding to checkout.
3.  **Positive Testing:** Only positive scenarios are considered (e.g., successful search, adding to cart with sufficient stock).
4.  **No Negative Testing:** Negative scenarios like invalid search queries or insufficient stock are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios like applying discounts or using gift cards are not included.
6.  **Fast Execution:** Tests are designed to be quick and efficient, providing rapid feedback on build stability.
7.  **Independent Tests:** Each test is independent and can be run in isolation without dependencies on other tests.
8.  **Limited Data Variation:** Only a single set of data is used for each test to minimize execution time.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS
*   **Test Framework:** Playwright
*   **Test Runner:** Jest

## Test Data

Test data will be used to simulate various user scenarios and ensure the application functions correctly under different conditions.

## Test Deliverables

*   Test Plan Document
*   Test Cases (Gherkin Feature Files)
*   Test Results
*   Defect Reports

