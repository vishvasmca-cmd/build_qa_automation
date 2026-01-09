Feature: E-commerce Smoke Tests

  @smoke
  Scenario: User Login and Product Sorting
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be logged in and redirected to the inventory page
    When I sort the products by Name (Z to A)
    Then The products should be sorted in descending order by name

  @smoke
  Scenario: Add item to cart and checkout
    Given I am on the inventory page
    When I add "Test.allTheThings() T-Shirt" to the cart
    And I go to the item details page for "Sauce Labs Onesie"
    And I go back to the inventory page
    And I add "Sauce Labs Bike Light" to the cart
    And I go to the cart
    And I proceed to checkout
    When I fill in my information with first name "Jane", last name "Doe", and postal code "12345"
    And I finish the checkout process
    Then I should see the order confirmation
    When I go back to the home page
    And I log out
    Then I should be redirected to the login page
