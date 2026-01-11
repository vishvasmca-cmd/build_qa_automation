# Test Plan: Dyson E-commerce Website

## Introduction

This document outlines the test plan for the Dyson e-commerce website (www.dyson.in). The plan covers smoke and regression testing strategies to ensure the quality and stability of the website.

## Scope

The testing will cover the core functionalities of the Dyson website, including:

*   Navigation through main menu items
*   Page load verification
*   Popup handling

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the critical path of the website. This includes:

*   Handling the initial popup (if present).
*   Navigating through the main menu items (Deals, Vacuum & wet cleaners, Hair care, Air purifier, Headphones, Lighting, Support).
*   Verifying that each page loads successfully.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** The smoke tests cover the main navigation menu, which is a critical path for users to access different product categories and support information.
2.  **Core Business Logic:** Verifying that the main pages load successfully ensures that the core business logic of displaying product information and providing support is functional.
3.  **No Negative Testing:** The smoke tests do not include negative testing scenarios (e.g., invalid menu clicks).
4.  **No Complex Edge Cases:** The smoke tests focus on the happy path of navigating the main menu and do not cover complex edge cases.
5.  **Minimal Set:** The smoke suite is designed to be a minimal set of tests that can be executed quickly to verify the basic functionality of the website.
6.  **Build Rejection Criteria:** If any of the smoke tests fail, the build should be rejected, as it indicates a critical issue with the website's core functionality.
7.  **Positive Flow:** The smoke tests focus on positive flows, ensuring that users can successfully navigate the main menu and access the different pages.
8. **Essential Functionality:** The smoke tests cover the essential functionality of the website, ensuring that users can access the main product categories and support information.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including:

*   In-depth navigation testing of all menu items and sub-menus.
*   Broken link checking on all pages.
*   Testing of various page elements and functionalities.
*   Negative testing scenarios (e.g., invalid inputs, error handling).

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10
*   **URL:** https://www.dyson.in/

## Test Execution

*   The smoke suite will be executed after each build to ensure the stability of the core functionalities.
*   The regression suite will be executed periodically (e.g., weekly) to ensure the overall quality of the website.

## Test Deliverables

*   Test Plan Document
*   Test Cases (Gherkin Feature Files)
*   Test Execution Reports

