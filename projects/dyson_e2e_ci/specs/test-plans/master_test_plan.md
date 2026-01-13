# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as:

*   Handling popups
*   Searching for products
*   Adding products to the cart
*   Navigating to the checkout page

## Test Suites

### Smoke Suite

The smoke suite will focus on the core functionalities to ensure the basic health of the application. It will cover happy path scenarios only.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like product search and checkout initiation.
2.  **Core Business Logic:** Focuses on testing the primary flow of adding a product to the cart and proceeding to checkout.
3.  **Positive Testing:** Only positive scenarios are considered (e.g., valid search, successful add to cart).
4.  **No Negative Testing:** Negative scenarios like invalid search terms are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios or boundary conditions are not included.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Independent Tests:** Each test is independent and can be run in isolation.
8.  **Minimal Data Setup:** Data setup is kept to a minimum to reduce test complexity.

### Regression Suite

The regression suite will provide a comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   Test Framework: Playwright

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files.
