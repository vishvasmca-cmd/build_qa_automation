Feature: Application Navigation
  As a user
  I want to be able to access the banking application
  So that I can use its features

  @smoke
  Scenario: Navigate to the Home Page
    Given I navigate to the ParaBank home page
    Then the page should load successfully
