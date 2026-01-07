Feature: Amazon Homepage UI Elements Verification
  As a tester
  I want to verify the presence of specific UI elements on the Amazon homepage
  So that I can ensure the basic structure and content of the page are loading correctly

  @smoke
  Scenario: Verify the presence of buttons and links on the Amazon homepage
    Given I am on the Amazon homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
