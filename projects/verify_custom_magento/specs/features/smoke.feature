Feature: Website Availability
  As a user
  I want to be able to access the website
  So that I can browse products and make purchases

  @smoke
  Scenario: Verify website homepage loads successfully
    Given I navigate to the website "https://magento.softwaretestingboard.com/"
    Then I should see the website homepage loaded successfully
