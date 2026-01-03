# Test Plan: Careerraah.com Smoke Tests

## Introduction

This test plan outlines the smoke tests for Careerraah.com, an education platform. The purpose of these tests is to ensure the application's availability, basic functionality, and overall health after deployment or major changes.

## Scope

The smoke tests will cover the following areas:

*   Application Availability
*   Critical Navigation
*   Core Business Functionality
*   Basic Data Flow
*   Authentication (if applicable)
*   API Health (critical endpoints)
*   Environment Verification

## Smoke Suite Strategy

The smoke test suite is designed based on the following principles:

1.  **Application Availability**: Verify the website loads successfully and that critical assets (JS/CSS) are accessible.
2.  **Critical Navigation**: Test the main menu links and navigation to key pages (Home -> Products/Search/Help, if applicable).
3.  **Core Business Functionality (Happy Path)**: Execute ONE happy path for each major feature (e.g., Course browsing -> Detail -> Contact).
4.  **Basic Data Flow**: Ensure data is displayed correctly (e.g., Courses appear on listing pages).
5.  **Authentication**: Verify login/logout functionality for a standard user (NO invalid credentials tests).
6.  **API Health**: Check that critical API endpoints return a 200 OK status (e.g., Auth, Course, etc.).
7.  **Environment**: Validate the application version and feature flag settings.
8.  **Contact Form Submission**: Verify that a user can submit a contact form successfully.

## Test Cases

| Test Case ID | Description                                                        | Steps                                                                                                                                    | Expected Result                                                                                               |
|--------------|--------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| SMOKE-001    | Verify Homepage Loads                                             | 1. Navigate to the homepage (https://www.careerraah.com/).                                                                            | The homepage should load successfully without any errors.                                                      |
| SMOKE-002    | Navigate to Blog Page                                              | 1. From the homepage, click the "Blog" link.                                                                                              | The Blog page should load successfully.                                                                      |
| SMOKE-003    | Submit Contact Form                                                | 1. Navigate to the Contact Us page. 2. Fill in the Name, Email, Subject, and Message fields. 3. Click the "Send Message" button. | The contact form should be submitted successfully, and a confirmation message should be displayed (if present). |

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   Network: Stable internet connection

## Test Data

*   Name: Test User
*   Email: test@example.com
*   Subject: Test Subject
*   Message: This is a test message.

## Entry Criteria

*   The application is deployed to the test environment.
*   All necessary configurations are in place.

## Exit Criteria

*   All smoke tests have passed.
*   No critical defects are identified.

## Roles and Responsibilities

*   QA Architect: Designs and maintains the test plan and smoke suite.
*   QA Engineer: Executes the smoke tests and reports the results.
