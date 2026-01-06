Feature: Nginx Website - Basic Element Identification
  As a user,
  I want to verify the presence of key elements on the Nginx website
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Verify presence of links
    Given I am on the Nginx homepage
    Then I should see at least 2 links
