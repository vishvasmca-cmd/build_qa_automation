Feature: UI Element Identification
  As a user
  I want to verify the presence of specific UI elements on a webpage
  So that I can ensure the application's basic structure is correct

  @smoke
  Scenario: Load Google Homepage and Identify Elements
    Given I navigate to "https://www.google.com"
    Then I should see the "Sign in" button
    And I should see the "Store" link
    And I should see the "Gmail" link
