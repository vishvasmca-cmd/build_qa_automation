Feature: Homepage UI Elements Verification
  As a user,
  I want to verify the presence of key UI elements on the homepage
  So that I can ensure the basic functionality is available.

  @smoke
  Scenario: Verify presence of 5 buttons and 2 links
    Given I am on the homepage "https://ui.com/"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
