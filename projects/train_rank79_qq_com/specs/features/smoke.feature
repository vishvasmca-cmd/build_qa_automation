Feature: QQ.com Homepage Elements
  As a user,
  I want to verify the presence of key elements on the QQ.com homepage
  So that I can ensure the basic functionality of the website is working

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the QQ.com homepage
    Then I should be able to find at least 5 buttons
    And I should be able to find at least 2 links
