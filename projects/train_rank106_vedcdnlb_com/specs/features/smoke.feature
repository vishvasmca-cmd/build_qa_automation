Feature: Website Launch and Element Identification
  As a user,
  I want to launch the website and identify key elements,
  So that I can verify the basic structure of the website.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.example.com"
    Then I should see at least 1 link
    And I should see at least 0 buttons
