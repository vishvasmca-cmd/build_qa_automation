# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as:

*   Homepage interactions (popup handling, search).
*   Product search and navigation.
*   Add to cart and checkout processes.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. It will be executed after each build to ensure that the critical paths are working as expected. If any of the smoke tests fail, the build will be rejected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like searching for a product and initiating the checkout process.
2.  **Core Business Logic:** Focuses on the primary revenue flow (product discovery and add to cart).
3.  **No Negative Testing:** Only positive scenarios are included in the smoke suite.
4.  **No Complex Edge Cases:** Simple, straightforward scenarios are prioritized.
5.  **Minimal Test Set:** The suite contains only the most vital tests to provide quick feedback.
6.  **Build Validation:** Failure of any smoke test indicates a critical issue and leads to build rejection.
7.  **High Frequency Execution:** Smoke tests are run after every build or deployment.
8.  **Automated Execution:** The smoke suite is fully automated for rapid and reliable execution.

### Regression Suite

The regression suite will provide comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each test case will have a clear description, preconditions, steps, and expected results.
