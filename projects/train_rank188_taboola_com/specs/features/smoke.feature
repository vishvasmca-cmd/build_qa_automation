Feature: Taboola Website - Homepage Elements
  As a user,
  I want to verify the presence of key elements on the Taboola homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I am on the Taboola homepage
    Then I should see the "Login" link
    And I should see the "Create Account" button or link
    And I should see the "Get Started" button or link
    And I should see the "Engagement" link
    And I should see the "Leads" link
