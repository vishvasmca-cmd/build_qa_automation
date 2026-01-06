Feature: Account Registration
  As a user
  I want to access the registration page
  So that I can create an account

  @smoke
  Scenario: Navigate to My Account and attempt to access the registration page
    Given I am on the website homepage
    When I click on 'My Account'
    Then I should be on the 'My Account' page
    And I attempt to navigate to the registration page
    Then I should be on the 'My Account' page

