Feature: NIST Website Smoke Tests
  As a user
  I want to verify the basic functionality of the NIST website
  So that I can ensure the site is operational

  @smoke
  Scenario: Verify the presence of key elements on the homepage
    Given I am on the NIST homepage
    Then I should see the "Back to top" button
    And I should see the "What We Do" button
    And I should see the "Vote.gov" link
