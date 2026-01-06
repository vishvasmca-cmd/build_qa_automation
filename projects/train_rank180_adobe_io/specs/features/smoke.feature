Feature: Adobe I/O Website Smoke Tests

  @smoke
  Scenario: Launch website and verify key elements
    Given User navigates to the Adobe I/O website
    Then The website should load successfully
    And Verify the presence of at least 5 buttons
    And Verify the presence of at least 2 links
    And Verify the presence of the menu bar
