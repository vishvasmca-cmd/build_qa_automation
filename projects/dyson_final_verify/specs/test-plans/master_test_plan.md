# Test Plan: Dyson Final Verify

## Introduction

This document outlines the test plan for the Dyson Final Verify project. The goal is to ensure the core functionality of the Dyson India website is working as expected, focusing on searching for a product and verifying the presence of the 'Add to Cart' button.

## Scope

The testing will cover the following areas:

*   Homepage functionality
*   Search functionality
*   Product detail page

## Test Suites

This test plan includes two test suites:

*   Smoke Suite: A minimal set of tests to verify the core functionality.
*   Regression Suite: A comprehensive set of tests to ensure that new changes haven't introduced regressions.

### Smoke Suite Strategy

The Smoke Suite will focus on the critical path of searching for a product and verifying the 'Add to Cart' button. The following checklist has been applied:

1.  **Critical Path Coverage:** Covers the primary flow of searching and product verification.
2.  **Positive Testing:** Focuses on successful search and button verification.
3.  **No Negative Testing:** No invalid search terms or error conditions are tested.
4.  **Minimal Data Variation:** Uses a single, representative search term.
5.  **No Edge Cases:** Does not cover boundary conditions or unusual scenarios.
6.  **Independent Tests:** Each test can be run independently.
7.  **Fast Execution:** Tests are designed to execute quickly.
8.  **Automated:** All smoke tests are automated.

### Regression Suite

The Regression Suite will include more comprehensive tests, including:

*   Searching for different products
*   Handling search results with no products found
*   Verifying product details
*   Testing the 'Add to Cart' functionality
*   Checking for broken links

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   Test Framework: Playwright

## Test Data

*   Search Term: Dyson V15 Detect

## Test Deliverables

*   Test Plan Document
*   Automated Test Scripts (Playwright)
*   Test Execution Reports

## Roles and Responsibilities

*   QA Architect: Responsible for creating and maintaining the test plan.
*   QA Engineer: Responsible for writing and executing the test scripts.

