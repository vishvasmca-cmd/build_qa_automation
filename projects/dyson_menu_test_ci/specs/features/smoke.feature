Feature: Main Menu Navigation
  As a user
  I want to navigate the main menu
  So that I can access different sections of the Dyson website

  @smoke
  Scenario: Verify main menu links
    Given I am on the Dyson India homepage
    When I close the popup if it appears
    And I click on the 'Deals' link
    Then I should be able to access the Deals page
    When I go back to the Dyson India homepage
    And I click on the 'Vacuum & wet cleaners' link
    Then I should be able to access the Vacuum & wet cleaners page
    When I go back to the Dyson India homepage
    And I click on the 'Hair care' link
    Then I should be able to access the Hair care page
    When I go back to the Dyson India homepage
    And I click on the 'Air purifier' link
    Then I should be able to access the Air purifier page
    When I go back to the Dyson India homepage
    And I click on the 'Headphones' link
    Then I should be able to access the Headphones page
    When I go back to the Dyson India homepage
    And I click on the 'Lighting' link
    Then I should be able to access the Lighting page
    When I go back to the Dyson India homepage
    And I click on the 'Support' link
    Then I should be able to access the Support page