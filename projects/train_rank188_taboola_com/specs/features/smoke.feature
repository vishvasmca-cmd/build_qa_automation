Feature: Taboola Website - Smoke Tests

  Scenario: Verify presence of key elements on the homepage
    Given User navigates to the Taboola homepage
    Then User should see the 'Engagement' button
    And User should see the 'Performance Marketing Platforms' link
    And User should see the 'Login' link
    And User should see the 'Create Account' button
    And User should see the 'Get Started' button
    And User should see the 'Leads' button
    And User should see the 'Purchases' button
    And User should see the 'Measurable Outcomes' button
