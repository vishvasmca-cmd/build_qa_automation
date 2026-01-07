Feature: Product Search and Details
  As a user
  I want to search for a product and view its details
  So that I can find and learn about products I'm interested in

  @smoke @skip
  Scenario: Search for a product and view details
    Given I am on the home page
    When I search for "Watch"
    And I filter by category
    Then I should see product details
