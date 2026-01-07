Feature: Website Accessibility and Basic Element Presence
  As a user,
  I want to access the DigiCert website
  So that I can verify its basic functionality.

  @smoke
  Scenario: Verify website loads successfully
    Given the user navigates to the DigiCert website
    Then the website should load successfully

  @smoke
  Scenario: Verify presence of key interactive elements
    Given the user is on the DigiCert website
    Then the page should contain at least 5 buttons
    And the page should contain at least 2 links

  @smoke
  Scenario: Verify presence of menu bar
    Given the user is on the DigiCert website
    Then the page should contain a menu bar
