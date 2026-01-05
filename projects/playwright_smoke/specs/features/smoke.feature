Feature: Playwright Documentation Smoke Tests

  @smoke
  Scenario: Navigate to 'Get Started' page
    Given the user navigates to the Playwright homepage
    When the user clicks on the 'Get Started' link
    Then the user should be redirected to the 'Get Started' documentation page
