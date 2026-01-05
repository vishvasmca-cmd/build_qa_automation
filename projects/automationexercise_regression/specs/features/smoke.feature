Feature: Smoke Test - automationexercise_regression

  @smoke
  Scenario: Browse Products and Add to Cart
    Given User navigates to the products page
    When User searches for "polo"
    And User clicks on 'View Product' for a specific product
    And User clicks 'Add to cart'
    And User clicks 'Continue Shopping'
    Then User should be able to view the cart

  @smoke
  Scenario: Navigate to Test Cases Page
    Given User is on the home page
    When User navigates to the 'Test Cases' page
    Then User should be able to view the test cases

  @smoke
  Scenario: Submit Contact Us Form
    Given User navigates to the 'Contact us' page
    When User fills out the contact form with valid details
    Then User should be able to submit the form

  @smoke
  Scenario: Browse Products and Add another product to Cart
    Given User navigates to the products page
    When User clicks on 'View Product' for a specific product
    And User clicks 'Add to cart'
    And User clicks 'Continue Shopping'
    Then User should be able to continue shopping
