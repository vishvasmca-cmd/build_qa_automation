Feature: InMobi Website - UI Element Identification
  As a user,
  I want to verify the presence of key UI elements on the InMobi website
  So that I can ensure the website's basic structure is intact.

  @smoke
  Scenario: Identify and verify the presence of buttons, links, and menu bars
    Given I navigate to the InMobi website
    Then I should see the "ACCEPT ALL" button
    And I should see the "Learn More" link
    And I should see the "Glance Now" button
    And I should see the "Our Consumer Brands" link
    And I should see the "Consumer Brands" menu bar
    And I should see the "Advertising Platforms" menu bar
