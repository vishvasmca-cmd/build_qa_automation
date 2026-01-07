Feature: Akamai Website - Element Verification
  As a user,
  I want to verify the presence of key elements on the Akamai website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website loads successfully
    Given I navigate to "https://www.akamai.com"
    Then the page should load successfully

  @smoke
  Scenario: Verify the presence of buttons, links, and menu bars
    Given I am on the Akamai homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
