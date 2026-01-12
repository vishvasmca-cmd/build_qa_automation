Feature: Menu Bar Navigation
  As a user
  I want to navigate the Anthropic website using the menu bar
  So that I can access different sections of the website

  @smoke
  Scenario: Navigate to Meet Claude page
    Given I am on the Anthropic homepage
    When I click on the "Claude" menu item
    Then I should be navigated to the Claude page

  @smoke
  Scenario: Navigate to Platform page
    Given I am on the Anthropic homepage
    When I click on the "products" menu item
    Then I should be navigated to the Platform page

  @smoke
  Scenario: Navigate to Solutions page
    Given I am on the Anthropic homepage
    When I click on the "products" menu item
    Then I should be navigated to the Solutions page