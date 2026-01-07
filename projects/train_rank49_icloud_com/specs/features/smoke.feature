Feature: iCloud Website - Smoke Tests

  @smoke
  Scenario: Launch website and identify key elements
    Given The user navigates to the iCloud website
    Then The website should load successfully
    And The user should be able to identify the 'Sign In' button
    And The user should be able to identify the 'Help' button
    And The user should be able to identify the 'apple.com/icloud' link
    And The user should be able to identify the 'System Status' link
    And The user should be able to identify the 'Privacy Policy' link
    And The user should be able to identify the 'Terms & Conditions' link
