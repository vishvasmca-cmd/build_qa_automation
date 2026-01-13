Feature: Dyson E-commerce Smoke Tests

  Scenario: Search, Add to Cart, and Checkout
    @smoke
    Given I am on the Dyson India homepage
    When I handle the 'Subscribe' popup
    And I search for 'Dyson V15 Detect'
    And I click on the first product result
    Then I should see the 'Add to Cart' button
    When I click the 'Add to Cart' button
    Then the cart drawer should open
    And I click 'Checkout'
    Then I should be on the Checkout page
