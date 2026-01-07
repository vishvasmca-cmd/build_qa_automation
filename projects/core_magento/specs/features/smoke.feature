Feature: Website Accessibility
  As a user
  I want to access the Magento website
  So that I can browse products and make purchases

  @smoke
  Scenario: Verify website accessibility
    Given I navigate to the Magento website
    Then the website should be accessible
    And an SSL error should not be present
