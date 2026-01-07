Feature: Product Search
  As a user
  I want to be able to search for products
  So that I can find the products I am interested in

  @smoke
  Scenario: Search for a product and view its details
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results containing "Watch"
    And I should be able to view the details of a product