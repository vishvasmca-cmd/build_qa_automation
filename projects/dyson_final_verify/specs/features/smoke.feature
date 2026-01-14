Feature: Product Search and Add to Cart Verification
  As a user
  I want to search for a specific product
  So that I can verify its availability

  @smoke
  Scenario: Search for Dyson V15 Detect and verify 'Add to Cart' button
    Given I am on the Dyson India homepage
    When I handle the popup if it exists
    And I search for "Dyson V15 Detect"
    Then I should see the 'Add to Cart' button on the product page
