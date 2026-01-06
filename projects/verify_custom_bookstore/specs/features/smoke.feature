Feature: Book Search
  As a user
  I want to search for books
  So that I can find books of interest

  @smoke
  Scenario: Search for a book by title
    Given I am on the Book Store page
    When I search for "Git Pocket Guide"
    Then I should see search results