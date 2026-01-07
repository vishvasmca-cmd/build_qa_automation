Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to the website and identify key elements
  So that I can verify the basic structure of the website

  @smoke
  Scenario: Navigate to the website
    Given I navigate to "https://bunny.net/"
    Then the page should load successfully

  @smoke
  Scenario: Identify elements on the homepage
    Given I am on the "HomePage"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
