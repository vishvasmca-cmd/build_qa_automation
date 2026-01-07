Feature: YouTube Website - Basic Element Verification
  As a user,
  I want to verify the presence of key elements on the YouTube homepage
  So that I can ensure the website is loading correctly and the basic navigation is available.

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I am on the YouTube homepage
    Then I should see the "Guide" button
    And I should see the "Skip navigation" button
    And I should see the "Search" button
    And I should see the "Settings" button
    And I should see the "Sign in" button
    And I should see the "YouTube Home" link
    And I should see the "Sign in" link in the menu
