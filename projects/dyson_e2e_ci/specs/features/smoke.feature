Feature: Smoke Tests - Dyson E-commerce

  @smoke
  Scenario: Search and Add to Cart
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click the "Add to Cart" button
    Then the cart drawer should open
    And I click "Checkout"
    Then I should be on the Checkout page
