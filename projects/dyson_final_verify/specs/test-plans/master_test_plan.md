# Test Plan: Dyson Final Verify

## Introduction

This document outlines the test plan for the Dyson Final Verify project. The goal is to ensure the core functionality of the Dyson India website is working as expected, specifically focusing on searching for a product and verifying the presence of the 'Add to Cart' button.

## Scope

The scope of this test plan includes:

*   Searching for 'Dyson V15 Detect'.
*   Verifying the presence of the 'Add to Cart' button on the product page.

## Test Suites

This test plan includes the following test suites:

*   Smoke Suite: A minimal set of tests to verify the core functionality.
*   Regression Suite: A comprehensive set of tests to ensure that recent changes have not broken existing functionality.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick and efficient way to verify the stability of the Dyson India website. The following checklist is applied to this project:

1.  **Critical Paths:** Focuses on the most critical user flow (searching and verifying 'Add to Cart').
2.  **Core Business Logic:** Verifies the basic search functionality.
3.  **Positive Testing:** Only positive scenarios are considered (successful search, 'Add to Cart' button present).
4.  **No Negative Testing:** Negative scenarios (e.g., invalid search query) are excluded.
5.  **No Complex Edge Cases:** Complex scenarios are not considered.
6.  **Fast Execution:** The tests are designed to execute quickly.
7.  **High Priority:** Any failure in the Smoke Suite will result in build rejection.
8.  **Limited Scope:** Only the essential functionality is covered.

### Regression Suite

The Regression Suite will include more comprehensive tests, including:

*   Searching for different products.
*   Verifying different elements on the product page.
*   Negative search scenarios (e.g., invalid search query).
*   Edge cases (e.g., searching for products with special characters).

## Test Cases

Test cases will be documented in the Gherkin feature files.
