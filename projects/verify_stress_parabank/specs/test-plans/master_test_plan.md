# Test Plan: ParaBank Exploration

## Introduction

This test plan outlines the testing strategy for exploring the ParaBank website. The primary goal is to ensure the basic functionality and navigation of the site are working as expected.

## Scope

The scope of this test plan includes:

*   Navigation between different pages.
*   Verification of key links and buttons.
*   Basic functionality of the site map.
*   Customer lookup functionality.

## Test Suites

This test plan defines two test suites: Smoke and Regression.

### Smoke Suite Strategy

The Smoke Suite is designed to quickly verify the core functionality of the ParaBank website. The following checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential navigation flows, such as accessing the site map and customer lookup.
2.  **Core Business Logic:** Focuses on the primary function of providing banking services information and access.
3.  **No Negative Testing:** Only positive scenarios are included in the smoke tests.
4.  **No Complex Edge Cases:** Simple and straightforward scenarios are prioritized.
5.  **Minimal Test Set:** The suite includes a minimal set of tests to provide quick feedback.
6.  **Automated Execution:** The smoke tests are designed for automated execution.
7.  **Fast Execution Time:** The tests should execute quickly to provide rapid feedback.
8.  **Build Validation:** The smoke tests are used to validate new builds.

### Regression Suite Strategy

The Regression Suite is designed to ensure that new changes have not introduced any regressions in the existing functionality of the ParaBank website. This suite will include more comprehensive tests, including alternative flows, negative scenarios, and boundary analysis.

## Test Cases

Test cases will be documented in Gherkin feature files.

## Test Environment

The tests will be executed in a standard web browser environment.

## Test Data

Test data will be used to simulate different user scenarios.
