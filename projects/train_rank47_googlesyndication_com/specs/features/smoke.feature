Feature: Landing Page Element Verification
  As a user,
  I want to verify the presence of key UI elements on the landing page,
  So that I can ensure the basic structure of the website is intact.

  @smoke
  Scenario: Verify the presence of buttons and links
    Given I am on the "https://googlesyndication.com" website
    Then I should see at least 5 buttons
    And I should see at least 2 links
