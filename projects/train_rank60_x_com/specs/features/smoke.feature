Feature: Home Page - Element Identification
  As a user,
  I want to verify the presence of key elements on the home page
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the x.com home page
    Then I should see at least 5 buttons
    And I should see at least 2 links
