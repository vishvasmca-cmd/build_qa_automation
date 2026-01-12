# Navigation Log: 1. Login: standard_user / secret_sauce. 2. Action: Add three items (Backpack, Bike Light, Bolt T-Shirt) to the cart. 3. Checkout: Go to the cart, click 'Checkout', fill in 'First', 'Last', and '11111' zip code. 4. Finalize: Click 'Continue' and then 'Finish'. 5. Verify: Assert that 'Thank you for your order!' is displayed.

| Step | Page | Action | Target | Outcome | Screenshot |
|------|------|--------|--------|---------|------------|
| 0 | HomePage | fill | Username | ✅ | [View](../snapshots/step_00_HomePage.png) |
| 1 | HomePage | fill | Password | ✅ | [View](../snapshots/step_01_HomePage.png) |
| 2 | SwagLabsPage | click | page.locator("[data-test='logi | ✅ | [View](../snapshots/step_02_HomePage.png) |
| 3 | SaucedemoInventoryPage | click | Add to cart | ✅ | [View](../snapshots/step_03_SaucedemoInventoryPage.png) |
| 4 | SaucedemoInventoryPage | click | Add to cart | ✅ | [View](../snapshots/step_04_SaucedemoInventoryPage.png) |
