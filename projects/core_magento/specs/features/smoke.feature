Feature: Product Search and Details
  As a user
  I want to search for a product, filter the results, and view the product details
  So that I can find the product I am looking for

  @smoke
  Scenario: Search for a product and view details
    Given I am on the homepage
    When I search for "Watch"
    Then I should see search results for "Watch"
    When I filter the search results by category
    Then I should see the filtered search results
    When I click on a product
    Then I should be able to view the product details
