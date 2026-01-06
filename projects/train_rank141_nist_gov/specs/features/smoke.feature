Feature: NIST Homepage - Element Presence
  As a user
  I want to verify the presence of key elements on the NIST homepage
  So that I can ensure the basic structure and navigation are functional

  @smoke
  Scenario: Verify the presence of buttons and links on the homepage
    Given I navigate to "https://www.nist.gov/"
    Then I should see at least 5 buttons
    And I should see at least 2 links
