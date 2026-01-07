Feature: Product Catalog Smoke Tests

  @smoke
  Scenario: Navigate to the website
    Given I navigate to the Magento website
    Then I should see the Magento website

  @smoke
  Scenario: Handle SSL certificate error
    Given I navigate to the Magento website
    Then I should see an SSL certificate error message
