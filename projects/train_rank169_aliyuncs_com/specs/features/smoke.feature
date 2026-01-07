Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to the aliyuncs.com website
  And identify key elements on the page
  So that I can verify the basic functionality of the website

  @smoke
  Scenario: Navigate to the website and identify elements
    Given I navigate to "https://aliyuncs.com/"
    Then I should be able to see the website
    And I should be able to find 5 buttons
    And I should be able to find 2 links
    And I should be able to find 2 menu bars
