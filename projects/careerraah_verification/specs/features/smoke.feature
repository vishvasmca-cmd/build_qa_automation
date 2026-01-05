Feature: CareerRaah Website Smoke Tests

  @smoke
  Scenario: Navigate to Homepage and Verify Heading
    Given User navigates to the CareerRaah homepage
    Then The main heading should be visible

  @smoke
  Scenario: Navigate to Homepage and click on Career Counseling or Explore Programs
    Given User is on the CareerRaah homepage
    When User clicks on 'Career Counseling' or 'Explore Programs'
    Then The user should be navigated to the corresponding page
