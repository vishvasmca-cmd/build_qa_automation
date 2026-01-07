Feature: Snapchat Homepage - Smoke Tests
  As a user,
  I want to verify the basic elements on the Snapchat homepage
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify presence of buttons and links
    Given I navigate to the Snapchat homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
