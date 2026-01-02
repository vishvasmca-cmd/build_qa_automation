Feature: Interact with the Complicated Page and Handle Login
  As a user
  I want to navigate to the Complicated Page and interact with its elements
  So that I can test form filling and login scenarios

  Scenario: Navigate to Complicated Page and Fill Forms
    Given I am on the "Complicated Page"
    When I fill the username field in the first login form with "standard_user"
    And I fill the password field in the first login form with "secret_sauce"
    And I fill the name field in the first contact form with "John Doe"
    And I fill the email field in the first contact form with "john.doe@example.com"

  Scenario: Attempt Login and Handle Access Denied
    Given I am on the Login Page
    When I fill the username field with "standard_user"
    And I fill the password field with "secret_sauce"
    And I click the Login button
    Then I should be redirected to the dashboard

  Scenario: Handle Access Denied and Unlock Account
    Given I am on the Access Denied Page
    When I click the Unlock Me button
    And I fill the username or email field with "standard_user"
    And I click the Unlock Me button again

  Scenario: Attempt Login after Access Denied, Try Again.
    Given I am on the Access Denied Page
    When I click the Try again link
    Then I should be redirected to the Login Page
    When I fill the username field with "standard_user"
    And I fill the password field with "secret_sauce"
    And I click the Login button
    Then I should be redirected to the dashboard
