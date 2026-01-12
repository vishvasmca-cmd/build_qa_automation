Feature: Anthropic Menu Navigation
  As a user
  I want to navigate the main menu
  So that I can access different sections of the Anthropic website

  @smoke
  Scenario: Navigate to Meet Claude
    Given I am on the Anthropic homepage
    When I click on the "Claude" link
    Then I should be navigated to the Claude page

  @smoke
  Scenario: Navigate to Platform
    Given I am on the Anthropic homepage
    When I click on the "products" link
    Then I should be navigated to the Platform page

  @smoke
  Scenario: Navigate to Solutions
    Given I am on the Anthropic homepage
    When I click on the "products" link
    Then I should be navigated to the Solutions page