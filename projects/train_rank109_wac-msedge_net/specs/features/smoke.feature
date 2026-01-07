Feature: Website Element Identification
  As a tester,
  I want to verify the presence of key elements on the website,
  So that I can ensure the basic structure is in place.

  @smoke
  Scenario: Verify website accessibility
    Given I navigate to "https://wac-msedge.net"
    Then the website should load successfully
