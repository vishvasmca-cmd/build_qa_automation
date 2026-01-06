Feature: Basic JavaScript Interaction
  As a user
  I want to navigate to the Basic JavaScript page
  So that I can interact with the JavaScript alerts

  @smoke
  Scenario: Navigate to Basic JavaScript page
    Given I am on the test pages home page
    When I click the "JavaScript33" link
    Then I should be on the "JavaScript33" page
    And I navigate to the basic javascript alerts page
    Then I am redirected back to the home page due to 404 error
