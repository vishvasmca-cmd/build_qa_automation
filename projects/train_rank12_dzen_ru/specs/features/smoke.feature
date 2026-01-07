Feature: Dzen.ru - Smoke Test
  As a user,
  I want to verify the presence of key elements on the Dzen.ru homepage
  So that I can ensure the basic functionality is working.

  @smoke
  Scenario: Verify 'Login' button is present
    Given I am on the Dzen.ru homepage
    Then I should see the 'Login' button

  @smoke
  Scenario: Verify 'Открыть виртуальную клавиатуру' link is present
    Given I am on the Dzen.ru homepage
    Then I should see the 'Открыть виртуальную клавиатуру' link
