Feature: Apple Homepage - Element Presence
  As a user
  I want to verify the presence of key elements on the Apple homepage
  So that I can ensure the basic functionality of the website is working

  @smoke
  Scenario: Verify presence of 5 buttons and 2 links
    Given I am on the Apple homepage
    Then I should see the "Store" button
    And I should see the "Mac" button
    And I should see the "iPad" button
    And I should see the "iPhone" button
    And I should see the "Watch" button
    And I should see the "Apple" link
    And I should see the "Store" link