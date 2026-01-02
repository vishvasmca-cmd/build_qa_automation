Feature: Complicated Page Login
  As a user
  I want to log in to the Complicated Page
  So that I can access secure content

  Scenario: Login with valid credentials using the first login form
    Given I am on the Complicated Page
    When I enter 'standard_user' into the first username field
    And I enter 'secret_sauce' into the first password field

  Scenario: Login with valid credentials using the second login form
    Given I am on the Complicated Page
    When I enter 'standard_user' into the second username field
    And I enter 'secret_sauce' into the second password field

  Scenario: Attempt to fill multiple username fields
    Given I am on the Complicated Page
    When I repeatedly enter 'standard_user' into the first username field
    Then the first username field should contain 'standard_user'

  Scenario: Attempt to fill password field multiple times
    Given I am on the Complicated Page
    When I repeatedly enter 'secret_sauce' into the first password field
    Then the first password field should contain 'secret_sauce'
