Feature: Website Element Identification
  As a user
  I want to be able to identify key elements on the website
  So that I can interact with the website effectively

  @smoke
  Scenario: Identify buttons, links, and menu bars on the homepage
    Given I navigate to "https://apple-dns.net"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
