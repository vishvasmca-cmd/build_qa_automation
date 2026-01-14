# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The goal is to ensure the website functions correctly and provides a seamless user experience.

## Scope

The testing will cover core functionalities such as product search, adding to cart, and proceeding to checkout. Both smoke and regression test suites will be implemented.

## Test Suites

1.  **Smoke Suite:** A minimal set of tests to verify the system's most critical functions.
2.  **Regression Suite:** A comprehensive suite of tests ensuring that recent changes haven't broken existing functionality.

### Smoke Suite Strategy

The smoke suite will adhere to the following 8-point checklist:

1.  **Critical Path Coverage:** Tests cover essential user flows (search, add to cart, checkout).
2.  **Core Functionality:** Focus on the primary business logic of the e-commerce platform.
3.  **Positive Testing:** Primarily focuses on successful scenarios.
4.  **No Edge Cases:** Avoid complex or unusual scenarios.
5.  **No Negative Testing:** Exclude tests with invalid inputs or error conditions (unless critical security related).
6.  **Fast Execution:** Tests should be quick to execute to provide rapid feedback.
7.  **Stable Locators:** Use robust locators to minimize test flakiness.
8. **Independent Tests:** Tests should be independent of each other.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS (latest versions)
*   Test Framework: Playwright
*   Test Data: Use a combination of static and dynamically generated test data.

## Test Cases

Test cases will be written in Gherkin syntax and organized into feature files.

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Results will be reported to a central dashboard.

## Metrics

*   Test Pass Rate
*   Test Failure Rate
*   Test Execution Time

