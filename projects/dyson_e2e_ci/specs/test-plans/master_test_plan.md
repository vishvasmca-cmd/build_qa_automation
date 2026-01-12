# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The goal is to ensure the website's core functionalities are working as expected and that recent changes haven't introduced regressions.

## Scope

The testing will cover the following areas:

*   Homepage
*   Product Listing Page (PLP)
*   Product Details Page (PDP)
*   Cart
*   Checkout

## Test Suites

This test plan includes two main test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the most critical functionalities of the Dyson India website. It focuses on happy path scenarios and core business logic.

**8-Point Checklist for Smoke Suite:**

1.  **Critical Paths Only:** Focuses solely on essential user journeys (e.g., product search, add to cart, checkout).
2.  **Happy Path Focus:**  Tests only positive scenarios without negative inputs or edge cases.
3.  **Core Functionality:** Verifies the primary functions of each page/module involved in the critical paths.
4.  **Minimal Data Variation:** Uses a single, representative data set for each scenario.
5.  **No External Dependencies (if possible):** Avoids tests that rely on external services that might be unstable.
6.  **Fast Execution:**  Designed to run quickly so that feedback is almost immediate.
7.  **Automated:** Fully automated for continuous integration.
8.  **Build Breaker:**  Failures in the smoke suite will result in the rejection of the build.

### Regression Suite

The Regression Suite is a comprehensive set of tests designed to ensure that new changes haven't broken existing functionality. It covers a wider range of scenarios, including alternative flows, negative cases, and edge cases.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each feature file will represent a specific area of the website.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   Test Framework: Playwright
*   Test Runner: Jest

## Test Data

Test data will be stored in separate files and used to parameterize the tests. This will allow for easy modification and maintenance of the test data.

## Reporting

Test results will be reported using the Jest reporter. The reports will include information about the number of tests run, the number of tests passed, and the number of tests failed.
