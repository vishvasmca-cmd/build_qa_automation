Feature: Product Catalog - Smoke Tests
  As a user
  I want to be able to search for products and view their details
  So that I can find and purchase the items I need

  @smoke
  Scenario: Search for a product
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results for "Watch"

  @smoke
  Scenario: View product details
    Given I am on the search results page for "Watch"
    When I click on a product
    Then I should be able to view the product details