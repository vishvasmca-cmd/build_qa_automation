Feature: flickr.com - Basic UI Elements
  As a user
  I want to verify the presence of key UI elements
  So that I can ensure the website is functional

  @smoke
  Scenario: Verify presence of Login, Signup, and other key UI elements
    Given I am on the flickr.com homepage
    Then I should see a "Login" button or link
    And I should see a "Signup" or "Get Started" or "Try for Free" button or link
    And I should see at least 3 other buttons or links
    And I should see at least 2 menu bars

