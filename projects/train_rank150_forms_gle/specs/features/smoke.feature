Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to a website and identify key elements,
  So that I can verify the basic structure and functionality of the page.

  @smoke
  Scenario: Navigate to Google and Identify Links
    Given I navigate to "https://www.google.com/"
    Then I should be able to identify at least 2 links on the page
