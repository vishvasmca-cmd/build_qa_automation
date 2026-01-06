Feature: GitHub Homepage - UI Elements Verification
  As a user,
  I want to verify the presence of key UI elements on the GitHub homepage
  So that I can ensure the basic functionality of the website is working.

  @smoke
  Scenario: Verify presence of buttons and links on the homepage
    Given I am on the GitHub homepage
    Then I should see the "Platform" button
    And I should see the "Solutions" button
    And I should see the "Resources" button
    And I should see the "Open Source" button
    And I should see the "Enterprise" button
    And I should see the "Homepage" link
    And I should see the "Pricing" link