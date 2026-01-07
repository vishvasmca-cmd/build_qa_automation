Feature: CNN Website - Smoke Tests

  Scenario: Launch CNN Website and Identify Key Elements
    @smoke
    Given User navigates to the CNN homepage
    Then User should be able to see the CNN homepage
    And User should be able to identify multiple buttons and links
    And User should be able to identify the menu bar
