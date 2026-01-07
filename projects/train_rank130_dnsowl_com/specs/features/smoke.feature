Feature: Home Page Elements Verification
  As a user
  I want to verify the presence of key elements on the home page
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Launch Website and Verify Elements
    Given I navigate to the "https://dnsowl.com" website
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
