# Test Plan: Atlassian Jira Smoke Tests

## Introduction

This test plan outlines the smoke tests for the Atlassian Jira application. The purpose of these tests is to ensure the application's core functionality is working as expected and that the system is stable for further testing.

## Scope

The smoke tests will cover the following areas:

*   Application Availability and Performance
*   Critical Navigation
*   Core Business Functionality
*   Basic Data Flow
*   Authentication
*   API Health
*   Environment

## Smoke Suite Strategy

The Smoke Suite is designed based on the following principles:

1.  **Application Availability**: Verify the Jira homepage loads correctly, checking for the presence of critical assets (JS/CSS) and ensuring the URL is accessible.
2.  **Critical Navigation**: Test the main menu and navigation links, ensuring they redirect to the correct pages.
3.  **Core Business Functionality (Happy Path)**: Focus on one happy path for the core feature of signing up for a free trial.
4.  **Basic Data Flow**:  After clicking 'Try it Free', ensure the signup page loads.
5.  **Authentication**:  Not in scope for this trace.
6.  **API Health**: Check that key API endpoints related to signup return a 200 OK status (this would be for actual Signup).
7.  **Environment**: Not in scope for this trace.
8.  **Hero Headline Verification**: Confirm the main landing page contains the correct hero headline.

## Test Cases

The following test cases will be executed as part of the smoke test suite:

1.  **Verify Jira Homepage Loads Successfully:**
    *   Navigate to the Jira homepage.
    *   Verify the page loads without errors.
    *   Verify critical assets (JS/CSS) are loaded.
2.  **Verify Hero Headline:**
    *   Navigate to the Jira homepage.
    *   Verify the hero headline contains 'Plan, track, and release great software'.
3.  **Verify 'Try it Free' Button Navigation:**
    *   Navigate to the Jira homepage.
    *   Click the 'Try it Free' button.
    *   Verify that the user is redirected to a page related to Jira free trial signup.

## Test Environment

The tests will be executed against the production environment.

## Entry Criteria

The following criteria must be met before executing the smoke tests:

*   The Jira application must be deployed and accessible.

## Exit Criteria

The following criteria must be met for the smoke tests to be considered successful:

*   All smoke tests must pass.

## Test Deliverables

*   Test Plan
*   Test Results
*   BDD Feature Files
