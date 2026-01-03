# Master Test Plan: Delta Air Lines (delta.com) - Smoke Test

**Document Version:** 1.0
**Date:** October 26, 2023
**Author:** AI QA Strategist
**Target URL:** https://www.delta.com
**Business Domain:** Travel (Airline)
**Testing Type:** Smoke

## 1. Introduction

This document outlines the Master Test Plan for smoke testing the Delta Air Lines website (delta.com).  This plan focuses on verifying core functionality and ensuring the site is operational. It serves as a guide for autonomous agents to efficiently mine relevant information, execute critical test cases, and structure the test suite.

## 2. Domain Information & Analysis

**2.1. Domain:** Airline Travel (delta.com)

**2.2. Business Goal:** Delta Air Lines is a major airline providing air transportation services for passengers and cargo. The website serves as the primary interface for customers to:

*   Book flights
*   Manage reservations
*   Check flight status
*   Access SkyMiles account information
*   Get travel information
*   Contact customer support

**2.3. Key Areas of Focus for Testing:**

*   **Flight Booking:** The core functionality of the site.
*   **Account Management:** Accessing and managing user accounts.
*   **Information Resources:** Providing up-to-date travel information.
*   **Site Stability:** Ensuring the website is responsive and available.

## 3. Smoke Suite Definition

The Smoke Suite is designed to quickly verify the most critical functionalities of the Delta Air Lines website.  These tests are intended to be executed rapidly to confirm the site's basic health and readiness for further testing.

**3.1. Test Environment:**

*   Latest version of Chrome, Firefox, and Safari browsers.
*   Desktop resolution: 1920x1080

**3.2. Test Cases:**

**TC_SMOKE_001: Website Availability & Core Navigation**

*   **Description:**  Verify the Delta Air Lines website is accessible and that core navigation elements are functional.
*   **Steps:**
    1.  Navigate to https://www.delta.com.
    2.  Verify the page loads successfully (HTTP 200 status code).
    3.  Verify the presence of the main navigation menu (e.g., "Book," "My Trips," "SkyMiles").
    4.  Click on each of the main navigation links and verify that the corresponding pages load without errors.

**TC_SMOKE_002: Hero Headline Verification**

*   **Description:** Verify the hero headline on the Delta Air Lines homepage contains the expected text.
*   **Steps:**
    1.  Navigate to https://www.delta.com.
    2.  Locate the main hero headline element (XPath: `//h1` - adjust if needed).
    3.  Verify that the headline text contains "Keep climbing".

**TC_SMOKE_003: 'Book' Button Functionality**

*   **Description:** Verify that the 'Book' button is present and clickable, redirecting to the booking flow.
*   **Steps:**
    1.  Navigate to https://www.delta.com.
    2.  Locate the 'Book' button (CSS Selector: `.book-flight-module` - adjust if needed).
    3.  Verify that the button is visible and enabled.
    4.  Click the 'Book' button.
    5.  Verify that the user is redirected to the flight booking section (check for URL containing `/flight-search/`).

**3.3. Expected Results:**

*   All pages load successfully without errors.
*   Navigation links function correctly.
*   The hero headline contains the expected text ("Keep climbing").
*   The 'Book' button is functional and redirects to the flight booking section.

## 4. Strategic Mining Instructions

These instructions guide the autonomous agent on prioritizing specific elements and pages for deeper analysis and test case creation in future test cycles.

**4.1. High-Priority Elements for Mining:**

*   **Booking Form Elements:** All input fields (origin, destination, dates, number of passengers) and associated labels/validation messages within the "Book a Flight" section.
*   **Navigation Menu:**  All links and dropdown menus in the main navigation bar.  Specifically, the links under "Travel Info" and "SkyMiles" need to be mined.
*   **Flight Status Section:** Input field and associated "Check Status" button, including result display elements.
*   **Error Messages:** Any error messages displayed during the booking process (e.g., invalid date format, missing information).
*   **Accessibility Attributes:**  Prioritize mining `aria-label`, `role`, and `alt` attributes for accessibility testing in later phases.

**4.2. High-Priority Pages for Mining:**

*   **/flight-search/:** Flight search results page. Focus on extracting data elements related to flight information (price, duration, stops, aircraft type).
*   **/my-trips/:** Account login and "My Trips" section. Focus on form elements, data displayed, and actions available.
*   **/profile/:** User profile page to extract profile information labels and form input methods.
*   **/travel-info/:** Travel Information page to extract different categories like "Baggage", "Check-in", "Delta Discoveries", and "Travel Planning Center".

**4.3. Mining Techniques:**

*   **XPath and CSS Selectors:** Use a combination of XPath and CSS selectors to precisely target elements. Prioritize using attributes (e.g., `id`, `name`, `data-testid`) for more stable selectors.
*   **Regular Expressions:** Use regular expressions to extract specific data patterns (e.g., flight numbers, prices, dates) from text content.
*   **DOM Traversal:**  Use DOM traversal techniques to identify related elements (e.g., finding the label associated with an input field).
*   **API Mining:**  If possible, identify and analyze API calls made by the website to understand data flow and validation logic.

## 5. Test Data

Since this is a smoke test, minimal test data is needed. Focus should be on ensuring the basic functionality works.

*   Valid origin and destination airports (e.g., ATL, LAX).
*   Valid departure and arrival dates (within the current date range).

## 6. Reporting

The autonomous agent should generate a detailed report after each test run, including:

*   Test case execution status (Pass/Fail/Blocked).
*   Screenshots of any errors encountered.
*   Console logs.
*   Performance metrics (page load times).
*   Extracted element data from strategic mining (saved in a structured format like JSON or CSV).

## 7. Future Considerations

*   Expand the smoke suite to include more critical functionalities (e.g., flight check-in, SkyMiles login).
*   Implement data-driven testing using different sets of test data.
*   Integrate with a CI/CD pipeline for automated execution.
*   Develop accessibility tests to ensure the website is usable for people with disabilities.