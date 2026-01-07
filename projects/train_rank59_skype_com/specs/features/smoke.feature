Feature: Skype Website - Element Identification
  As a user
  I want to verify the presence of key elements on the Skype website
  So that I can ensure the basic structure and navigation are functional

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the Skype homepage
    Then I should see the "Download Teams" button
    And I should see the "Sign in" button
    And I should see the "Open Teams in your browser" button
    And I should see the "Join a meeting" button
    And I should see the "Download the Teams app" button
    And I should see the "Teams meetings" link
    And I should see the "Need help?" link