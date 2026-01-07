Feature: LinkedIn Homepage - Element Presence
  As a user
  I want to see key elements on the LinkedIn homepage
  So that I can start using the platform

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the LinkedIn homepage
    Then I should see the "Join now" button
    And I should see the "Sign in" button
    And I should see the "Continue with Google" button
    And I should see the "Sign in with email" button
    And I should see the "Show more" button
    And I should see the "Skip to main content" link
    And I should see the "LinkedIn" link
