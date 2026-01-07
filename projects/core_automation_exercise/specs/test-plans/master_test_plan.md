# Test Plan: core_automation_exercise

## Domain: E-commerce

### Scope

This test plan covers the core functionality of the e-commerce platform, focusing on product browsing, searching, adding to cart, and initiating the checkout process.

### Test Suites

This test plan defines two test suites:

1.  Smoke Suite: A minimal set of tests to verify the most critical functions.
2.  Regression Suite: A comprehensive suite to ensure that recent changes have not broken existing functionality.

### Module: Product Catalog

#### Description

This module focuses on testing the product catalog functionality, including browsing, searching, and viewing product details.

#### Test Cases

##### Smoke Suite

*   TC\_PC\_001: Navigate to Products page
*   TC\_PC\_002: Search for a product ('Dress')

##### Regression Suite

*   TC\_PC\_003: Filter products by category
*   TC\_PC\_004: Sort products by price
*   TC\_PC\_005: Search for a non-existent product

### Module: Shopping Cart

#### Description

This module focuses on testing the shopping cart functionality, including adding items to the cart, viewing the cart summary, and updating quantities.

#### Test Cases

##### Smoke Suite

*   TC\_SC\_001: Add item to cart

##### Regression Suite

*   TC\_SC\_002: Update quantity in cart
*   TC\_SC\_003: Remove item from cart
*   TC\_SC\_004: Add out-of-stock item (verify error)
*   TC\_SC\_005: Cart persistence (refresh page)

### Module: Checkout

#### Description

This module focuses on testing the checkout functionality, including entering shipping information, selecting a payment method, and completing the purchase.

#### Test Cases

##### Smoke Suite

*   TC\_CO\_001: Initiate checkout process

##### Regression Suite

*   TC\_CO\_002: Checkout with formatted address
*   TC\_CO\_003: Apply valid/invalid coupon code
*   TC\_CO\_004: Payment decline simulation
*   TC\_CO\_005: Calculate tax/shipping correctly

## Smoke Suite Strategy

The Smoke Suite is designed to provide a quick and efficient way to verify the core functionality of the application. The following checklist is applied to ensure the quality and effectiveness of the Smoke Suite:

1.  **Critical Paths:** Tests cover the most critical user flows (e.g., login, product search, add to cart, checkout).
2.  **Core Business Logic:** Tests validate the primary business logic (e.g., pricing, inventory management).
3.  **Positive Testing:** Focus is on positive scenarios with valid inputs.
4.  **Minimal Negative Testing:** Only critical security-related negative tests are included.
5.  **No Complex Edge Cases:** Complex or less common scenarios are excluded.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Independent Tests:** Tests are independent and do not rely on each other.
8.  **High Stability:** Tests are stable and reliable, minimizing false failures.
