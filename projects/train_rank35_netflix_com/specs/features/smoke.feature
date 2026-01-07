Feature: Netflix Homepage - Element Identification
  As a user
  I want to verify the presence of key elements on the Netflix homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of 'Get Started' button and page scrolling
    Given I am on the Netflix homepage
    Then I should see the 'Get Started' button
    And I can scroll down the page
