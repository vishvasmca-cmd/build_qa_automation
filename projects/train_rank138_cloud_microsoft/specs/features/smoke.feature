Feature: Microsoft Cloud Homepage - Element Verification
  As a user,
  I want to verify the presence of key buttons and links on the Microsoft Cloud homepage
  So that I can ensure the basic functionality is available.

  @smoke
  Scenario: Verify presence of key buttons and links
    Given I navigate to the Microsoft Cloud homepage
    Then I should see the "Sign in" button
    And I should see the "Get Microsoft 365" button
    And I should see the "More" button
    And I should see the "All Microsoft" button
    And I should see a fifth button
    And I should see the "Skip to main content" link
    And I should see the "Microsoft 365 Copilot" link
