Feature: Pinterest Homepage - Smoke Tests
  As a user,
  I want to verify the presence of key elements on the Pinterest homepage
  So that I can ensure the basic functionality is working.

  @smoke
  Scenario: Verify presence of 'Log in' and 'Sign up' buttons
    Given I am on the Pinterest homepage
    Then I should see the 'Log in' button
    And I should see the 'Sign up' button

  @smoke
  Scenario: Verify presence of 'Explore', 'Shop', and 'About' links
    Given I am on the Pinterest homepage
    Then I should see the 'Explore' link
    And I should see the 'Shop' link
    And I should see the 'About' link