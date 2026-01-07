Feature: Akamai Website Element Identification
  As a QA Engineer
  I want to verify the presence of key elements on the Akamai website
  So that I can ensure the website's basic structure is intact

  @smoke
  Scenario: Verify presence of buttons, links, and menu bars
    Given I navigate to "https://www.akamai.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
