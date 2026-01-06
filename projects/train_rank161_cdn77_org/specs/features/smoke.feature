Feature: CDN77 Website - Element Identification
  As a user,
  I want to verify the presence of key elements on the CDN77 website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of buttons and links on CDN77 website
    Given I navigate to "https://cdn77.org"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
