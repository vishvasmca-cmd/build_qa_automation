Feature: PayPal Website - Smoke Tests

  Scenario: Verify presence of key links and buttons on the homepage
    @smoke
    Given User navigates to the PayPal homepage
    Then User should see the 'Terms' link
