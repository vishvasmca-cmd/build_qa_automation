Feature: GitHub Website - Smoke Tests
  As a user
  I want to verify the presence of key elements on the GitHub website
  So that I can ensure the basic functionality is working

  @smoke
  Scenario: Verify presence of Sign In link
    Given I am on the GitHub homepage
    Then I should see the "Sign in" link

  @smoke
  Scenario: Verify presence of other key elements
    Given I am on the GitHub homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
