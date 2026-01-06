Feature: CNN Website Smoke Tests
  As a user,
  I want to ensure the CNN website is accessible
  So that I can access news and information.

  @smoke
  Scenario: Verify Website Accessibility
    Given I navigate to "https://www.cnn.com/"
    Then the page should load successfully

  @smoke
  Scenario: Verify Presence of Interactive Elements
    Given I am on "https://www.cnn.com/"
    Then I should see interactive elements like buttons, links, and menu bars
