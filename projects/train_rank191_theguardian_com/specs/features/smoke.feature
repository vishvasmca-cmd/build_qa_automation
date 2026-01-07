Feature: Website Launch
  As a user
  I want to access the theguardian.com website
  So that I can verify it loads successfully

  @smoke
  Scenario: Launch theguardian.com
    Given I navigate to "https://theguardian.com"
    Then the page should load successfully
