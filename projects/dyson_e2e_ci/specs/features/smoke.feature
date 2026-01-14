Feature: Dyson E2E Smoke Test

  @smoke
  Scenario: Search for a product and add it to the cart
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then I should see the cart drawer opens
    And I click on the "Checkout" button
    Then I should be on the checkout page
