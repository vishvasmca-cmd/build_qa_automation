Feature: Vungle Website - UI Element Identification
  As a tester
  I want to verify the presence of key UI elements on the Vungle website
  So that I can ensure the basic functionality is available

  @smoke
  Scenario: Launch website and identify buttons and links
    Given I navigate to the Vungle website "https://vungle.com"
    Then I should see the "Log In" button
    And I should be able to scroll the page

