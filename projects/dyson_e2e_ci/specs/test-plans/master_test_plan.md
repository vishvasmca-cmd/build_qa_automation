# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated using Playwright and follow a Behavior-Driven Development (BDD) approach with Gherkin syntax.

## Scope

The scope of this test plan includes:

*   Smoke testing of core functionality (search, add to cart, checkout).
*   Regression testing to ensure existing functionality remains intact after changes.

## Test Suites

1.  **Smoke Suite:**  A minimal set of tests to verify the core functionality of the application.
2.  **Regression Suite:** A comprehensive suite to ensure that new changes do not introduce regressions.

The smoke suite will focus on verifying the most critical paths through the application. These tests are designed to be quick and efficient, providing a rapid assessment of the application's health.

**Smoke Suite Strategy (8-Point Checklist)**

1.  **Critical Paths Only:** Focuses solely on the most essential user flows (e.g., search, add to cart, checkout).
2.  **Positive Testing:** Primarily uses positive test cases (happy path) to ensure core functionality is working.
3.  **Minimal Data Variation:** Uses a limited set of data to minimize execution time.
4.  **No Edge Cases:** Excludes complex edge cases or boundary conditions.
5.  **No Error Handling:** Does not explicitly test error handling or negative scenarios.
6.  **Independent Tests:** Each test should be independent and not rely on the state of previous tests.
7.  **Fast Execution:** Tests should be designed for quick execution to provide rapid feedback.
8.  **High Priority:** Smoke tests are given the highest priority and are executed before any other tests.

### Regression Suite

The regression suite will provide comprehensive coverage of the application's functionality, including alternative flows, negative scenarios, and boundary conditions. These tests will ensure that new changes have not introduced regressions into the existing codebase.

## Test Environment

*   Browser: Chromium, Firefox, Webkit
*   Operating System: Windows, macOS, Linux
*   Test Framework: Playwright
*   Language: JavaScript/TypeScript

## Test Cases

Test cases will be written in Gherkin syntax and organized into feature files. Each feature file will represent a specific area of functionality.
