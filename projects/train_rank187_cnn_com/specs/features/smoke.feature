Feature: CNN Website - Basic UI Element Identification
  As a user,
  I want to verify the presence of key UI elements on the CNN website
  So that I can ensure the website is loading correctly and the basic structure is in place.

  @smoke
  Scenario: Launch CNN website and verify basic elements
    Given I navigate to "https://www.cnn.com/"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
