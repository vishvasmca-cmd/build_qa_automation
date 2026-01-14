Feature: Search Functionality
  As a user
  I want to be able to search for products
  So that I can find the products I am interested in

  @smoke
  Scenario: Search for 'Dyson V15 Detect' and verify 'Add to Cart' button
    Given I am on the Dyson India homepage
    When I click on the search icon
    Then I should be able to search for "Dyson V15 Detect"
    And I should see the 'Add to Cart' button
