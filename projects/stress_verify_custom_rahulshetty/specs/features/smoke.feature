Feature: Autocomplete Functionality
  As a user
  I want to be able to type in a country and select a valid option from the suggestions
  So that I can quickly find the country I am looking for

  @smoke
  Scenario: Autocomplete suggests countries as user types
    Given I am on the Rahul Shetty Academy practice page
    When I type "India" in the "Type to Select Countries" input field
    Then I should see suggestions for countries matching "India"

  @smoke
  Scenario: User can select a country from the suggestions
    Given I am on the Rahul Shetty Academy practice page
    When I type "United States" in the "Type to Select Countries" input field
    Then I should see suggestions for countries matching "United States"
    #And I select "United States of America" from the suggestions
