Feature: Taboola Website - Smoke Tests

  Scenario: Verify key elements on the homepage
    @smoke
    Given User navigates to the Taboola homepage
    Then User should see the 'Get Started' link
    And User should see the 'Login' link
    And User should see the 'Create Account' link
    And User should see the 'Contact Us' link
    And User should see the 'Advertise' link
    And User should see the 'Advertisers' menu item
    And User should see the 'Publishers' menu item
    And User should see the 'Engagement' button
    And User should see the 'Leads' button
    And User should see the 'Purchases' button
    And User should see the 'Measurable Outcomes' button
