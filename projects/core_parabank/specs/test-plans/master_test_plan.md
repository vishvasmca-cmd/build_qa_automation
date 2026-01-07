# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities related to account access and information retrieval. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover the following areas:

*   Account Access (Login)
*   Navigation to key pages (Account History, About Us)

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. These tests are designed to be executed quickly and efficiently to ensure that the application is in a stable state.

#### Smoke Suite Strategy

The following 8-point checklist was applied when designing the smoke suite:

1.  **Critical Paths:** The smoke tests cover the most critical user paths, such as accessing key pages.
2.  **Core Business Logic:** The tests verify the basic functionality of the application.
3.  **No Negative Testing:** The smoke tests focus on positive scenarios and do not include negative test cases.
4.  **No Complex Edge Cases:** The tests avoid complex or edge-case scenarios.
5.  **Speed:** The smoke tests are designed to be executed quickly.
6.  **Stability:** The tests are reliable and should not fail due to environmental issues.
7.  **Independence:** The tests are independent of each other and can be executed in any order.
8.  **Automation:** The tests are automated to ensure repeatability.

### Regression Suite

The regression suite will include a more comprehensive set of tests to ensure that new changes have not introduced any regressions. These tests will cover a wider range of scenarios, including edge cases and negative test cases.

## Test Environment

The tests will be executed in a dedicated test environment that mirrors the production environment.

## Test Deliverables

*   Test Plan Document
*   Test Cases (Gherkin Feature Files)
*   Test Execution Reports

