Feature: WordPress.org - Smoke Tests

  As a user,
  I want to verify the presence of key elements on the WordPress.org website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Launch website and identify key elements
    Given I navigate to the WordPress.org homepage
    Then I should be able to identify the 'Get WordPress' link
    And I should be able to identify at least 4 other buttons or links on the page
    And I should be able to identify at least 2 menu bars on the page
