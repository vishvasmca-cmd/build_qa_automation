Feature: Identify UI Elements on ax-msedge.net
  As a tester
  I want to verify the presence of key UI elements on the ax-msedge.net website
  So that I can ensure the basic functionality is working

  @smoke
  Scenario: Verify the presence of buttons, links, and menu bars
    Given I navigate to "https://ax-msedge.net"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
