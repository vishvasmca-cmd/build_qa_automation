Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Complete purchase flow
    Given I am on the Magento homepage
    When I search for "Jacket"
    And I click on the first product "Olivia 1/4 Zip Light Jacket"
    And I select size "M"
    And I select color "Purple"
    And I add the product to the cart
    Then I should see a success message
    When I click on the 'Sale' menu link
    And I click on 'Tees' in the left sidebar
    And I click on 'Desiree Fitness Tee'
    And I select size "L"
    And I select color "Black"
    And I add the product to the cart
    When I click on the Cart icon in header
    And I click 'View and Edit Cart'
    And I update 'Desiree Fitness Tee' quantity to 2
    And I click 'Update Shopping Cart'
    Then I verify usage of coupons is available
    When I proceed to checkout
    And I enter email 'test_user_99@example.com'
    And I fill First Name 'Test', Last Name 'User'
    And I fill Street Address '123 Test St'
    And I fill City 'New York'
    And I select State 'New York'
    And I fill Zip '10001'
    And I fill Phone '1234567890'
    And I select Shipping Method 'Table Rate'
    And I click Next
    Then I verify 'Payment Method' step is visible
    When I click Place Order
    Then I verify Order Confirmation number is visible
