Feature: Website UI Elements Verification
  As a user
  I want to verify the presence of key UI elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify website launch and presence of buttons and links
    Given I navigate to the "https://cloudflare-dns.com" website
    Then I should see the "iPhone" button
    And I should see the "Android" button
    And I should see the "MacOS" button
    And I should see the "Windows" button
    And I should see the "Linux" button
    And I should see the "Router" button
    And I should see the Cloudflare logo link
    And I should see the "1.1.1.1" link
    And I should see the "DNS" link
    And I should see the "Families" link
    And I should see the "More Info" link
    And I should see the "DNSPerf" link
    And I should see the "Community Forum" link
