# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing scope covers essential functionalities such as product search, product detail page (PDP) verification, adding items to the cart, and navigating to the checkout page.

## Test Suites

### 1. Smoke Suite

The smoke suite comprises a minimal set of tests to verify the core functionality of the application. These tests are executed to ensure the build's basic stability before more extensive testing.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Focuses on core user journeys like searching for a product and initiating the checkout process.
2.  **Core Business Logic:** Covers essential e-commerce functions such as adding items to the cart.
3.  **Positive Testing:** Primarily focuses on successful scenarios (e.g., valid search, successful add to cart).
4.  **No Negative Testing:** Excludes negative scenarios (e.g., invalid search terms) unless critical for security.
5.  **No Complex Edge Cases:** Avoids complex scenarios or boundary conditions.
6.  **Fast Execution:** Designed for quick execution to provide rapid feedback on build stability.
7.  **Independent Tests:** Each test is independent and can be run in any order.
8.  **Limited Data Dependency:** Minimizes reliance on specific test data.

### 2. Regression Suite

The regression suite includes a comprehensive set of tests to ensure that new changes haven't introduced regressions in existing functionality. This suite covers alternative flows, negative scenarios, boundary conditions, and cross-module interactions.

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS
*   **Test Data:** Using a set of predefined test data for products and user accounts.

## Test Deliverables

*   Test Plan Document
*   Gherkin Feature Files
*   Test Execution Reports

