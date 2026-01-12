# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E-commerce website, focusing on end-to-end testing to ensure critical user flows are functioning correctly. The tests will cover core functionalities such as product search, adding to cart, and proceeding to checkout.

## Scope

The scope of this test plan includes:

*   Smoke Tests: Verify the core functionalities of the website.
*   Regression Tests: Ensure that new changes do not negatively impact existing functionalities.

## Test Suites

1.  **Smoke Suite:**
    *   Objective: To quickly verify the stability and core functionality of the Dyson website.
    *   Description: A minimal set of tests covering the most critical paths.

2.  **Regression Suite:**
    *   Objective: To ensure that new changes or bug fixes haven't introduced new issues or broken existing functionality.
    *   Description: A comprehensive set of tests covering various scenarios, including edge cases and negative tests.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following 8-point checklist:

1.  **Critical Paths:** Focus on essential user journeys like searching for a product, adding it to the cart, and initiating the checkout process.
2.  **Core Business Logic:** Verify the primary revenue-generating flow (product purchase).
3.  **Positive Testing:** Primarily focus on successful scenarios (e.g., valid search, successful add to cart).
4.  **No Negative Testing:** Exclude negative scenarios unless they represent critical security concerns.
5.  **Minimal Edge Cases:** Avoid complex or less common scenarios.
6.  **Fast Execution:** Design tests for quick execution to provide rapid feedback.
7.  **Independent Tests:** Ensure tests are independent and do not rely on each other.
8.  **High Priority:** Treat smoke tests as the highest priority and execute them with every build.

## Test Cases

Test cases will be written in Gherkin syntax and organized into feature files.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS (latest versions)
*   Test Framework: Playwright

## Test Data

Test data will include:

*   Valid search queries (e.g., "Dyson V15 Detect")
*   Valid product selections

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline.

## Metrics

*   Test Pass Rate
*   Test Failure Rate
*   Test Execution Time

