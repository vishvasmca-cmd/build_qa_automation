Feature: Salesforce Website Accessibility
  As a user
  I want to access the Salesforce website
  So that I can verify its basic functionality

  @smoke
  Scenario: Verify website is accessible
    Given I navigate to "https://www.salesforce.com/"
    Then the page should load successfully
