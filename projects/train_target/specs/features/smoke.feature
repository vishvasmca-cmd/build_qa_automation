Feature: Target Homepage Smoke Test
  As a user,
  I want to verify the basic functionality of the Target homepage
  So that I can ensure the website is working as expected.

  @smoke
  Scenario: Verify Homepage Hero Section and Navigation
    Given I navigate to the Target homepage
    Then I should see the hero headline containing 'Expect more. Pay less.'
    When I click the 'Shop Now' button
    Then I should be navigated to a relevant shopping page
