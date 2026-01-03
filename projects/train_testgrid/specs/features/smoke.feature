Feature: TestGrid Smoke Tests
  As a user
  I want to verify the core functionality of the TestGrid application
  So that I can ensure the application is working as expected

  @smoke
  Scenario: Verify application availability and homepage elements
    Given I navigate to the TestGrid homepage
    Then the application should load successfully
    And the homepage should be displayed correctly

  @smoke
  Scenario: Verify 'Start for free' link redirects to the signup page
    Given I am on the TestGrid homepage
    When I click on the 'Start for free' link
    Then I should be redirected to the signup page
    And the URL should contain '/signup'

  @smoke
  Scenario: Fill out sign up form and navigate to the home page
    Given I am on the Sign Up page
    When I fill in the signup form with valid details
      | full_name | business_email    |
      | John Doe  | test@example.com |
    And I click the logo to navigate back to the home page
    Then I should be redirected to the homepage
