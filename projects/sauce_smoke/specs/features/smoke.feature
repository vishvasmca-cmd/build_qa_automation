Feature: Homepage Accessibility
  As a user
  I want to access the homepage
  So that I can browse available products

  @smoke
  Scenario: Verify homepage is reachable
    Given I navigate to the saucedemo homepage
    Then I should be able to access the homepage
