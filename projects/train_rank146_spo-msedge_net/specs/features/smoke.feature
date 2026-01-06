Feature: Website Element Verification
  As a user
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify website loads and key elements are present
    Given I navigate to "https://spo-msedge.net"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
