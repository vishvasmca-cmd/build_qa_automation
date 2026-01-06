Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of buttons and links on the Google homepage
    Given I navigate to "https://www.google.com"
    Then I should be able to identify buttons and links on the page
