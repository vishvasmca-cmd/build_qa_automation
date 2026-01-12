Feature: Purchase Flow
  As a user
  I want to purchase a product from the Demoblaze website
  So that I can successfully complete an order

  @smoke
  Scenario: Purchase a laptop
    Given I am on the Demoblaze homepage
    When I click on the 'Laptops' category
    And I click on 'Sony vaio i5'
    And I click 'Add to cart'
    And I accept the alert
    And I go to 'Cart'
    And I click 'Place Order'
    And I fill in the name with "test"
    And I fill in the city with "Test City"
    And I fill in the credit card with "1234567890"
    Then I should be able to see the order confirmation
