Feature: Search and Verify Add to Cart Button
  As a user
  I want to search for a product and verify the 'Add to Cart' button
  So that I can ensure the product is available for purchase

  @smoke
  Scenario: Search for Dyson V15 Detect and verify 'Add to Cart' button
    Given I am on the Dyson India homepage
    When I search for "Dyson V15 Detect"
    Then I should see the 'Add to Cart' button
