Feature: Website Element Identification
  As a user
  I want to verify the presence of key elements on the fastly.net website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify website loads and key elements are present
    Given I navigate to "https://www.fastly.com/"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
