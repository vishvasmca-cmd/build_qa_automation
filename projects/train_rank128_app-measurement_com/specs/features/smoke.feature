Feature: Basic Website Elements Verification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the basic functionality is available

  @smoke
  Scenario: Verify presence of links on Google homepage
    Given I navigate to "https://www.google.com/"
    Then I should see the "About" link
    And I should see the "Store" link
    And I should see the "Gmail" link
