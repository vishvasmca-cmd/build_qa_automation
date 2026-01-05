Feature: Playwright Documentation - Smoke Tests
  As a user
  I want to navigate the Playwright documentation website
  So that I can access the documentation

  @smoke
  Scenario: Navigate to Playwright and access documentation
    Given I navigate to the Playwright website
    When I click on the "Get Started" button
    Then I should be redirected to the documentation page
    When I click on the Playwright logo
    Then I should be redirected to the home page
