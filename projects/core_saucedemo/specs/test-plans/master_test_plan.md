# Test Plan: core_saucedemo

## Introduction

This document outlines the test plan for the core_saucedemo e-commerce application. It details the testing scope, strategy, and specific test cases to be executed.

## Test Scope

The testing will cover the following modules:

*   Authentication (Login/Logout)
*   Product Catalog (Sorting)
*   Shopping Cart (Add to Cart)
*   Checkout & Payments (Basic Checkout Flow)

## Test Strategy

The testing will be conducted using a combination of smoke and regression testing.

*   **Smoke Testing:**  A quick verification of the core functionalities to ensure the application is stable and ready for further testing.
*   **Regression Testing:** A more comprehensive testing approach to ensure that new changes or bug fixes have not introduced new issues or broken existing functionality.

### Smoke Suite Strategy

The smoke suite will focus on the following critical aspects:

1.  **Critical Path Coverage:** Tests cover the most common and essential user flows.
2.  **Positive Testing:** Primarily focuses on successful scenarios (happy paths).
3.  **Core Functionality:** Verifies the basic functions of each module.
4.  **Build Verification:** Determines if the build is stable enough for further testing.
5.  **Limited Scope:**  Keeps the test suite small and fast to execute.
6.  **High Priority:**  Smoke tests are executed before any other tests.
7.  **No Edge Cases:** Avoids complex or unusual scenarios.
8.  **Data Driven:** Uses a standard user.

## Test Suites

The following test suites will be executed:

*   Smoke Suite
*   Regression Suite

## Test Cases

Detailed test cases are defined in the BDD feature files.
