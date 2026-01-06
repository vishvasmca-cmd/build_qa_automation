Feature: Website Functionality
  As a user
  I want to ensure the website functions correctly
  So that I can access its features

  @smoke
  Scenario: Verify website loads successfully
    Given I navigate to "https://www.example.com"
    Then the page should load successfully

  @smoke
  Scenario: Verify the presence of at least one link
    Given I am on "https://www.example.com"
    Then I should see at least 1 link
