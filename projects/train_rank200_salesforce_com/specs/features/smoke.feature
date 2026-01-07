Feature: Salesforce.com - Smoke Tests
  As a user,
  I want to verify the presence of key elements on the Salesforce.com website
  So that I can ensure the website is accessible and functional

  @smoke
  Scenario: Verify website accessibility and presence of key elements
    Given I navigate to the Salesforce.com news page
    Then I should be able to access the website
    And I should be able to identify buttons, links, and menu bars
