Feature: Website Element Identification
  As a user,
  I want to verify the presence of specific elements on a website
  So that I can ensure the website structure is as expected.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.google.com"
    Then I should be able to find a link named "About"
