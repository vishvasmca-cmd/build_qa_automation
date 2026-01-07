Feature: Basic Website Navigation and Element Identification
  As a user,
  I want to navigate to the website and identify key elements,
  So that I can verify the website is accessible and key elements are present.

  @smoke
  Scenario: Launch Website and Find Key Elements
    Given I navigate to "https://azurewebsites.net"
    Then I should see the website is loaded successfully
    And I should be able to find 5 buttons
    And I should be able to find 2 links
    And I should be able to find 2 menu bars
