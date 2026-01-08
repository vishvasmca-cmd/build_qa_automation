# Test Plan: ParaBank

## Introduction

This document outlines the test plan for ParaBank, a demo website for online banking. The plan covers smoke and regression testing to ensure the quality and stability of the application.

## Scope

The testing will cover the following functionalities:

*   User Registration
*   User Login
*   Opening a New Account
*   Transferring Funds
*   Requesting a Loan

## Test Suites

### Smoke Suite

The smoke suite will focus on the core functionalities of the application to ensure that the basic features are working as expected. This suite will be executed after each build to quickly identify any critical issues.

#### Smoke Suite Strategy

The smoke suite strategy is based on the following 8-point checklist:

1.  **Critical Path Coverage:** Tests cover the most common and important user flows.
2.  **Positive Testing:** Primarily focuses on happy path scenarios with valid inputs.
3.  **Minimal Data Variation:** Uses a limited set of test data to keep execution time short.
4.  **Independent Tests:** Tests are designed to be independent and can be run in any order.
5.  **Fast Execution:** Tests should execute quickly to provide rapid feedback.
6.  **Clear Pass/Fail Criteria:** Each test has a clear and unambiguous pass/fail criteria.
7.  **Automation Priority:** Tests are automated for consistent and repeatable execution.
8.  **Build Acceptance:** Successful completion of the smoke suite is required for build acceptance.

The following scenarios will be included in the smoke suite:

*   Successful User Registration
*   Successful User Login

### Regression Suite

The regression suite will cover a wider range of functionalities and scenarios to ensure that existing features are not broken by new changes. This suite will be executed periodically or before major releases.

The following scenarios will be included in the regression suite:

*   All scenarios from the smoke suite
*   User Registration with invalid data
*   User Login with invalid credentials
*   Opening a New Account with different account types
*   Transferring Funds between different accounts
*   Requesting a Loan with different loan amounts and down payments

## Test Environment

The tests will be executed in the following environment:

*   Browser: Chrome
*   Operating System: Windows 10
*   Test Automation Framework: Playwright

## Test Data

Test data will be generated and managed using a dedicated test data management strategy. This will ensure that the tests are repeatable and reliable.
