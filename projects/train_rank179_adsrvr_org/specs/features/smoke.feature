Feature: Website Element Verification
  As a user
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify website homepage loads successfully and contains buttons and links
    Given I navigate to the website "https://adsrvr.org/"
    Then I should see at least 5 buttons
    And I should see at least 2 links
