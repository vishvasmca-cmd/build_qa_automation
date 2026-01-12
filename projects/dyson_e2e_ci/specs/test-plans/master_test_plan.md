# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as:

*   Handling popups
*   Searching for products
*   Adding products to the cart
*   Navigating to the checkout page

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. It will include tests that cover the happy path scenarios for critical user flows.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like product search and checkout initiation.
2.  **Core Business Logic:** Focuses on the primary function of an e-commerce site - finding and adding products to the cart.
3.  **Positive Testing:** Only successful scenarios are included (e.g., valid search terms, adding to cart when in stock).
4.  **No Negative Testing:** Scenarios like invalid search queries or out-of-stock items are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Advanced features or unusual user behavior are not covered in the smoke tests.
6.  **Fast Execution:** Tests are designed to be quick and efficient, providing rapid feedback on build stability.
7.  **Independent Tests:** Each test is self-contained and does not rely on the state of other tests.
8.  **Limited Data Dependency:** Tests use minimal and readily available test data.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   Test Framework: Playwright

## Test Data

Test data will be used to simulate various user scenarios and ensure the application handles different types of input correctly. This will include:

*   Valid search queries (e.g., Dyson V15 Detect)
*   Valid product selections

## Test Deliverables

*   Test Plan Document
*   Test Automation Scripts (Playwright)
*   Test Execution Reports
*   Defect Reports
