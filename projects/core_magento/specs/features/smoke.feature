Feature: Product Search and Details
  As a user
<<<<<<< Updated upstream
  I want to search for a product, filter the results, and view the product details
  So that I can find the product I am looking for
=======
  I want to search for products, filter them, and view their details
  So that I can find the products I'm interested in
>>>>>>> Stashed changes

  @smoke
  Scenario: Search for a product and view details
    Given I am on the home page
    When I search for "Watch"
<<<<<<< Updated upstream
    Then I should see search results for "Watch"
    When I filter the search results by category
    Then I should see filtered search results
    When I select a product from the search results
    Then I should be able to view the product details
=======
    And I filter by category
    Then I should see product details for the selected product
>>>>>>> Stashed changes
