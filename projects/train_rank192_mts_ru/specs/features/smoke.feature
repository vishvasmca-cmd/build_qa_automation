Feature: MTS.ru Website - Homepage Verification
  As a user
  I want to verify the basic elements of the MTS.ru homepage
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify website launch and basic elements presence
    Given I navigate to "https://mts.ru"
    Then I should see the MTS.ru homepage
    And I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
