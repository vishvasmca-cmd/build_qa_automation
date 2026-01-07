Feature: WordPress.org - Element Identification
  As a user,
  I want to verify the presence of key elements on the WordPress.org homepage
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify the presence of 'Get WordPress' button
    Given I am on the WordPress.org homepage
    Then I should see the 'Get WordPress' button

  @smoke
  Scenario: Verify the presence of News Link
    Given I am on the WordPress.org homepage
    Then I should see the 'News' link
