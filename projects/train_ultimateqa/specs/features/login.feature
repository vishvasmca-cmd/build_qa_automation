Feature: Backoffice Login and Account Unlock
  As a user,
  I want to be able to log in to the backoffice
  So that I can access the dashboard.

  Scenario: Successful Login
    Given I am on the backoffice login page
    When I enter 'standard_user' into the username field
    And I enter 'secret_sauce' into the password field
    And I click the login button
    Then I should be logged in and redirected to the dashboard

  Scenario: Account is locked - Unlock account
    Given I am on the Access Denied page
    When I click the Unlock Me button
    And I enter 'standard_user' into the username or email field
    Then I click the Unlock Me button

  Scenario: Account is locked - Try Again
    Given I am on the Access Denied page
    When I click the Try again link
    Then I should be redirected to the Login page
