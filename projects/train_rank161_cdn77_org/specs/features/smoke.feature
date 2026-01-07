Feature: Website Launch and Element Identification
  As a user,
  I want to verify the basic functionality of the website,
  So that I can ensure the core features are working.

  @smoke
  Scenario: Launch website and identify key elements
    Given I navigate to "https://cdn77.org"
    Then I should see the website loaded successfully
    And I should see at least 5 buttons including "Login", "Signup", or "Try for Free"
    And I should see at least 2 links
    And I should see at least 2 menu bars
