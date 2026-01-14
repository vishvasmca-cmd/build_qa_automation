Feature: Search and Verify Add to Cart
  As a user
  I want to search for a product
  So that I can verify the 'Add to Cart' button is present

  @smoke
  Scenario: Search for 'Dyson V15 Detect' and verify 'Add to Cart' button
    Given I am on the Dyson India homepage
    When I click the search icon
    And I close the popup if it appears
    And I fill the search input with 'Dyson V15 Detect'
    And I click the search button
    Then I should see the 'Add to Cart' button
