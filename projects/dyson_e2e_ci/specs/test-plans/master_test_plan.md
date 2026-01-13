# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing scope covers essential functionalities such as product search, product detail page (PDP) verification, add-to-cart flow, and checkout process.

## Test Suites

1.  **Smoke Suite:**  A minimal set of tests to verify the core functionality of the application.
2.  **Regression Suite:** A comprehensive suite to ensure that new changes do not introduce regressions.

### Smoke Suite Strategy

The smoke suite is designed to provide rapid feedback on the health of the application. The following checklist is applied:

1.  **Critical Path Coverage:** Tests cover the most critical user flows (e.g., search, add to cart, checkout).
2.  **Core Business Logic:** Focus on testing the primary business logic related to product discovery and purchase.
3.  **Positive Testing:** Primarily focuses on positive scenarios (happy paths).
4.  **Minimal Negative Testing:** Only critical security-related negative tests are included.
5.  **No Complex Edge Cases:** Avoid complex or less common scenarios.
6.  **Fast Execution:** Tests should be quick to execute to provide rapid feedback.
7.  **Independent Tests:** Tests should be independent of each other to avoid cascading failures.
8.  **Stable Locators:** Use robust and stable locators to minimize test flakiness.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS (latest versions)
*   Test Framework: Playwright
*   Test Data: Use a combination of static and dynamically generated test data.

## Test Deliverables

*   Test Plan Document
*   Test Automation Scripts (Playwright)
*   Test Execution Reports
*   Defect Reports
