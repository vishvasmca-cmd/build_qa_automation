Feature: Main Menu Navigation
  As a user
  I want to navigate through the main menu
  So that I can access different sections of the Dyson website

  @smoke
  Scenario: Verify main menu links navigate to correct pages
    Given I am on the Dyson India homepage
    When I click on each link in the main menu
      | Deals                  |
      | Vacuum & wet cleaners |
      | Hair care                |
      | Air purifier             |
      | Headphones             |
      | Lighting               |
      | Support                |
    Then I should be navigated to the corresponding page
