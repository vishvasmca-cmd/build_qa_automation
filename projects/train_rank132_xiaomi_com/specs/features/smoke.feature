Feature: Element Identification on Google.com
  As a tester
  I want to verify the identification of buttons and links on Google.com
  So that I can ensure the basic functionality of the website is working

  @smoke
  Scenario: Identify a link on the page
    Given I navigate to "https://www.google.com"
    Then I should be able to find the "About" link

  @smoke
  Scenario: Identify another link on the page
    Given I navigate to "https://www.google.com"
    Then I should be able to find the "Store" link
