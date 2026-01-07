# Test Plan: MTS.RU

## Introduction

This document outlines the test plan for MTS.RU, focusing on verifying the presence of key UI elements (buttons and links) on the homepage. The tests will be executed against the production environment.

## Scope

The scope of this test plan includes:

*   Verification of the presence of 5 buttons on the homepage.
*   Verification of the presence of 2 links on the homepage.
*   Verification of the presence of 2 menu bars on the homepage.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   URL: <https://mts.ru>

## Test Strategy

This test plan will employ both smoke and regression testing strategies.

### Smoke Suite Strategy

The smoke suite will focus on verifying the core functionality of the application. The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** The primary navigation and key UI elements (buttons and links) are verified.
2.  **Core Business Logic:** N/A (This is a UI element presence check, not business logic).
3.  **No Negative Testing:** Only positive assertions (element is present) are performed.
4.  **No Complex Edge Cases:** Simple presence checks, no complex scenarios.
5.  **Minimal Scope:** Only the homepage is included.
6.  **Fast Execution:** Tests are designed to be quick to execute.
7.  **Build Validation:** Failure of any smoke test indicates a critical issue.
8.  **Happy Path Focus:** Only verifies the expected elements are present.

### Regression Suite Strategy

Due to the limited scope of the trace data, a full regression suite cannot be defined at this time. However, a regression suite would typically include:

*   Verification of button and link functionality (e.g., click actions).
*   Verification of menu bar navigation.
*   Cross-browser compatibility testing.
*   Responsive design testing.

## Test Cases

The following test cases will be executed:

*   **TC\_001:** Verify the presence of 5 buttons on the homepage.
*   **TC\_002:** Verify the presence of 2 links on the homepage.
*   **TC\_003:** Verify the presence of 2 menu bars on the homepage.

## Test Deliverables

*   Test Plan document
*   Gherkin feature files
*   Test execution reports

## Test Automation

The tests will be automated using Playwright.
