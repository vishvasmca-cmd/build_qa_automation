Feature: Product Search and Details
  As a user
  I want to search for products and view their details
  So that I can find and purchase the products I need

  @smoke
  Scenario: Search for a product
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results

  @smoke
  Scenario: View product details
    Given I am on the home page
    When I search for "Watch"
    And I select a product from the search results
    Then I should see the product details page
