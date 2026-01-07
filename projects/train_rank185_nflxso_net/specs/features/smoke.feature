Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to the website and identify key elements
  So that I can verify the basic functionality of the website.

  @smoke
  Scenario: Launch Website Successfully
    Given I navigate to "https://nflxso.net"
    Then the page should load successfully

  @smoke
  Scenario: Identify Key Elements on the Page
    Given I am on the "https://nflxso.net" page
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
