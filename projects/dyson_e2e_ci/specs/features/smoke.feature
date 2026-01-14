Feature: Dyson E-commerce Smoke Tests

  @smoke
  Scenario: Search for a product and initiate checkout
    Given I am on the Dyson India homepage
    When I close the initial popups
    And I search for "Dyson V15 Detect"
    Then I should see the search results
    And I click on the first product
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then the cart drawer should open
    When I click on the "Checkout" button
    Then I should be on the checkout page
