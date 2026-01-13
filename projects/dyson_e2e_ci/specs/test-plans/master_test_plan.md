# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The primary goal is to ensure the stability and functionality of key features through automated testing.

## Scope

The testing scope includes:

*   **Smoke Tests:** Verify core functionality, such as searching for a product, adding it to the cart, and proceeding to checkout.
*   **Regression Tests:** Cover a broader range of scenarios, including alternative flows, negative testing, and boundary conditions.

## Test Suites

1.  **Smoke Suite:**
    *   Objective: To quickly verify the most critical functionalities of the Dyson India website.
    *   Execution Frequency: After each build/deployment.
    *   Environment: Staging environment.

2.  **Regression Suite:**
    *   Objective: To ensure that new changes haven't introduced regressions in existing functionality.
    *   Execution Frequency: Nightly or weekly, depending on the release cycle.
    *   Environment: Staging environment.

## Smoke Suite Strategy

The Smoke Suite is designed to provide a rapid assessment of the application's health. The following checklist is applied:

1.  **Critical Path Coverage:** Tests cover the most essential user flows (e.g., login, search, checkout).
2.  **Positive Testing:** Focus on happy path scenarios with valid inputs.
3.  **Minimal Data Variation:** Use a small, representative set of test data.
4.  **Independent Tests:** Each test should be independent and not rely on the state of previous tests.
5.  **Fast Execution:** Tests should be designed for quick execution to provide rapid feedback.
6.  **High Priority:** Any failures in the smoke suite should be treated as critical and addressed immediately.
7.  **Automated Execution:** The suite should be fully automated for continuous integration.
8.  **Environment Stability:** Execute smoke tests in a stable and representative environment.

## Test Cases

Test cases will be written in Gherkin syntax and automated using Playwright.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright
*   Programming Language: JavaScript/TypeScript

## Test Data

Test data will be managed within the test scripts or in separate data files.

## Metrics

*   Test Pass Rate
*   Test Execution Time
*   Defect Density

