Feature: E-commerce Smoke Tests

  Scenario: Search for a product and add it to the cart
    Given User is on the home page
    When User navigates to the Products page
    And User searches for "Dress"
    And User adds the first product to the cart
    And User continues shopping
    And User navigates to the cart page
    Then User proceeds to checkout
    And User should be on the checkout page

