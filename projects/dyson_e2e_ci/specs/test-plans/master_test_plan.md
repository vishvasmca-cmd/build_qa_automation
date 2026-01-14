# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The primary focus is on testing the core functionality of the Dyson India website, including:

*   Handling popups
*   Product search
*   Product detail page (PDP) verification

## Test Suites

### Smoke Suite

The smoke suite will cover the most critical paths to ensure the basic functionality of the application is working as expected. This suite will be executed after each build to quickly identify any major issues.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover essential user flows like searching for a product.
2.  **Core Business Logic:** Focuses on core e-commerce functions.
3.  **No Negative Testing:** Only positive scenarios are included.
4.  **No Complex Edge Cases:** Simple, straightforward flows are prioritized.
5.  **Fast Execution:** Tests are designed to run quickly.
6.  **High Stability:** Tests are reliable and unlikely to fail due to environment issues.
7.  **Independent Tests:** Tests do not depend on each other.
8.  **Clear Pass/Fail Criteria:** Results are easy to interpret.

### Regression Suite

The regression suite will provide comprehensive coverage of the application's functionality, including alternative flows, negative scenarios, and edge cases. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright

## Test Data

Test data will be used to simulate various user scenarios and ensure the application handles different types of input correctly. This may include valid and invalid search terms.

## Test Deliverables

*   Test Plan Document
*   Test Scripts (Playwright)
*   Test Results
*   Defect Reports
