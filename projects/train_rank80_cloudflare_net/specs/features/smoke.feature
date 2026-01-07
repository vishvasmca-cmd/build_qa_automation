Feature: Cloudflare Website - Smoke Tests

  @smoke
  Scenario: Verify website launch and presence of key elements
    Given User navigates to "https://cloudflare.net/"
    Then User should see the Cloudflare security check page

  @smoke
  Scenario: Attempt to bypass Cloudflare security check
    Given User navigates to "https://cloudflare.net/"
    Then User should be redirected to the Cloudflare homepage or see a bypass option
