Feature: Telegram Website - Homepage Elements
  As a user,
  I want to verify the presence of key elements on the Telegram homepage
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify presence of links on the homepage
    Given I am on the Telegram homepage
    Then I should see the "Instant View" link
    And I should see the "English" link

  @smoke
  Scenario: Verify the presence of menu bars on the homepage
    Given I am on the Telegram homepage
    Then I should see at least 2 menu bars
