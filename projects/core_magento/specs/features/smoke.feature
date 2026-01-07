Feature: Product Catalog Smoke Tests

  @smoke
  Scenario: Search for a product
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results

  @smoke
  Scenario: View product details
    Given I am on the home page
    When I search for "Watch"
    And I click on a product
    Then I should see the product details page
