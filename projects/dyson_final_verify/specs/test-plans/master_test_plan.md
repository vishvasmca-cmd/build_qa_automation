# Test Plan: Dyson Final Verify

## Introduction

This document outlines the test plan for the Dyson Final Verify project. It includes smoke and regression test suites designed to ensure the quality and stability of the Dyson India website.

## Test Scope

The tests will cover the core functionality of the Dyson India website, focusing on search functionality and product verification.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the critical path of searching for a product and verifying its availability. This suite will be executed after each build to ensure the core functionality is working as expected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Focus on the most important user flows (e.g., searching for a product).
2.  **Core Business Logic:** Verify the primary function of searching and product availability.
3.  **Positive Testing:** Primarily positive tests, ensuring the happy path works.
4.  **Minimal Data Sets:** Use a small, representative set of data for testing.
5.  **Fast Execution:** Tests should be quick to execute, providing rapid feedback.
6.  **Independent Tests:** Tests should be independent of each other.
7.  **Automated Execution:** The smoke suite should be fully automated.
8.  **Build Acceptance:** Passing smoke tests are required for build acceptance.

### Regression Suite

The regression suite will cover a broader range of scenarios, including alternative flows, negative scenarios, and boundary conditions. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each feature file will contain a set of scenarios that test a specific feature or functionality.
