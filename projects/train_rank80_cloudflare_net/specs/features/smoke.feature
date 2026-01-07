Feature: Website Element Identification
  As a user,
  I want to launch the website and identify key elements,
  So that I can verify the basic structure and functionality of the website.

  @smoke
  Scenario: Launch website and attempt to identify elements
    Given I navigate to "https://cloudflare.net"
    Then I should be able to identify the presence of buttons, links, and menu bars
