Feature: Adobe Website UI Element Identification
  As a user,
  I want to verify the presence of key UI elements on the Adobe website
  So that I can ensure the website is loading correctly and the basic structure is in place.

  @smoke
  Scenario: Verify Adobe website loads and key UI elements are present
    Given I navigate to "https://adobe.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
