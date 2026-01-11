Feature: Main Menu Navigation
  As a user
  I want to navigate the main menu
  So that I can access different sections of the website

  @smoke
  Scenario: Navigate through main menu links
    Given I am on the Dyson India homepage
    When I handle the popup if it appears
    And I click on each link in the main menu:
      | Deals                |
      | Vacuum & wet cleaners |
      | Hair care              |
      | Air purifier           |
      | Headphones             |
      | Lighting               |
      | Support                |
    Then I should be able to access each page successfully
