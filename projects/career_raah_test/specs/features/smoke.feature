Feature: Career Raah - Smoke Test

  @smoke
  Scenario: Check Login Button Existence
    Given I navigate to the Career Raah homepage
    Then I should see a "Login" button