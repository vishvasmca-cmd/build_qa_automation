Feature: Careerraah Smoke Tests
  As a QA Engineer
  I want to perform smoke tests on Careerraah.com
  So that I can ensure the application's availability and basic functionality

  @smoke
  Scenario: Verify Homepage Loads
    Given I navigate to the Careerraah homepage
    Then the homepage should load successfully

  @smoke
  Scenario: Navigate to Blog Page
    Given I navigate to the Careerraah homepage
    When I click the "Blog" link
    Then the Blog page should load successfully

  @smoke
  Scenario: Submit Contact Form
    Given I navigate to the Contact Us page
    When I fill in the contact form with valid data
    And I click the "Send Message" button
    Then the contact form should be submitted successfully
