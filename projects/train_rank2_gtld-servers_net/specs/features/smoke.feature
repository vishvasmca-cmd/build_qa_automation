Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to a website and identify key elements
  So that I can verify the basic functionality of the website

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.google.com"
    Then I should be able to see the "About" link
    And I should be able to see the "Store" link
    And I should be able to see the "Sign in" button
