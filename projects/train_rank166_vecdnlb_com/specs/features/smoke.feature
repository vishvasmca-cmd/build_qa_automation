Feature: Homepage Element Identification
  As a user,
  I want to be able to identify key elements on the homepage,
  So that I can verify the website's structure.

  @smoke
  Scenario: Identify links on the homepage
    Given I am on the "https://www.google.com" homepage
    Then I should see the "About" link
    And I should see the "Store" link

  @smoke
  Scenario: Identify buttons on the homepage
    Given I am on the "https://www.google.com" homepage
    Then I should see the "Sign in" button
