Feature: Basic Website Element Identification
  As a tester,
  I want to verify the basic elements of a website can be identified,
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "google.com"
    Then I should see the page