# Test Plan: core_parabank

## Overview

This test plan outlines the testing strategy for the core_parabank application, focusing on verifying critical functionalities and ensuring a stable user experience. The plan includes both Smoke and Regression test suites, designed to cover essential workflows and edge cases within the banking domain.

## Scope

The testing will cover the following modules:

*   Account Access
*   Statements & History

## Test Suites

### Smoke Suite

The Smoke Suite is a collection of high-priority tests designed to quickly verify the core functionality of the application. These tests are executed to ensure that the system is stable and that the most critical features are working as expected. If smoke tests fail, the build is rejected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths**: Focus on the most essential user flows (e.g., Login, Account Access).
2.  **Core Business Logic**: Cover primary revenue or operational flows.
3.  **Positive Testing**: Primarily focus on successful scenarios.
4.  **No Negative Testing**: Exclude negative scenarios unless they represent critical security concerns.
5.  **No Complex Edge Cases**: Avoid complex or unusual scenarios.
6.  **Minimal Data Variation**: Use a small, representative set of test data.
7.  **Independent Tests**: Ensure tests can be run independently without dependencies.
8.  **Fast Execution**: Design tests for quick execution to provide rapid feedback.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes or bug fixes have not introduced unintended side effects or broken existing functionality. This suite includes a wider range of scenarios, covering alternative flows, negative cases, boundary conditions, and cross-module interactions.

## Test Modules

### Account Access (Criticality: Critical)

#### Smoke Tests

*   Verify navigation to the About Us page.
*   Verify navigation back to the Home page.
*   Verify the ability to navigate to the Account History page.

#### Regression Tests

*   Verify error messages when entering invalid credentials.
*   Test password recovery functionality.
*   Test account lockout after multiple failed login attempts.

### Statements & History (Criticality: Medium)

#### Smoke Tests

*   Verify navigation to the Account History page.

#### Regression Tests

*   Verify the ability to search transactions by date range.
*   Verify the ability to filter transactions by type.
*   Verify the ability to download statements in different formats (PDF, CSV).

## Test Data

Test data will be managed centrally and will include valid and invalid credentials, account numbers, and transaction details.

## Test Environment

The tests will be executed in a dedicated test environment that mirrors the production environment. This includes the operating system, database, and network configuration.
