Feature: E-commerce Smoke Tests

<<<<<<< Updated upstream
  As a user
  I want to perform basic actions on the e-commerce site
  So that I can verify core functionalities are working

  @smoke
  Scenario: Successful Login and Sort Products
    Given I am on the login page
    When I enter username "standard_user" and password "secret_sauce"
    And I click the login button
    Then I should be logged in and redirected to the inventory page
    When I sort the products by price "Price (low to high)"
    Then the products should be sorted by price from low to high
=======
  Scenario: Successful Login and Product Sorting
    @smoke
    Given I am on the Saucedemo login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be logged in and redirected to the inventory page
    When I sort the products by price from low to high
    Then The products should be sorted by price low to high

  Scenario: Add item to cart
    @smoke
    Given I am on the Saucedemo inventory page
    When I add the first item to the cart
    Then The item should be added to the cart
>>>>>>> Stashed changes
