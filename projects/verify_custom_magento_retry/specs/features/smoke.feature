Feature: Initial Application Load
  As a user
  I want to access the Magento website
  So that I can verify the site is reachable

  @smoke
  Scenario: Verify initial page load and certificate check
    Given I navigate to the Magento homepage
    Then I should see the "Click to reveal" button
    When I click the "Click to reveal" button
    Then I should be able to access the website content
