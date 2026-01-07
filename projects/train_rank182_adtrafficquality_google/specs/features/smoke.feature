Feature: Website Launch and Element Presence
  As a user,
  I want to verify the basic functionality of the adtrafficquality.google website
  So that I can ensure the website is accessible and key elements are present.

  @smoke
  Scenario: Launch website and verify presence of key elements
    Given I navigate to "https://adtrafficquality.google"
    Then I should see key buttons like "Login", "Signup", "GetStarted", "Try for Free" present
    And I should see key links present
    And I should see menu bars present
