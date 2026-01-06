Feature: Autocomplete and Alert Handling
  As a user
  I want to type a country, select it from the autocomplete, and handle the alert
  So that I can verify the functionality works as expected

  @smoke
  Scenario: Type country, select option, and handle alert
    Given I am on the Automation Practice page
    When I type "India" in the autocomplete input
    And I select "India" from the autocomplete options
    And I click the "Practice" button
    Then an alert is displayed
