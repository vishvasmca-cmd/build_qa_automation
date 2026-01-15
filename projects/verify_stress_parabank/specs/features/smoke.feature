Feature: ParaBank Website Exploration
  As a user
  I want to explore the ParaBank website
  So that I can understand its functionality

  @smoke
  Scenario: Navigate to Site Map and Back to Home
    Given I am on the ParaBank home page
    When I click on the "Site Map" link
    Then I should be on the Site Map page
    When I click on the "Log Out" link
    Then I should be redirected to the home page

  @smoke
  Scenario: Navigate to Customer Lookup Page
    Given I am on the ParaBank home page
    When I click on the "Forgot login info?" link
    Then I should be on the Customer Lookup page
    When I click on the "Site Map" link
    Then I should be on the Site Map page
