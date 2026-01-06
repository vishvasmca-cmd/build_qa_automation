Feature: Basic Website Elements
  As a user
  I want to verify the presence of basic website elements
  So that I can ensure the website is functional

  @smoke
  Scenario: Verify website navigates to Google.com and identifies links
    Given I navigate to "https://www.google.com"
    Then I should see the "About" link
    And I should see the "Store" link
    And I should see the "Settings" text
