Feature: Product Search and Details
  As a user
  I want to search for products and view their details
  So that I can find and purchase the products I need

  @smoke
  Scenario: Search for a product and view details
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results for "Watch"
    And I click on the first product in the search results
    Then I should be able to view the product details
