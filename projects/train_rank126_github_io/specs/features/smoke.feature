Feature: Homepage UI Elements Verification
  As a user
  I want to verify the presence of key UI elements on the homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify the presence of buttons and links
    Given I am on the "https://github.io" homepage
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
