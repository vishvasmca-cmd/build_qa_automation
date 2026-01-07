# Test Plan: core_saucedemo

## Introduction

This document outlines the test plan for the core_saucedemo e-commerce application. It details the scope, objectives, and strategy for testing the application's core functionalities.

## Scope

The testing will cover the following modules:

*   Authentication (Login/Logout)
*   Product Catalog (Sorting)
*   Shopping Cart (Add to Cart)
*   Checkout

## Objectives

*   Verify the core functionalities of the application are working as expected.
*   Identify any defects or issues that may impact the user experience.
*   Ensure the application meets the specified requirements.

## Test Strategy

The testing will be conducted using a combination of smoke and regression testing.

*   **Smoke Testing:** A quick and basic test to ensure the critical functionalities are working.
*   **Regression Testing:** A more comprehensive test to ensure that new changes have not introduced any new defects.

### Smoke Suite Strategy

The smoke suite will focus on the following critical functionalities:

1.  **Login:** Verify that users can successfully log in with valid credentials.
2.  **Product Listing:** Verify that products are displayed correctly.
3.  **Add to Cart:** Verify that users can add products to the cart.
4.  **View Cart:** Verify that the cart displays the correct items and quantities.
5.  **Checkout:** Verify that users can complete the checkout process.
6.  **Sorting:** Verify that users can sort products by price.
7.  **User Registration:** (Not in trace, but critical for e-commerce)
8.  **Basic Navigation:** (Verify main pages load)

## Test Suites

The following test suites will be created:

*   Smoke Suite
*   Regression Suite
