# Test Plan: Criteo Website

## Introduction

This test plan outlines the testing strategy for the Criteo website, focusing on verifying the presence of key elements like buttons and links on the homepage. The plan includes both smoke and regression testing strategies to ensure the stability and functionality of the website.

## Scope

This test plan covers the homepage of the Criteo website (https://criteo.com). The focus is on identifying and verifying the presence of specific UI elements, namely buttons and links, without interacting with them.

## Test Strategy

The testing strategy consists of two main suites: Smoke and Regression.

### Smoke Suite Strategy

The smoke suite will focus on verifying the most critical functionality of the Criteo website. For this project, the smoke tests will ensure that key elements (buttons and links) are present on the homepage. The following 8-point checklist has been applied to define the smoke suite:

1.  **Critical Paths:** Verify the presence of key UI elements on the homepage.
2.  **Core Business Logic:** Ensure that the basic structure of the homepage is intact.
3.  **No Negative Testing:** No negative tests are included in the smoke suite.
4.  **No Complex Edge Cases:** No complex edge cases are considered in the smoke suite.
5.  **Fast Execution:** The smoke tests should execute quickly.
6.  **Minimal Scope:** The smoke suite covers only the most essential functionality.
7.  **Build Acceptance:** Failure of any smoke test indicates a critical issue and should reject the build.
8.  **Happy Path Focus:** Smoke tests focus on the happy path, assuming ideal conditions.

### Regression Suite Strategy

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, and edge cases. However, based on the provided trace data, a regression suite is not defined at this time, as the trace only covers identifying elements without interaction.

## Test Suites

1.  **Smoke Suite:**
    *   Verify the presence of at least 5 buttons on the homepage.
    *   Verify the presence of at least 2 links on the homepage.
    *   Verify the presence of at least 2 menu bars on the homepage.

2.  **Regression Suite:** (Not defined based on the provided trace data)

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   Network: Stable internet connection

## Test Deliverables

*   Test Plan Document
*   Gherkin Feature Files
*   Test Execution Reports
