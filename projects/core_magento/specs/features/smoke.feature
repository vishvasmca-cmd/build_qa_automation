Feature: Website Accessibility
  As a user,
  I want to access the website,
  So that I can browse products.

  @smoke
  Scenario: Verify website is accessible
    Given I navigate to the website "https://magento.softwaretestingboard.com/"
    Then the website should be accessible
