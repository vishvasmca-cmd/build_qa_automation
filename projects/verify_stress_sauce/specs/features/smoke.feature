Feature: E-commerce Smoke Tests

  @smoke
  Scenario: User Login, Sort Products, Add to Cart, Checkout
    Given User is on the login page
    When User logs in with username "standard_user" and password "secret_sauce"
    Then User should be redirected to the inventory page
    When User sorts products by "Name (Z to A)"
    Then Products should be sorted in descending order by name
    When User adds "Test.allTheThings() T-Shirt" to the cart
    And User navigates to item details of "Sauce Labs Onesie"
    And User goes back to the inventory page
    And User adds "Sauce Labs Bike Light" to the cart
    When User navigates to the cart
    Then User should see the added items in the cart
    When User proceeds to checkout
    And User fills in personal information with first name "Jane", last name "Doe", and postal code "12345"
    And User finishes the checkout process
    Then User should be redirected back to the home page
    When User logs out
    Then User should be redirected to the login page
