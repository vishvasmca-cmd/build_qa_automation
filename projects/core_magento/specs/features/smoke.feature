Feature: Product Catalog
  As a user
  I want to search for products
  So that I can find the items I need

  @smoke @broken
  Scenario: Search for a product
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results
