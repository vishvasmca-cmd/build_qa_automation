Feature: Yandex.ru Homepage Elements
  As a user
  I want to verify the presence of key elements on the Yandex.ru homepage
  So that I can ensure the basic structure and functionality are working

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the Yandex.ru homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
