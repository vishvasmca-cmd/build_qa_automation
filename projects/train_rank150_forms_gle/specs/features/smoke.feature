Feature: Google Forms UI Element Identification
  As a tester
  I want to verify the presence of specific UI elements on the Google Forms website and Google Search page
  So that I can ensure the basic functionality of the website

  @smoke
  Scenario: Verify presence of links on Google Search page
    Given I navigate to "https://www.google.com"
    Then I should see the "About" link

  @smoke
  Scenario: Verify presence of Settings text on Google Search page
    Given I navigate to "https://www.google.com"
    Then I should see the "Settings" text
