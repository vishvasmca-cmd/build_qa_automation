# Test Plan: Dyson E-commerce Website

## Introduction

This document outlines the test plan for the Dyson e-commerce website (dyson.in). The plan includes smoke and regression test suites to ensure the quality and stability of the website.

## Scope

The testing will cover the core functionalities of the website, including:

*   Navigation
*   Page Loading
*   Popup Handling

## Test Suites

### Smoke Suite

The smoke suite will focus on the critical path of the website to ensure that the core functionalities are working as expected. This suite will be executed after each build to quickly identify any major issues.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like navigating the main menu.
2.  **Core Business Logic:** Verifies basic page loading and navigation.
3.  **Positive Testing:** Focuses on successful navigation through the menu.
4.  **No Negative Testing:** No invalid inputs or error conditions are tested in the smoke suite.
5.  **No Complex Edge Cases:** Simple navigation is tested, not complex scenarios.
6.  **Fast Execution:** The smoke tests are designed to be quick to execute.
7.  **Build Validation:** Failure of any smoke test indicates a critical issue.
8.  **Limited Scope:** Only the main menu navigation is covered.

### Regression Suite

The regression suite will cover a broader range of functionalities, including edge cases and error handling. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files.

## Test Environment

The tests will be executed in a Chrome browser.

## Test Data

No specific test data is required for the smoke tests.
