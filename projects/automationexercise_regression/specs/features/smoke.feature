Feature: Smoke Tests - Automation Exercise

  As a user,
  I want to perform smoke tests on the Automation Exercise website
  To ensure core functionalities are working as expected.

  @smoke
  Scenario: Verify Homepage Loads Successfully and Navigate to Products Page
    Given I am on the Automation Exercise homepage
    When I click the 'Products' link
    Then I should be on the Products page

  @smoke
  Scenario: Add product to cart from Products page
    Given I am on the Products page
    When I click the 'Add to cart' button for a product
    Then The product should be added to cart without errors

  @smoke
  Scenario: Add two products to cart from Products page
    Given I am on the Products page
    When I click the 'Add to cart' button for a product
    And I click the 'Add to cart' button for another product
    Then Both products should be added to cart without errors
