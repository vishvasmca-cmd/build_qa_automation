Feature: GoDaddy Website - Element Presence
  As a user,
  I want to verify the presence of key elements on the GoDaddy website
  So that I can ensure the basic structure and navigation are available.

  @smoke
  Scenario: Verify presence of key elements on the homepage
    Given I navigate to the GoDaddy homepage
    Then I should see a "Login" button
    And I should see a "Sign Up" or "Get Started" button
    And I should see a "Try for Free" button
    And I should see at least 2 other buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
