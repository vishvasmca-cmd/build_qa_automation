# Test Plan: Dyson Menu Verification

## Introduction

This test plan outlines the strategy for testing the main menu navigation on the Dyson India website. The goal is to ensure that all menu links are functional and lead to the correct pages.

## Scope

This test plan covers the main menu items: Deals, Vacuum & wet cleaners, Hair care, Air purifier, Headphones, Lighting, and Support.

## Test Suites

This test plan includes a smoke test suite and a regression test suite.

### Smoke Suite Strategy

The smoke suite will focus on verifying the core functionality of the main menu. The following checklist is applied:

1.  **Critical Paths:** Tests the main navigation links.
2.  **Core Business Logic:** Ensures the basic navigation flow is working.
3.  **Positive Testing:** Only verifies that the links are working and the pages load.
4.  **No Negative Testing:** No negative scenarios are included in the smoke suite.
5.  **No Complex Edge Cases:** Only the main navigation links are tested.
6.  **Fast Execution:** The smoke suite should be quick to execute.
7.  **Independent Tests:** Each test should be independent of the others.
8.  **Automated:** The smoke suite will be fully automated.

### Regression Suite

The regression suite will cover more detailed scenarios, including:

*   Broken link verification on each page.
*   Checking sub-menu items.
*   Verifying content on each page.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files.

## Test Environment

*   Browser: Chrome
*   Operating System: Windows 10
*   Test Framework: Playwright

## Test Data

No specific test data is required for the smoke tests. The regression tests may require some test data for specific scenarios.
