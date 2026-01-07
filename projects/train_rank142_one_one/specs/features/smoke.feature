Feature: Landing Page Elements
  As a user
  I want to verify the presence of key elements on the landing page
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify website loads and key elements are present
    Given I navigate to "https://www.one.com/"
    Then I should see at least 5 links
    And I should see at least 0 buttons
