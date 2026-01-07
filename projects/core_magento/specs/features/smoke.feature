<<<<<<< Updated upstream
Feature: E-commerce Smoke Tests

  Scenario: Navigate to the Home Page
    Given User navigates to the home page
    Then The home page should load successfully

  @smoke
  Scenario: Search for a product
    Given User is on the home page
    When User searches for "Watch"
    Then Search results page should be displayed
=======
Feature: Product Search and Details
  As a user
  I want to search for products and view their details
  So that I can find and purchase the items I need

  @smoke
  Scenario: Search for a product
    Given I am on the home page
    When I search for "Watch"
    Then I should see search results for "Watch"

  @smoke
  Scenario: Filter products by category
    Given I have searched for "Watch"
    When I filter the results by "Category"
    Then I should see only watches in the selected category

  @smoke
  Scenario: View product details
    Given I have searched for "Watch" and see a list of watches
    When I select a watch from the search results
    Then I should see the details of the selected watch
>>>>>>> Stashed changes
