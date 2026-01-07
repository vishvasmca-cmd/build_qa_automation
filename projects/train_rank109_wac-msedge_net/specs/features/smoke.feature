Feature: Identify UI Elements on Website
  As a tester
  I want to verify the presence of specific UI elements on a website
  So that I can ensure the website's basic structure is correct

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.example.com"
    Then I should be able to identify 5 buttons
    And I should be able to identify 2 links
    And I should be able to identify 2 menu bars
