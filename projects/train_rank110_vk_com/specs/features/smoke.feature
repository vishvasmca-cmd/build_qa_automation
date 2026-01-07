Feature: VK.com Homepage - Smoke Tests

  Scenario: Verify key elements on the homepage
    Given User navigates to the VK.com homepage
    Then User should see the 'Create business page' button
    And User should see the 'Other sign-in options' button
    And User should see the 'Sign up' button
    And User should see the 'Очистить' button
    And User should see the 'Help' link
    And User should see the 'Learn more' link
