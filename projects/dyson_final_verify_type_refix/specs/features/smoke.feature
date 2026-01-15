Feature: Product Search and Add to Cart Verification
  As a user
  I want to search for a specific product
  So that I can verify the 'Add to Cart' button is present

  @smoke
  Scenario: Search for 'Dyson V15 Detect' and verify 'Add to Cart' button
    Given I am on the Dyson India homepage
    When I close the initial popup
    And I click on the search icon
    And I enter "Dyson V15 Detect" in the search input
    And I submit the search query
    And I close the login popup
    And I scroll down to view products
    And I click on a product link
    Then I should see the 'Add to cart' button
