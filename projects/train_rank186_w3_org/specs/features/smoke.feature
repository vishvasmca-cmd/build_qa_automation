Feature: W3.org Homepage - Smoke Tests

  Scenario: Verify presence of buttons and links
    @smoke
    Given I am on the W3.org homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
