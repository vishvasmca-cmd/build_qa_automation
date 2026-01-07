Feature: Discord Homepage - Element Identification
  As a user,
  I want to ensure that key elements on the Discord homepage are present and identifiable,
  so that I can navigate and use the website effectively.

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the Discord homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
