# Test Plan: dyson_menu_test_ci

## Introduction

This document outlines the test plan for the dyson_menu_test_ci project, focusing on verifying the main menu navigation on the Dyson India website. The tests will ensure that all menu links are functional and lead to the correct pages.

## Scope

The scope of this test plan includes:

*   Verification of the main menu links (Deals, Vacuum & wet cleaners, Hair care, Air purifier, Headphones, Lighting, Support).
*   Ensuring that each menu link navigates to the correct corresponding page.

## Test Suites

This test plan includes two test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the core functionality of the Dyson India website's main menu. The following checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Focuses on the main menu navigation, a critical path for user experience.
2.  **Core Business Logic:** Ensures users can access key product categories.
3.  **Positive Testing:** Verifies successful navigation to each menu item.
4.  **No Negative Testing:**  Excludes scenarios with invalid inputs or error conditions.
5.  **Minimal Test Set:** Includes only the essential tests to confirm basic functionality.
6.  **Fast Execution:** Designed for quick execution to provide rapid feedback.
7.  **Build Validation:** Used to determine if a build is stable enough for further testing.
8.  **Happy Path Focus:** Concentrates on the ideal user flow without interruptions.

### Regression Suite

The Regression Suite will include more comprehensive tests to cover edge cases, error handling, and alternative flows. This suite will be developed in subsequent iterations.

## Test Cases

The following test cases will be included in the Smoke Suite:

*   **TC\_001:** Verify that clicking on each main menu link navigates to the correct page.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   URL: https://www.dyson.in/

## Test Execution

The tests will be executed using a CI/CD pipeline.

## Test Deliverables

*   Test Plan Document
*   Gherkin Feature Files
*   Test Execution Reports
