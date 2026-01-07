Feature: ParaBank - Smoke Tests
  As a user, I want to verify core functionalities of the ParaBank application.

  @smoke
  Scenario: Verify navigation to Account History page fails and redirects to WSDL page
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be redirected to the ParaBank WSDL page

  @smoke
  Scenario: Verify navigation back to the ParaBank home page from the WSDL page
    Given I am on the ParaBank WSDL page
    When I navigate back to the ParaBank home page
    Then I should be on the ParaBank home page
