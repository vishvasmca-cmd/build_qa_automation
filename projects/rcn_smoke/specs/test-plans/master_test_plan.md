# Test Plan: RCN Smoke Suite

## Introduction

This test plan outlines the strategy for the smoke test suite for the RCN (Astound) application. The smoke tests are designed to verify the basic functionality and stability of the application in a production-like environment.

## Scope

The smoke tests will cover the following areas:

*   Application availability and basic functionality.
*   Critical user workflows.
*   Basic data flow.

## Smoke Suite Strategy

The smoke test suite is designed based on the following principles:

1.  **Application Availability**: Verify load, URL, and critical assets (JS/CSS).
2.  **Critical Navigation**: Main menu, Home -> Products/Search/Help (where applicable in this domain).
3.  **Core Business Functionality (Happy Path)**: ONE happy path per major feature (e.g., Login -> Billing Overview).
4.  **Basic Data Flow**: Verify results appear (e.g., Billing data is displayed after login).
5.  **Authentication**: Login/Logout (Standard User only). NO invalid creds tests.
6.  **API Health**: Critical endpoints return 200 (Auth, Billing). (Implicit through UI tests).
7.  **Environment**: Version check, Feature flags (Not directly testable from provided trace).
8. **SMS Notifications**: Verify functionality of enabling and disabling SMS notifications.

## Test Cases

The following test cases will be included in the smoke test suite:

1.  **Verify Application Availability**: Ensure the application is accessible and loads correctly.
2.  **User Login**: Verify that a user can successfully log in with valid credentials.
3.  **Billing Overview**: Verify that the billing information is displayed after login.
4.  **Enable SMS Notifications**: Verify that SMS notifications can be enabled.
5. **User Logout**: Verify that user can successfully logout from the application.

## Test Environment

The smoke tests will be executed in a production-like environment.

## Test Data

The following test data will be used:

*   Valid user credentials (vishvas.mca@gmail.com / Myaccount@123)

## Entry Criteria

*   The application is deployed to the test environment.
*   The test environment is stable.

## Exit Criteria

*   All smoke tests have passed.

## Test Deliverables

*   Test Plan
*   Test Cases
*   Test Results

## Roles and Responsibilities

*   QA Architect: Responsible for creating and maintaining the test plan and test cases.
*   QA Engineer: Responsible for executing the test cases and reporting the results.

## Test Schedule

The smoke tests will be executed daily or as needed.
