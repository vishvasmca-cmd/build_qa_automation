Feature: Intuit Website - UI Element Verification
  As a user,
  I want to verify the presence of key UI elements on the Intuit website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website launch and presence of buttons and links
    Given I navigate to the Intuit website "https://intuit.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
