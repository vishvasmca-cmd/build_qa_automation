Feature: Microsoft Cloud Website - Basic Functionality
  As a user,
  I want to verify the basic functionality of the Microsoft Cloud website,
  So that I can ensure the core features are working as expected.

  @smoke
  Scenario: Load the Microsoft Cloud website and identify buttons and links
    Given I navigate to the Microsoft Cloud website
    Then I should be able to identify at least 5 buttons on the page
    And I should be able to identify at least 2 links on the page
