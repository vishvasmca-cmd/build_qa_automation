Feature: Homepage Elements Verification
  As a user
  I want to verify the presence of key elements on the homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Navigate to the website
    Given I navigate to "https://www.example.com"
    Then the page should load successfully

  @smoke
  Scenario: Identify elements on the homepage
    Given I am on the "https://www.example.com" homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
