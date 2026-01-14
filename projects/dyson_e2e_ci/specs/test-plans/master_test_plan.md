# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will cover core functionalities such as product search, adding to cart, and proceeding to checkout.

## Scope

The scope of this test plan includes:

*   Smoke testing of essential functionalities.
*   Regression testing to ensure existing functionalities are not broken by new changes.

## Test Suites

This test plan defines two main test suites:

1.  Smoke Suite
2.  Regression Suite

### Smoke Suite Strategy

The Smoke Suite is designed to verify the most critical functionalities of the Dyson India website. The following checklist is applied to define the scope of the Smoke Suite:

1.  **Critical Paths:** Covers essential user flows like product search, adding to cart, and checkout.
2.  **Core Business Logic:** Focuses on primary revenue-generating flows.
3.  **No Negative Testing:** Excludes negative scenarios unless they involve critical security aspects.
4.  **No Complex Edge Cases:** Avoids complex or less common scenarios.
5.  **Positive Flows:** Primarily focuses on successful, positive flows.
6.  **Minimal Data Variation:** Uses a limited set of test data.
7.  **Fast Execution:** Designed to execute quickly to provide rapid feedback.
8.  **Build Validation:** Used to validate new builds and deployments.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes have not introduced regressions in existing functionalities. This suite covers a wide range of scenarios, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each feature file will contain scenarios that cover specific functionalities.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Test results will be reported in a clear and concise manner.
