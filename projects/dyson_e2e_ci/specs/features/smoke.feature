Feature: Product Purchase Flow
  As a user
  I want to be able to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Purchase Dyson V15 Detect
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click the search button
    Then I should see the search results page
    #And I click on the first product result
    #Then I should see the product details page
    #And I should see the "Add to Cart" button
    #When I click the "Add to Cart" button
    #Then I should see the cart drawer open
    #When I click the "Checkout" button
    #Then I should be redirected to the checkout page
