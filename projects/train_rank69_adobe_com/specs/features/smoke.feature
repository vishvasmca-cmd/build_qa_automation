Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the Adobe website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://adobe.com"
    Then I should be able to see "5" buttons
    And I should be able to see "2" links
    And I should be able to see "2" menu bars
