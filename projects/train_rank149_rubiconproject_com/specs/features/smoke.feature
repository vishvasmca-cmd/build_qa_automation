Feature: Homepage Element Identification
  As a user
  I want to verify the presence of key elements on the homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify the presence of buttons on the homepage
    Given I am on the "https://www.magnite.com/" homepage
    Then I should see at least 5 buttons

  @smoke
  Scenario: Verify the presence of links on the homepage
    Given I am on the "https://www.magnite.com/" homepage
    Then I should see at least 2 links

  @smoke
  Scenario: Verify the presence of menu bars on the homepage
    Given I am on the "https://www.magnite.com/" homepage
    Then I should see at least 2 menu bars
