Feature: Product Search and View
  As a user
  I want to search for a product and view its details
  So that I can find the product I am looking for

  @smoke
  Scenario: Search for a product and view details
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results
    And I should be able to view the details of a product