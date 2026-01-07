Feature: Homepage Element Identification
  As a user,
  I want to verify the presence of key elements on the homepage,
  So that I can ensure the basic structure of the website is intact.

  @smoke
  Scenario: Verify homepage loads successfully
    Given I navigate to the "https://app-analytics-services.com/"
    Then the page should load successfully

  @smoke
  Scenario: Identify elements on the homepage
    Given I am on the "HomePage"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
