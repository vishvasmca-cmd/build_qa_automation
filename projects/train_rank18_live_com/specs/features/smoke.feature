Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the "https://live.com" homepage
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And the page should load successfully
