Feature: Europa.eu Website Smoke Tests
  As a user,
  I want to ensure the basic functionality of the Europa.eu website is working.

  @smoke
  Scenario: Launch Europa.eu website
    Given I navigate to "https://europa.eu"
    Then the page should load successfully

  @smoke
  Scenario: Verify presence of key elements
    Given I am on the "https://europa.eu" page
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
