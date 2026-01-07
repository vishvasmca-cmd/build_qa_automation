Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to the MIIT website and identify key elements,
  So that I can verify the basic structure of the website.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://miit.gov.cn"
    Then I should be able to identify at least 5 buttons, 2 links, and 2 menu bars without clicking them
