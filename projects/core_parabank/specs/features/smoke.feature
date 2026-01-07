Feature: Verify Parabank Home Page and Navigation
  As a user
  I want to verify the Parabank home page and navigate to the About Us page
  So that I can ensure the basic functionality of the website is working

  @smoke
  Scenario: Verify the login page elements are present and navigate to the About Us page
    Given I am on the Parabank home page
    Then I should see the login form
    When I click on the "About Us" link
    Then I should be on the "About Us" page
