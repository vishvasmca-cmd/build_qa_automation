Feature: User Registration
  As a new user
  I want to register on the ParaBank website
  So that I can access banking services

  Scenario: Successful Registration with Valid Data
    Given I am on the ParaBank registration page
    When I enter 'John' into the First Name field
    And I enter 'Doe' into the Last Name field
    And I enter '123 Main Street' into the Address field
    And I enter 'New York' into the City field
    And I enter 'NY' into the State field
    And I enter '10001' into the Zip Code field
    And I enter '555-1234' into the Phone Number field
    And I enter '123-45-6789' into the SSN field
    And I enter 'user_123' into the Username field
    And I enter 'password' into the Password field
    And I enter 'password' into the Confirm Password field
    When I click the Register button
    Then I should see a success message indicating that my account has been created

  Scenario: Attempt Registration with Invalid Data
    Given I am on the ParaBank registration page
    When I click the Register button without filling any required fields
    Then I should see error messages for all required fields

  Scenario: Attempt Registration with weak password
    Given I am on the ParaBank registration page
    When I enter 'John' into the First Name field
    And I enter 'Doe' into the Last Name field
    And I enter '123 Main Street' into the Address field
    And I enter 'New York' into the City field
    And I enter 'NY' into the State field
    And I enter '10001' into the Zip Code field
    And I enter '555-1234' into the Phone Number field
    And I enter '123-45-6789' into the SSN field
    And I enter 'user_123' into the Username field
    And I enter 'weak' into the Password field
    And I enter 'weak' into the Confirm Password field
    When I click the Register button
    Then I should see error messages for weak password
