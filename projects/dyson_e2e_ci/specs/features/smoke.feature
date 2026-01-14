Feature: Dyson India - Smoke Tests

  @smoke
  Scenario: Search for a product and verify PDP
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    Then I should see the "Add to Cart" button on the product page
