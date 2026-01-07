Feature: ParaBank Smoke Tests

  Scenario: Verify ParaBank Home Page Loads Successfully @smoke
    Given I navigate to the ParaBank home page
    Then I should see the ParaBank logo
    And I should see the "Register" link
    And I should see the "Forgot login info" link

  Scenario: Attempt to navigate to Account History and return to home page @smoke
    Given I am on the ParaBank home page
    When I click on the 'Account History' link
    Then I should be navigated back to the ParaBank home page
