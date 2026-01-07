Feature: Website Accessibility and Element Identification
  As a user,
  I want to ensure the website is accessible and key elements are present,
  So that I can start using the website.

  @smoke
  Scenario: Verify website accessibility
    Given I navigate to "https://steamserver.net"
    Then the page should load successfully

  @smoke
  Scenario: Verify the presence of key elements
    Given I am on the "HomePage"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
