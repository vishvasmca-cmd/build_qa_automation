Feature: Website Functionality
  As a user
  I want to verify basic website functionality
  So that I can ensure the website is working correctly

  @smoke
  Scenario: Load Website and Identify Links
    Given I navigate to "https://www.google.com"
    Then I should be able to identify links on the page
