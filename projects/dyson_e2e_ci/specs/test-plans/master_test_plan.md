# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E-commerce website, focusing on end-to-end testing. The goal is to ensure the critical functionalities of the website are working as expected.

## Scope

The testing will cover the following areas:

*   Homepage
*   Product Search
*   Product Detail Page (PDP)
*   Add to Cart
*   Checkout

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the core functionalities of the Dyson website. The following checklist is applied to define the scope of the Smoke Suite:

1.  **Critical Paths:** Tests cover essential user flows like product search, adding to cart, and initiating checkout.
2.  **Core Business Logic:** Focuses on verifying the primary revenue-generating flows.
3.  **Positive Testing:** Primarily focuses on happy path scenarios.
4.  **No Negative Testing:** Excludes negative scenarios unless critical for security.
5.  **No Complex Edge Cases:** Avoids complex or less common scenarios.
6.  **Limited Data Variation:** Uses a minimal set of test data.
7.  **Fast Execution:** Tests are designed to execute quickly.
8.  **Build Validation:** Failure of any smoke test indicates a critical issue and potential build rejection.

### Regression Suite

The Regression Suite is a comprehensive set of tests to ensure that new changes haven't introduced any regressions. It covers a wider range of scenarios, including alternative flows, negative scenarios, and edge cases.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS (latest versions)
*   Test Framework: Playwright

## Test Data

Test data will be used to simulate different user scenarios and product variations.

## Test Deliverables

*   Test Plan Document
*   Test Automation Scripts
*   Test Execution Reports
*   Defect Reports
