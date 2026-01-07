Feature: Home Page - Smoke Tests
  As a user,
  I want to verify the presence of key elements on the Vimeo home page
  So that I can ensure the website is loading correctly and key functionalities are accessible.

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I am on the Vimeo home page
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
