Feature: Product Catalog - Smoke Tests

  @smoke
  Scenario: Search for a product
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results for "Watch"
