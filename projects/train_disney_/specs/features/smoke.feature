Feature: Disney+ Smoke Tests
  As a user,
  I want to verify the core functionalities of Disney+.

  @smoke
  Scenario: Verify Disney+ homepage loads successfully and navigate to sign-up flow
    Given I navigate to the Disney+ homepage
    Then I should see the Disney+ homepage
    When I click on the 'View Plan Options' button
    Then I should be redirected to a page related to sign-up options
