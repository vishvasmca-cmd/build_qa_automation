Feature: RCN Smoke Tests

  @smoke @login
  Scenario: User Login and Logout
    Given User navigates to the login page "https://my.astound.com/login"
    Then User should be able to see the login page

  @smoke
  Scenario: Check successful login with valid credentials
  Given User is logged in with username "vishvas.mca@gmail.com" and password "Myaccount@123"
  Then User should be able to see the billing information

  @smoke
  Scenario: User is able to enable SMS notification
  Given User is logged in
  Then User should be able to enable SMS notifications
  And User should be able to logout
