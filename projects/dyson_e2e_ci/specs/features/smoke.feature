Feature: E-commerce Smoke Test
  As a user
  I want to perform basic e-commerce functions
  So that I can verify the core functionality of the Dyson website

  @smoke
  Scenario: Search, Add to Cart, and Navigate to Checkout
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click the search button
    Then I should see the search results
    When I click on the first product result
    Then I should see the "Add to Cart" button on the product page
    When I click the "Add to Cart" button
    Then the cart drawer should open
    When I click the "Checkout" button in the cart drawer
    Then I should be navigated to the checkout page
