# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The goal is to ensure the website functions correctly and provides a seamless user experience.

## Test Scope

The testing will cover core functionalities such as:

*   Handling popups
*   Searching for products
*   Product Detail Page (PDP) verification
*   Add to Cart functionality
*   Checkout process

## Test Strategy

The test strategy will consist of two main suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite will focus on verifying the most critical functionalities of the website. The following checklist is applied:

1.  **Critical Path Coverage:** Tests cover essential user journeys (e.g., product search, add to cart, checkout).
2.  **Core Business Logic:** Focus on testing the primary revenue-generating flows.
3.  **Positive Testing:** Primarily focuses on happy path scenarios.
4.  **Minimal Negative Testing:** Only critical security-related negative tests are included.
5.  **No Complex Edge Cases:** Avoid complex or less common scenarios.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Build Validation:** Failure of any smoke test indicates a critical issue and may reject the build.
8.  **Limited Scope:** Only the most vital functionalities are included.

### Regression Suite Strategy

The Regression Suite will provide comprehensive coverage of the website's functionalities, including alternative flows, negative scenarios, and edge cases. This suite will ensure that new changes do not introduce regressions in existing functionalities.

## Test Suites

1.  **Smoke Suite:**
    *   Objective: Verify critical functionalities are working after deployment.
    *   Scope: As defined in the Smoke Suite Strategy.
2.  **Regression Suite:**
    *   Objective: Ensure that new changes have not broken existing functionalities.
    *   Scope: Comprehensive coverage of all functionalities, including edge cases and negative scenarios.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Data: Use a combination of valid and invalid test data to ensure proper validation and error handling.

## Test Deliverables

*   Test Plan Document
*   Test Automation Scripts (Playwright)
*   Test Execution Reports
*   Defect Reports
