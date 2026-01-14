# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated using Playwright and follow a Behavior-Driven Development (BDD) approach.

## Scope

The scope of this test plan includes:

*   Smoke tests to verify core functionality.
*   Regression tests to ensure existing functionality remains intact after changes.

## Test Strategy

The testing strategy is divided into two main suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite will focus on the most critical paths to ensure the basic functionality of the Dyson India website is working as expected. The following checklist is applied to determine the scope of the smoke tests:

1.  **Critical Path Coverage:** Does this test cover a primary user journey (e.g., purchase, login)?
2.  **Core Business Logic:** Does this test exercise essential business rules or calculations?
3.  **Deployment Validation:** Can this test quickly confirm a successful deployment?
4.  **High Failure Risk:** Does this functionality have a history of frequent failures?
5.  **Customer Impact:** Would a failure in this area significantly impact the user experience?
6.  **Data Integrity:** Does this test verify the correct creation, modification, or deletion of data?
7.  **Security Vulnerability:** Does this test address a potential security risk?
8.  **Third-Party Integration:** Does this test validate a critical integration with an external system?

### Regression Suite Strategy

The Regression Suite will provide comprehensive coverage of the Dyson India website, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This suite will ensure that new changes do not introduce regressions into existing functionality.

## Test Suites

### Smoke Suite

*   **Description:** A minimal set of tests to verify the core functionality of the Dyson India website.
*   **Goal:** To quickly identify critical issues and ensure the website is in a usable state.
*   **Scope:**
    *   Handle Popup *   Search for a product *   Add product to cart *   Navigate to checkout page

### Regression Suite

*   **Description:** A comprehensive suite of tests to ensure that recent changes have not broken existing functionality.
*   **Goal:** To provide a high level of confidence in the stability and reliability of the Dyson India website.
*   **Scope:**
    *   All Smoke tests, plus:
    *   Alternative payment methods
    *   Invalid login attempts
    *   Out-of-stock scenarios
    *   Boundary testing of quantities
    *   Validation of error messages

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS
*   **Test Framework:** Playwright
*   **Programming Language:** JavaScript

## Test Data

Test data will be used to simulate various user scenarios and ensure the application handles different types of input correctly. This includes:

*   Valid and invalid login credentials
*   Product search queries
*   Payment information
*   Shipping addresses

## Test Deliverables

*   Test Plan
*   BDD Feature Files
*   Automated Test Scripts
*   Test Execution Reports

