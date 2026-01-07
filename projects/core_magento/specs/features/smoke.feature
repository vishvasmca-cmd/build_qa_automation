Feature: Product Catalog
  As a user
  I want to be able to search for products and view their details
  So that I can find and purchase the products I need

  @smoke
  Scenario: Search for a product and view details
    Given I am on the home page
    When I search for "Watch"
    And I filter by a category
    Then I should see a list of watches
    And I should be able to view the details of a selected watch
