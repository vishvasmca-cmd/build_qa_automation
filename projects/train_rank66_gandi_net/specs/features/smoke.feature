Feature: Gandi.net Website - Smoke Tests
  As a user,
  I want to access the Gandi.net website
  So that I can verify its basic functionality

  @smoke
  Scenario: Access Gandi.net website and identify key elements
    Given I navigate to the Gandi.net website
    Then I should be able to see the "Create a website" button
