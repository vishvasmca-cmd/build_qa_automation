Feature: Homepage Elements Verification
  As a user,
  I want to verify the presence of key elements on the Snapchat homepage
  So that I can ensure the basic functionality of the website

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I am on the Snapchat homepage
    Then I should see the "Log in" button
    And I should see the "Sign Up" button
    And I should see the "Community Geofilter Terms" link
    And I should see the "Report Infringement" link
