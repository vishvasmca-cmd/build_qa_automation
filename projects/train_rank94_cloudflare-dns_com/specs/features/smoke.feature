Feature: Website Element Identification
  As a user
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the "https://cloudflare-dns.com" website
    Then I should see the "iPhone" button
    And I should see the "DNS" link
    And I should see the share button