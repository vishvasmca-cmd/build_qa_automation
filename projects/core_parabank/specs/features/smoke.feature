Feature: ParaBank - Basic Navigation and UI Verification
  As a user,
  I want to verify the basic functionalities of the ParaBank application
  So that I can ensure the core features are working as expected.

  @smoke
  Scenario: Verify Login Page and Navigate to About Us
    Given I am on the ParaBank home page
    Then I should see the login form
    When I click on the "About Us" link
    Then I should be redirected to the "About Us" page

  @smoke
  Scenario: Navigate back to Home page from About Us page
    Given I am on the "About Us" page
    When I click on the "Home" link
    Then I should be redirected to the ParaBank home page

  @smoke
  Scenario: Verify Account History link navigates to a valid page
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be redirected to the Account History page or a relevant page
