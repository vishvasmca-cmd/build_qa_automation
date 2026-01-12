Feature: Product Search and Checkout Flow
  As a user
  I want to be able to search for a product and initiate the checkout process
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and initiate checkout
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click the search button
    Then I should be able to see the search results
