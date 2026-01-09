Feature: Product Search
  As a user
  I want to be able to search for products on the website
  So that I can find the products I am interested in

  @smoke
  Scenario: Search for a product
    Given I navigate to the Products page
    When I enter "Dress" in the search input
    And I click the search button
    Then I should see search results displayed
