Feature: Instagram Homepage - Element Verification
  As a user,
  I want to see key elements on the Instagram homepage,
  So that I can easily navigate and use the platform.

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I am on the Instagram homepage
    Then I should see the "Log in" button
    And I should see the "Log in with Facebook" button
    And I should see the "Sign up" button
    And I should see the "Forgot password?" link
    And I should see the "Meta" link
