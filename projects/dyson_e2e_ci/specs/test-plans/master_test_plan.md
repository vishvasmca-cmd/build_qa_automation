# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be executed using Playwright and follow a Behavior-Driven Development (BDD) approach with Gherkin syntax.

## Scope

The scope of this test plan includes:

*   Smoke testing of core functionality (search, add to cart, checkout).
*   Regression testing to ensure existing functionality remains intact after changes.

## Test Environment

*   Browser: Chromium, Firefox, and WebKit
*   Operating System: Windows, macOS, and Linux
*   Test Framework: Playwright
*   BDD Framework: Cucumber

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the most critical paths of the application. If any of these tests fail, the build should be rejected.

#### Smoke Suite Strategy

The following 8-point checklist is applied to define the Smoke Suite:

1.  **Critical Paths:** Tests cover essential user journeys like searching for a product, adding it to the cart, and proceeding to checkout.
2.  **Core Business Logic:** Focuses on testing the primary revenue-generating flow (product purchase).
3.  **No Negative Testing:** Only positive scenarios are considered (e.g., successful search, valid product addition).
4.  **No Complex Edge Cases:** Avoids testing unusual or rare scenarios.
5.  **Fast Execution:** Tests are designed to run quickly to provide rapid feedback.
6.  **Minimal Dependencies:** Reduces reliance on external systems or data.
7.  **High Stability:** Tests are reliable and unlikely to fail due to environmental factors.
8. **Limited Scope:** Only the bare minimum functionality required for a functional build is tested.

### Regression Suite

The regression suite will provide comprehensive coverage of the application's functionality, including alternative flows, negative scenarios, and edge cases.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each feature file will represent a specific feature or functionality of the application.

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Test results will be reported and analyzed to identify any defects or regressions.

## Test Reporting

Test results will be reported in a clear and concise manner, including the number of tests executed, the number of tests passed, and the number of tests failed. Detailed logs and screenshots will be provided for failed tests to aid in debugging.
