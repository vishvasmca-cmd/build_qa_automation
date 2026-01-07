Feature: Ad Traffic Quality - Element Discovery
  As a user,
  I want to verify the presence of key elements on the Ad Traffic Quality website
  So that I can ensure the basic structure and navigation are available.

  @smoke
  Scenario: Verify presence of links
    Given I am on the Ad Traffic Quality website
    Then I should see the "Overview" link
    And I should see the "Skip to content" link
