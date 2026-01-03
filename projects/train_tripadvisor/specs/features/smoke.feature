Feature: TripAdvisor Smoke Tests
  As a user
  I want to ensure the TripAdvisor application is functioning correctly
  So that I can plan my trips effectively

  @smoke
  Scenario: Verify Homepage Load and Basic Navigation
    Given I navigate to the TripAdvisor homepage
    Then I should see the hero headline containing 'Know better. Book better. Go better.'
    And I should see the 'Start Planning' button
    When I click the 'Start Planning' button
    Then I should be redirected to a page where I can start planning

  @smoke
  Scenario: Basic Search Functionality
    Given I am on the TripAdvisor homepage
    When I search for "hotels in Paris"
    Then I should see search results related to "hotels in Paris"

  @smoke
  Scenario: User Login
    Given I am on the TripAdvisor login page
    When I enter valid credentials for a standard user
    And I click the login button
    Then I should be logged in successfully

  @smoke
  Scenario: Verify API Health (Search)
    Given I make a GET request to the search API for "restaurants in Rome"
    Then the API response status code should be 200

  @smoke
  Scenario: Check Application Version
    Given I navigate to the 'About' page
    Then I should see the application version information