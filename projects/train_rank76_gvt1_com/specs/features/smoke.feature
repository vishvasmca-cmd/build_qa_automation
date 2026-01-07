Feature: Website Launch and Element Identification
  As a user,
  I want to verify the website launches successfully
  And I can identify basic elements like buttons and links

  @smoke
  Scenario: Launch Website and Identify Elements
    Given I navigate to "https://www.google.com"
    Then I should be able to identify elements on the page
