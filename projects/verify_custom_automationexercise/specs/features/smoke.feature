Feature: Product Search
  As a user
  I want to be able to search for products
  So that I can find the items I need

  @smoke
  Scenario: Search for a product
    Given I am on the home page
    When I navigate to the Products page
    And I search for "shirt"
    Then I should see products containing the word "shirt" in the search results
