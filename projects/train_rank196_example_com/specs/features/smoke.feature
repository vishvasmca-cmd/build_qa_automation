Feature: Home Page Elements Verification
  As a user,
  I want to verify the presence of key elements on the home page
  So that I can ensure the basic structure of the website is intact.

  @smoke
  Scenario: Verify website launch and presence of elements
    Given I navigate to "https://example.com"
    Then I should see the website launch successfully
    And I should be able to find at least 1 link

  @smoke
  Scenario: Verify website launch and presence of elements on google.com
    Given I navigate to "https://www.google.com"
    Then I should see the website launch successfully
    And I should be able to find at least 1 link
