Feature: Website Accessibility
  As a user
  I want to access the website
  So that I can start using the application

  @smoke
  Scenario: Verify website is accessible
    Given I navigate to the website "https://magento.softwaretestingboard.com/"
    Then I should see an SSL certificate error message
    And the website should not be accessible