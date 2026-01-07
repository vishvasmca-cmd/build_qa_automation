Feature: Element Identification on Website
  As a tester,
  I want to verify the identification of buttons, links, and menu bars on a website,
  So that I can ensure the basic functionality of the website is working.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.google.com"
    Then I should be able to identify links on the page
    And I should be able to scroll the page
