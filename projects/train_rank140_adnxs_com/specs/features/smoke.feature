Feature: Website Element Identification
  As a user
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Launch website and verify basic elements
    Given I navigate to "https://adnxs.com/"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
