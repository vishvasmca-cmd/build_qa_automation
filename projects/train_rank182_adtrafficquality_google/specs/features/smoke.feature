Feature: AdTrafficQuality - Smoke Tests
  As a user,
  I want to verify the presence of key elements on the AdTrafficQuality landing page
  So that I can ensure the basic functionality is working as expected.

  @smoke
  Scenario: Verify presence of links on the landing page
    Given I am on the AdTrafficQuality landing page
    Then I should see at least 2 links

  @smoke
  Scenario: Verify presence of menu bars on the landing page
    Given I am on the AdTrafficQuality landing page
    Then I should see at least 2 menu bars
