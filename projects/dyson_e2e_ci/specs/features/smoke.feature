Feature: Product Search and Checkout
  As a user
  I want to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for Dyson V15 Detect and initiate checkout
    Given I am on the Dyson India homepage
    When I handle the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click "Add to Cart"
    Then the cart drawer should open
    When I click "Checkout"
    Then I should be on the checkout page
