# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The goal is to ensure the website's core functionalities are working as expected and to prevent regressions with new code deployments.

## Scope

The testing will cover the following areas:

*   Homepage
*   Product Search
*   Product Display Page (PDP)
*   Shopping Cart
*   Checkout Process

## Test Suites

This test plan includes two main test suites:

1.  Smoke Suite: A minimal set of tests to verify the core functionality.
2.  Regression Suite: A comprehensive set of tests to cover various scenarios and edge cases.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick and efficient way to validate the stability of the application after deployment. The following checklist is applied to this project:

1.  **Critical Paths:** Tests cover the most critical user flows (e.g., search, add to cart, checkout).
2.  **Core Business Logic:** Focuses on testing the primary revenue-generating flows.
3.  **Positive Testing:** Primarily focuses on happy path scenarios.
4.  **Minimal Negative Testing:** Only critical security-related negative tests are included.
5.  **No Complex Edge Cases:** Complex scenarios and edge cases are excluded from the smoke suite.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Independent Tests:** Each test should be independent and not rely on the state of other tests.
8.  **High Priority:** Any failures in the smoke suite will result in build rejection.

## Test Cases

Detailed test cases are defined in the feature files (see below).

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows/macOS/Linux (cross-platform)
*   Test Framework: Playwright

## Test Execution

*   The Smoke Suite will be executed after each build.
*   The Regression Suite will be executed on a regular schedule (e.g., nightly) or before major releases.

## Metrics

*   Test Pass/Fail Rate
*   Test Execution Time
*   Defect Density

