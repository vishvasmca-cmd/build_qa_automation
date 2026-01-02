Feature: Interact with the Complicated Page
  As a user, I want to interact with the complicated page by filling forms.

  Scenario: Fill the first login form with valid credentials
    Given I am on the "Complicated Page"
    When I fill the first username field with "standard_user"
    And I fill the first password field with "secret_sauce"

  Scenario: Fill the second login form with valid credentials
    Given I am on the "Complicated Page"
    When I fill the second username field with "standard_user"
    And I fill the second password field with "secret_sauce"

  Scenario: Fill the first contact form with valid details
    Given I am on the "Complicated Page"
    When I fill the name field in the first contact form with "John Doe"
    And I fill the email field in the first contact form with "john.doe@example.com"
    #And I fill the captcha field in the first contact form with a valid answer
