Feature: Netlify Smoke Tests
  As a user
  I want to verify the core functionality of the Netlify website
  So that I can ensure the application is working as expected

  @smoke
  Scenario: Verify homepage and navigate to sign-up
    Given I navigate to the Netlify homepage
    Then I should see the Netlify homepage
    When I click the 'Get started' button
    Then I should be redirected to the sign-up area
    And I should see elements related to the sign-up form
