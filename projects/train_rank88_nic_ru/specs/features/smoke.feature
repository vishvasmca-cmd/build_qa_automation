Feature: nic.ru Smoke Tests

  @smoke
  Scenario: Launch website and identify key elements
    Given User navigates to "https://nic.ru"
    Then User should see the website loaded successfully
    Then User should be able to identify at least 5 buttons
    Then User should be able to identify at least 2 links
    Then User should be able to identify at least 2 menu bars
