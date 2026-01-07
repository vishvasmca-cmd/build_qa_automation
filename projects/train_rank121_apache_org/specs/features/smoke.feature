Feature: Apache.org Homepage UI Elements Verification
  As a user,
  I want to verify the presence of key UI elements on the Apache.org homepage
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Verify presence of buttons, links, and menu bars
    Given I am on the Apache.org homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
