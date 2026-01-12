Feature: Product Search and Cart Verification
  As a user
  I want to search for a product, add it to the cart, and verify it is in the cart
  So that I can purchase the product

  @smoke
  Scenario: Search for 'Blue Cotton' and add the first result to the cart
    Given I am on the products page
    When I search for 'Blue Cotton'
    And I click on 'View Product' for the first result
    And I click on 'Add to cart'
    And I click on 'View Cart'
    Then I should see the 'Blue Cotton' product in the cart
