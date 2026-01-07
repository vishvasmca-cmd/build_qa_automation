Feature: GitHub Website - Element Identification
  As a user,
  I want to verify the presence of key elements on the GitHub website
  So that I can ensure the basic functionality is working

  @smoke
  Scenario: Identify buttons and links on the homepage
    Given I am on the GitHub homepage
    Then I should see the "Platform" button
    And I should see the "About" link
    And I should see the "Sign in" link
