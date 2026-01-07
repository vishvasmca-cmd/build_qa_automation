Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of key elements on the website
    Given I navigate to "https://macromedia.com"
    Then I should see a "Login" button or link
    And I should see a "Signup" or "Get Started" button or link
    And I should see a "Try for Free" button or link
    And I should see 2 other buttons
    And I should see 2 links
    And I should see 2 menu bars
