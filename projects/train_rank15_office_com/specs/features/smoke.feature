Feature: Office.com Smoke Tests
  As a user,
  I want to verify the basic functionality of the office.com website
  So that I can ensure the website is working as expected.

  @smoke
  Scenario: Launch website and identify key elements
    Given I navigate to "https://office.com"
    Then I should see the "Products" button
    And I should see the "Microsoft Power Platform Business" link
