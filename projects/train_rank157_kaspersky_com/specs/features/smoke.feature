Feature: Kaspersky Homepage - Smoke Tests

  Scenario: Verify presence of key elements on the homepage
    @smoke
    Given I am on the Kaspersky homepage
    Then I should see 5 buttons
    And I should see 2 links
