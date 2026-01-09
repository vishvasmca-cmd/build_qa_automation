Feature: Web Inputs Form
  As a user
  I want to be able to navigate to the web inputs page and fill the form
  So that I can test the input functionalities

  @smoke
  Scenario: Fill the web inputs form with valid data
    Given I navigate to the ExpandTesting practice website
    When I click on the "Web inputs" link
    And I fill the "Input: Number" field with "123"
    And I fill the "Input: Text" field with "test text"
    And I fill the "Input: Password" field with "password123"
    Then I should be able to see the filled values
