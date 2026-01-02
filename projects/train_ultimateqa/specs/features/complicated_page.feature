Feature: Interact with elements on the Complicated Page

  Scenario: Navigate to Complicated Page and fill in the first login form
    Given I am on the Automation Practice page
    When I click the Big page with many elements link
    Then I should be on the Complicated Page
    When I enter 'standard_user' into the first username field
    And I enter 'secret_sauce' into the first password field

