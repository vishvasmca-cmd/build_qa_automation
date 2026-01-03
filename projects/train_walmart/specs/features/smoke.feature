Feature: Homepage Navigation
  As a user
  I want to navigate the Walmart homepage
  So that I can verify critical elements and navigation are functional

  @smoke
  Scenario: Verify Homepage Hero Headline and Shop Now Button
    Given I am on the Walmart homepage
    Then I should see the hero headline containing "Save money. Live better."
    When I click the "Shop Now" button
    Then I should be navigated to a relevant page
