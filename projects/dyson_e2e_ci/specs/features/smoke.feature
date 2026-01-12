Feature: Product Search and Checkout Initiation
  As a user
  I want to search for a product and initiate the checkout process
  So that I can purchase the product

  @smoke
  Scenario: Search for Dyson V15 Detect and initiate checkout
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then the cart drawer should open
    When I click on the "Checkout" button
    Then I should be redirected to the checkout page
