Feature: Nginx Website - Basic UI Elements
  As a user
  I want to verify the presence of key UI elements on the Nginx website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of links
    Given I am on the Nginx homepage
    Then I should see the "Code" link

  @smoke
  Scenario: Verify presence of links after scroll
    Given I am on the Nginx homepage
    When I scroll down
    Then I should see the "Code" link
