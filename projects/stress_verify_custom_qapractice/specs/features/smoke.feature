Feature: JavaScript Alerts Interaction
  As a user
  I want to interact with JavaScript alerts
  So that I can verify their functionality

  @smoke
  Scenario: Display and Accept Alert
    Given I am on the Alerts JavaScript page
    When I click the "Show alert box" button
    Then an alert box is displayed

  @smoke
  Scenario: Display Confirm and Accept
    Given I am on the Alerts JavaScript page
    When I click the "Show confirm box" button
    Then a confirm box is displayed
