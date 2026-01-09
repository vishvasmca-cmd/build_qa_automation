
- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or transition. It might be covered by a loading overlay or require some JavaScript to fully initialize.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with the 'Add to cart' button to ensure it is visible and enabled before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It might be obscured or not yet fully rendered.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with the 'Add to cart' button to ensure it's visible and enabled before attempting to click it.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. Always implement a short wait or visibility check.

- ✅ PREFERRED: DO use explicit waits with `locator.wait_for()` to ensure the 'Add to cart' button is visible and enabled before attempting to click it. Consider using `locator.is_visible()` or `locator.is_enabled()` as conditions.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It may require a short wait or a specific condition to be met.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with 'Add to cart' buttons, especially after actions that might trigger dynamic content updates.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_role` with a generic name like 'Add to cart' without ensuring uniqueness or waiting for element stability.

- ✅ PREFERRED: DO implement explicit waits and consider more specific locators (e.g., using data attributes or CSS selectors) to target the 'Add to cart' button, especially when dealing with potentially dynamic content or overlays.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page transition. It may be obscured by a loading overlay or other dynamic content.

- ✅ PREFERRED: DO implement explicit waits or retry mechanisms when interacting with 'Add to cart' buttons, especially after page transitions or dynamic content updates. Consider using `locator.wait_for()` with a `state='visible'` or `state='enabled'` option.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It may require a short delay or a specific condition to be met.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the 'Add to cart' button is visible, enabled, and stable before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or product selection. It might be behind a loading state or animation.

- ✅ PREFERRED: DO implement explicit waits with `page.locator(...).first.wait_for()` before attempting to click the 'Add to cart' button, checking for visibility and/or enabling.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after a page load or transition. It might be covered by an overlay, animation, or still loading.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure the 'Add to cart' button is visible and enabled before attempting to click it. Consider using `locator.wait_for()` with `state='visible'` and `state='enabled'`.

- ⚠️ PROHIBITED: DON'T assume the 'Add to cart' button is immediately clickable after page load. It might be covered by a loading overlay or require some JavaScript to execute first.

- ✅ PREFERRED: DO implement a retry mechanism or explicit wait condition before clicking the 'Add to cart' button, ensuring it is both visible and enabled.
