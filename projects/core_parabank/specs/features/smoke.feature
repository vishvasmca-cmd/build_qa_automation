Feature: ParaBank - Basic Navigation
  As a user,
  I want to navigate the ParaBank website,
  So that I can access different sections of the application.

  @smoke
  Scenario: Navigate to About Us page
    Given I am on the ParaBank home page
    When I click on the "About Us" link
    Then I should be on the "About Us" page

  @smoke
  Scenario: Navigate to Home page from About Us page
    Given I am on the ParaBank About Us page
    When I click on the "Home" link
    Then I should be on the ParaBank home page

  @smoke
  Scenario: Verify Account History Link
    Given I am on the ParaBank home page
    Then I should see the "Account History" link
