# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The goal is to ensure the website functions correctly and provides a seamless user experience.

## Scope

The testing will cover core functionalities such as:

*   Handling popups
*   Searching for products
*   Navigating to the Product Detail Page (PDP)
*   Adding products to the cart
*   Initiating the checkout process

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the stability and core functionality of the Dyson India website. The following 8-point checklist is applied:

1.  **Critical Path Focus:** Tests cover essential user flows like product search and checkout initiation.
2.  **Positive Testing:** Scenarios primarily focus on successful outcomes (e.g., product added to cart successfully).
3.  **Minimal Data Variation:** Limited data sets are used, focusing on typical user inputs.
4.  **Independent Tests:** Tests are designed to be independent and can be run in any order.
5.  **Fast Execution:** Tests are optimized for speed to provide quick feedback.
6.  **High Priority:** Any failures in the smoke suite will block the release.
7.  **Automated Execution:** The smoke suite is fully automated and integrated into the CI/CD pipeline.
8.  **Environment Stability:** Smoke tests are run in a stable environment.

### Regression Suite

The Regression Suite aims to ensure that new changes haven't introduced any regressions in existing functionality. This suite will include more comprehensive test cases, covering edge cases, negative scenarios, and alternative flows.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. The following feature files will be created:

*   `smoke.feature`: Contains smoke test scenarios.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS/Linux
*   Test Framework: Playwright

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Test results will be reported in a clear and concise manner.
