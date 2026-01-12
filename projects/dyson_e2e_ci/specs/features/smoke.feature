Feature: Product Purchase Flow
  As a customer
  I want to be able to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the desired product

  @smoke
  Scenario: Purchase Dyson V15 Detect
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then the cart drawer should open
    And I click on the "Checkout" button
    Then I should be redirected to the checkout page
