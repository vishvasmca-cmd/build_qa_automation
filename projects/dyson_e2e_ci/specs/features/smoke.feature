Feature: Product Search and Add to Cart
  As a user
  I want to search for a product and add it to the cart
  So that I can purchase it

  @smoke
  Scenario: Search for Dyson V15 Detect and Add to Cart
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    Then I should see the search results
    When I click on the first product result
    Then I should see the product details page
    And the "Add to Cart" button should be visible
    When I click on the "Add to Cart" button
    Then the cart drawer should open
    And I click on "Checkout"
    Then I should be redirected to the checkout page
