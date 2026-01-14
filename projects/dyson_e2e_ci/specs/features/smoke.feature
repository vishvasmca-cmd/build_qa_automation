Feature: Product Search and PDP Verification
  As a user
  I want to search for a product and verify its details
  So that I can find and purchase the desired product

  @smoke
  Scenario: Search for 'Dyson V15 Detect' and verify PDP
    Given I am on the Dyson India homepage
    When I search for 'Dyson V15 Detect'
    And I click on the first product result
    Then I should see the 'Add to Cart' button on the PDP
