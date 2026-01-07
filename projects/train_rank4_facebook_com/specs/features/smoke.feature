Feature: Facebook Homepage UI Elements Verification
  As a user,
  I want to verify the presence of key UI elements on the Facebook homepage
  So that I can ensure the basic structure and functionality are intact.

  @smoke
  Scenario: Verify the presence of buttons and links
    Given I am on the Facebook homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
