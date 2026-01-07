Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Browse Products and Search
    Given User navigates to the Products page
    When User searches for "Dress"
    Then Products related to "Dress" should be displayed

  @smoke
  Scenario: Add a product to the cart
    Given User is on the Products page
    When User adds a product to the cart
    Then The product should be added to the cart successfully

  @smoke
  Scenario: Initiate checkout process
    Given User has items in the cart
    When User proceeds to checkout
    Then User should be redirected to the checkout page
