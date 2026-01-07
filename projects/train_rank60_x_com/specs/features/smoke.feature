Feature: X.com UI Element Verification
  As a user,
  I want to verify the presence of key UI elements on the X.com website
  So that I can ensure the basic functionality is available.

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the X.com homepage
    Then I should see the "Sign up with Apple" button
    And I should see the "About" link
