Feature: Form Filling
  As a user
  I want to be able to fill out forms on the Letcode website
  So that I can submit information

  @smoke
  Scenario: Fill the first name field
    Given I navigate to the Letcode forms page
    When I fill the "firstname" field with "Test Name"
    Then the "firstname" field should contain "Test Name"