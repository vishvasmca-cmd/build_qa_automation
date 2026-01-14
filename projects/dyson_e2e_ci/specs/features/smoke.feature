Feature: Dyson E-commerce Smoke Tests

  Scenario: Search, Add to Cart, and Checkout Initiation
    @smoke
    Given I am on the Dyson India homepage
    When I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click the "Add to Cart" button
    Then I should see the cart drawer open
    When I click the "Checkout" button in the cart drawer
    Then I should be on the Checkout page
