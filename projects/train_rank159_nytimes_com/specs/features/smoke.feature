Feature: NYTimes.com Homepage - Smoke Test

  Scenario: Verify the presence of the Search button
    @smoke
    Given I am on the NYTimes.com homepage
    Then I should see the "Search" button