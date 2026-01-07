Feature: Website Element Identification
  As a user,
  I want to verify the presence of key UI elements on the website
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Launch website and identify UI elements
    Given I navigate to "https://registrar-servers.com"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
