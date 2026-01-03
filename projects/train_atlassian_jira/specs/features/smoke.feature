Feature: Jira Smoke Tests
  As a user,
  I want to ensure the core functionalities of Jira are working
  So that I can use the application with confidence.

  @smoke
  Scenario: Verify Jira Homepage Loads Successfully and Hero Headline
    Given I navigate to the Jira homepage
    Then the page should load successfully
    And the hero headline should contain 'Plan, track, and release great software'

  @smoke
  Scenario: Verify 'Try it Free' Button Navigation
    Given I am on the Jira homepage
    When I click the 'Try it Free' button
    Then I should be redirected to a page related to Jira free trial signup