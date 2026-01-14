Feature: Dyson India - Smoke Tests
  As a user
  I want to perform basic actions on the Dyson India website
  So that I can verify core functionality is working

  @smoke
  Scenario: Search for a product and verify 'Add to Cart' button
    Given I am on the Dyson India homepage
    When I close the initial popup
    And I search for "Dyson V15 Detect"
    Then I should see the 'Add to Cart' button on the product page
