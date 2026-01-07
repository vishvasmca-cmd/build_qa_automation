Feature: Apple.com - Element Identification
  As a user
  I want to verify the presence of key elements on the Apple.com website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Launch website and identify buttons and links
    Given I navigate to "https://www.apple.com/"
    Then I should be able to find buttons
    And I should be able to find links
