Feature: Vacuum Cleaners Page Scroll
  As a user
  I want to be able to scroll to the bottom of the vacuum cleaners page
  So that I can view all available products

  @smoke
  Scenario: Scroll to the bottom of the page
    Given I navigate to the Dyson vacuum cleaners page
    When I scroll to the bottom of the page
    Then I should be able to see the footer
