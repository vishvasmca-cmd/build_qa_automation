Feature: Homepage Elements Verification
  As a user,
  I want to verify the presence of key elements on the akam.net homepage
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website navigation and presence of buttons, links, and menu bars
    Given I navigate to "https://akam.net"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
