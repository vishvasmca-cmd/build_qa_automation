Feature: Nginx Website - Homepage UI Elements
  As a user
  I want to verify the presence of key UI elements on the Nginx homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the Nginx homepage "https://nginx.com"
    Then I should see the "FREE TRIALS" button
    And I should find at least 4 other buttons
    And I should find at least 2 links
