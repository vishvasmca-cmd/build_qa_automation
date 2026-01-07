Feature: Authentication and Product Sorting
  As a user,
  I want to log in, sort products by price,
  So that I can easily find and purchase products.

  @smoke
  Scenario: Successful login and product sorting
    Given I am on the login page
    When I enter valid credentials
      And I click the login button
    Then I should be logged in successfully
    When I sort products by price "Price (low to high)"
    Then Products should be sorted by price low to high
