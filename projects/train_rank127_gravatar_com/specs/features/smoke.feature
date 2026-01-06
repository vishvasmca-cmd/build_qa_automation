Feature: Gravatar Homepage Element Identification
  As a user
  I want to ensure key elements are present on the Gravatar homepage
  So that I can easily navigate and use the site

  @smoke
  Scenario: Verify presence of key buttons on the homepage
    Given I am on the Gravatar homepage
    Then I should see the 'Log in' button
    And I should see the 'Get Started Now' button
    And I should see the 'Claim Your Free Profile' button

  @smoke
  Scenario: Verify presence of key links on the homepage
    Given I am on the Gravatar homepage
    Then I should see the 'Homepage' link
