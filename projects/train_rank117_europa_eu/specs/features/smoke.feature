Feature: Europa.eu Website - Smoke Tests
  As a user,
  I want to ensure the Europa.eu website loads correctly
  And I can identify buttons and links on the page

  @smoke
  Scenario: Launch Website and Identify Buttons and Links
    Given I navigate to the Europa.eu website
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
