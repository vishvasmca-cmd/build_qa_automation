Feature: Website Accessibility
  As a user
  I want to access the website
  So that I can verify its basic functionality

  @smoke
  Scenario: Access the website
    Given I navigate to "https://st.okcdn.ru/"
    Then the page should load successfully

  @smoke
  Scenario: Verify website is accessible
    Given I navigate to "https://st.okcdn.ru/"
    Then the website should be accessible
