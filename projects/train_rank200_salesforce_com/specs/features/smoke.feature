Feature: Google Homepage UI Elements Verification
  As a user
  I want to verify the presence of key UI elements on the Google homepage
  So that I can ensure the basic page structure is loaded correctly

  @smoke
  Scenario: Verify Google Homepage Loads and Displays UI Elements
    Given I navigate to "https://www.google.com"
    Then I should see at least 2 links
    And I should see at least 5 buttons
