# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website.

## Scope

The testing will cover core e-commerce functionalities, including product search, adding to cart, and proceeding to checkout. The tests will be executed against the production environment (https://www.dyson.in/).

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick sanity check of the core functionalities. The following checklist has been applied to define the scope of the Smoke Suite:

1.  **Critical Paths:** Includes essential user flows like product search and checkout initiation.
2.  **Core Business Logic:** Focuses on the primary e-commerce functions.
3.  **Positive Testing:** Primarily focuses on happy path scenarios.
4.  **No Negative Testing:** Excludes negative scenarios unless critical for security.
5.  **No Complex Edge Cases:** Avoids complex or less common scenarios.
6.  **Limited Scope:** Keeps the number of test cases minimal for fast execution.
7.  **Independent Tests:** Each test should be independent and not rely on the state of others.
8.  **High Priority:** Failures in the smoke suite will block the release.

### Regression Suite

The Regression Suite will provide comprehensive coverage of all functionalities, including edge cases and negative scenarios. This suite will be executed less frequently than the Smoke Suite.

## Test Cases

Test cases will be written in Gherkin syntax and organized into feature files.

## Test Environment

*   **URL:** https://www.dyson.in/
*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS

## Test Data

Test data will include valid product names (e.g., Dyson V15 Detect) and user credentials (if applicable).

## Test Execution

The tests will be executed using a CI/CD pipeline. Test results will be automatically reported.
