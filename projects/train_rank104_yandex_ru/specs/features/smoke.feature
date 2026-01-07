Feature: Yandex.ru Homepage - Element Identification
  As a user,
  I want to verify the presence of key UI elements on the Yandex.ru homepage
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Verify the presence of the 'Войти' (Login) button
    Given I am on the Yandex.ru homepage
    Then I should see the 'Войти' button with test id "login-button"

  @smoke
  Scenario: Verify the presence of the 'sport' link
    Given I am on the Yandex.ru homepage
    Then I should see the 'sport' link with test id "tab-news-rubric-4"

  @smoke
  Scenario: Verify the presence of the sidebar more button
    Given I am on the Yandex.ru homepage
    Then I should see the sidebar more button with test id "sidebar-more-button"
