Feature: ParaBank Smoke Tests

  Scenario: Verify navigation to Account History
    Given I am on the ParaBank home page
    When I click on "Account History"
    Then I should be on the ParaBank Web Service Definition page

  Scenario: Verify navigation to About Us page
    Given I am on the ParaBank home page
    When I navigate to "/index.htm"
    Then I should see a 404 error page
