Feature: Katalon Website Smoke Tests
  As a user,
  I want to verify the core functionalities of the Katalon website
  So that I can ensure the website is working as expected.

  @smoke
  Scenario: Navigate to Products menu and verify sub-items
    Given I am on the Katalon homepage
    When I click on the "Products" menu
    Then I should be able to see the sub-items

  @smoke
  Scenario: Validate visible links on the homepage
    Given I am on the Katalon homepage
    Then I should be able to validate all visible links

  @smoke
  Scenario: Navigate to the Contact Us page
    Given I am on the Katalon homepage
    When I navigate to the "Contact Us" page
    Then I should be on the Contact Us page
