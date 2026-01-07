Feature: Spotify Homepage - Element Identification
  As a user,
  I want to verify the presence of key elements on the Spotify homepage
  So that I can ensure the basic functionality is available.

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I am on the Spotify homepage
    Then I should see the "Log in" button
    And I should see the "Sign up" button
    And I should see the "Premium" button
    And I should see the "Support" button
    And I should see the "Download" button
    And I should see the "Install App" link
    And I should see the "Browse podcasts" link
    And I should see the "Home" button
    And I should see the "Search" button
