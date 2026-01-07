Feature: Homepage Element Identification
  As a user
  I want to verify the presence of key elements on the homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify the presence of the 'Log In' button
    Given I am on the homepage "https://liftoff.ai/"
    Then I should see the 'Log In' button
