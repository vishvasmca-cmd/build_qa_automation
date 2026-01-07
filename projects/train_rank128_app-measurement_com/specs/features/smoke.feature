Feature: Basic Website Functionality
  As a user,
  I want to verify the basic functionality of the website,
  So that I can ensure the website is accessible and key elements are present.

  @smoke
  Scenario: Verify website navigation and element identification
    Given I navigate to the website "https://app-measurement.com/"
    Then I should see the website is loaded successfully
    And I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
