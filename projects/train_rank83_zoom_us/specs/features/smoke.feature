Feature: Zoom Website - Homepage Elements
  As a user
  I want to ensure key elements are present on the Zoom homepage
  So that I can easily navigate and use the website

  @smoke
  Scenario: Verify presence of key buttons and links on the homepage
    Given I am on the Zoom homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
