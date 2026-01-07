Feature: Homepage Element Verification
  As a user,
  I want to ensure that key elements are present on the WordPress.com homepage,
  So that I can easily navigate and interact with the site.

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the "https://wordpress.com/" homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
