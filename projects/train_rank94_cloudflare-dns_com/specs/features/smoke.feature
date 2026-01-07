Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Launch website and identify buttons and links
    Given I navigate to "https://one.one.one.one/dns/"
    Then I should be able to find the "iPhone" button
    And I should be able to find at least 5 buttons
    And I should be able to find at least 2 links
