Feature: Homepage UI Elements Verification
  As a user
  I want to verify the presence of key UI elements on the homepage
  So that I can ensure the basic functionality of the website

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the tumblr.com homepage
    Then I should see the "Sign up" button
    And I should see the "Log in" button
    And I should see the "Change palette" button
    And I should see the "Home" link
    And I should see the "Explore" link