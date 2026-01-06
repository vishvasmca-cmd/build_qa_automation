Feature: Dropbox Homepage UI Elements
  As a user
  I want to see the basic UI elements on the Dropbox homepage
  So that I can navigate and use the website

  @smoke
  Scenario: Verify the presence of key UI elements
    Given I am on the Dropbox homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars