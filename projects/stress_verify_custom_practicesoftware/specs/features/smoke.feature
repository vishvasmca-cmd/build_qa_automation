Feature: My Account and Registration
  As a user
  I want to access the 'My Account' page
  So that I can register for an account

  @smoke
  Scenario: Navigate to My Account page
    Given I am on the home page
    When I click on 'My Account'
    Then I should be navigated to the 'My Account' page
