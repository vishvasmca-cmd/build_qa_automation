# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated using Playwright and follow a Behavior-Driven Development (BDD) approach.

## Scope

The scope of this test plan includes:

*   Smoke tests to verify core functionality.
*   Regression tests to ensure existing functionality remains intact after changes.

## Test Suites

### Smoke Suite

The smoke suite will cover the most critical user flows to ensure the basic functionality of the Dyson India website is working as expected. These tests are designed to be executed quickly and efficiently to provide rapid feedback on the stability of the application.

**Smoke Suite Strategy**

The following checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Does the test cover a primary user journey (e.g., login, checkout)? YES (Checkout flow)
2.  **Core Business Logic:** Does the test exercise essential business rules or calculations? YES (Add to cart, checkout)
3.  **Positive Flow:** Does the test primarily follow a happy path without negative inputs? YES
4.  **Data Dependency:** Does the test minimize reliance on specific test data? YES (Uses a specific product but could be generalized)
5.  **External Systems:** Does the test avoid or mock external system dependencies? YES (Assumes payment gateway works)
6.  **Execution Time:** Is the test relatively quick to execute? YES
7.  **Setup/Teardown:** Is the test setup and teardown minimal and efficient? YES
8.  **Failure Impact:** Would a failure of this test indicate a major system outage? YES

### Regression Suite

The regression suite will cover a broader range of scenarios, including alternative flows, negative scenarios, and edge cases. These tests will ensure that new changes do not introduce regressions and that the application remains stable and reliable.

## Test Cases

Test cases will be defined using Gherkin syntax in feature files. Each feature file will represent a specific functionality or module of the application.

## Test Environment

*   Browser: Chromium, Firefox, WebKit
*   Operating System: Windows, macOS, Linux
*   Test Framework: Playwright
*   Programming Language: JavaScript/TypeScript

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Test results will be reported and tracked to ensure timely identification and resolution of issues.
