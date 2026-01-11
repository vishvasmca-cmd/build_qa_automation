# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will cover core e-commerce functionalities, ensuring a smooth user experience.

## Scope

The testing will cover the following areas:

*   Homepage
*   Product Search
*   Product Detail Page (PDP)
*   Shopping Cart
*   Checkout

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the stability and core functionality of the application. The following checklist is applied:

1.  **Critical Paths Only:** Focuses on the most essential user journeys (e.g., search, add to cart, checkout).
2.  **Positive Testing:** Primarily uses valid inputs and expected data.
3.  **Minimal Data Variation:** Uses a small, representative set of test data.
4.  **Independent Tests:** Each test should be able to run independently without relying on the state of others.
5.  **Fast Execution:** Tests should be designed for quick execution to provide rapid feedback.
6.  **Automated:** All smoke tests are automated for continuous integration.
7.  **Build Acceptance:** Passing smoke tests are a prerequisite for build acceptance.
8.  **Limited Scope:** Excludes edge cases, error handling, and less common scenarios.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes haven't introduced defects into existing functionality. This suite includes:

*   All Smoke Tests
*   Tests covering alternative flows (e.g., different payment methods).
*   Negative tests (e.g., invalid input, out-of-stock items).
*   Boundary value analysis.
*   Cross-module interactions.
*   Validation message verification.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright

## Test Data

Test data will be managed in a separate file and will include:

*   Search queries
*   Product information
*   User credentials
*   Payment information

## Metrics

*   Test pass/fail rate
*   Defect density
*   Test execution time

