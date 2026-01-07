Feature: Home Page - Smoke Tests
  As a user
  I want to ensure the home page loads correctly and key elements are present

  @smoke
  Scenario: Verify Home Page Loads and Identify Links/Buttons
    Given the user navigates to "https://googlesyndication.com"
    Then the page should load successfully
    And the user should be able to identify at least 2 links
    And the user should be able to identify at least 5 buttons