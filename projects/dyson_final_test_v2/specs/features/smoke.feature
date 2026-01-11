Feature: Dyson Website - Smoke Tests
  As a user,
  I want to navigate the Dyson website
  So that I can access different product categories and support information.

  @smoke
  Scenario: Verify main menu navigation and page load
    Given I am on the Dyson India homepage
    When I handle the initial popup
    And I navigate through the main menu items
      | Deals                 |
      | Vacuum & wet cleaners |
      | Hair care             |
      | Air purifier          |
      | Headphones            |
      | Lighting              |
      | Support               |
    Then each page should load successfully
