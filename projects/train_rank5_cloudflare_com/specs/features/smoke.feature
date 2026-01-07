Feature: Website UI Verification
  As a user,
  I want to verify the presence of key UI elements on the Cloudflare website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website launch and key UI elements
    Given I navigate to "https://cloudflare.com"
    Then I should see the 'Log in' button
    And I should see the 'Start for free' button
    And I should see the 'See pricing' button
    And I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
