Feature: Google Homepage UI Elements
  As a user
  I want to verify the presence of key UI elements on the Google homepage
  So that I can ensure the basic functionality of the website

  @smoke
  Scenario: Verify presence of 'Sign in' button
    Given I am on the Google homepage
    Then I should see the 'Sign in' button

  @smoke
  Scenario: Verify presence of 'About' link
    Given I am on the Google homepage
    Then I should see the 'About' link

  @smoke
  Scenario: Verify presence of 'Gmail' link
    Given I am on the Google homepage
    Then I should see the 'Gmail' link
