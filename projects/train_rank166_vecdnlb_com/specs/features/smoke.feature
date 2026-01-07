Feature: Website Structure Verification
  As a user,
  I want to verify the basic structure of the website,
  So that I can ensure core elements are present.

  @smoke
  Scenario: Verify website loads and essential elements are present
    Given I navigate to "https://vecdnlb.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
