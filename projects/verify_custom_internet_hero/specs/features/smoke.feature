Feature: Form Authentication
  As a user
  I want to be able to log in with valid credentials
  So that I can access the secure area

  @smoke
  Scenario: Successful Login
    Given I navigate to the Form Authentication page
    When I enter username "tomsmith"
    And I enter password "SuperSecretPassword!"
    Then I should be logged in successfully
