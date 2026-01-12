Feature: Anthropic Menu Bar - Smoke Tests

  Scenario: Navigate to Meet Claude
    Given I am on the Anthropic homepage
    When I click on the "Claude" menu item
    Then I should be navigated to the Claude page
    And the URL should contain "claude"
    @smoke

  Scenario: Navigate to Platform
    Given I am on the Anthropic homepage
    When I click on the "products" menu item
    Then I should be navigated to the Platform page
    And the URL should contain "products"
    @smoke

  Scenario: Navigate to Solutions
    Given I am on the Anthropic homepage
    When I click on the "products" menu item
    Then I should be navigated to the Solutions page
    And the URL should contain "products"
    @smoke