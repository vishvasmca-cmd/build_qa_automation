- **ADVERTISEMENT OVERLAY**: This site has aggressive full-screen ads (e.g., `<div class="overlay-content">` or `<section id="advertisement">`) that intercept clicks.
  - **ACTION**: You MUST use `force=True` for ALL clicks on 'Add to cart' or 'View Product' buttons.
  - **ALTERNATIVE**: If `force=True` fails, inject this JS to remove ads: `self.page.evaluate("document.querySelectorAll('#advertisement, .ad-container').forEach(el => el.remove())")`

- Before attempting to add an item to the cart, ensure that any modals, banners, or overlays are closed or dismissed to prevent them from obstructing the 'Add to cart' button. Also, verify the item is in-stock and the button is enabled.

- Before interacting with 'Add to cart' buttons, ensure that any overlaying elements (modals, banners, etc.) are dismissed or that the button is fully loaded and visible. Website might be slow, so a longer timeout might be needed.

- Before interacting with the search input, ensure the main page content has fully loaded. Implement explicit waiting for a stable element on the page to confirm readiness.

- When interacting with the search input field, implement a retry mechanism with exponential backoff, and ensure no modal or overlay obscures the element before attempting to fill it.

- When interacting with the search input field, implement a more robust waiting strategy (e.g., using `wait_for` with `state='attached'` or `state='visible'`) before attempting to fill it. Account for potential delays in element loading, possibly due to dynamic content loading or network latency.

- Before interacting with the search input field, ensure that the page has fully loaded and that any potential overlays or modals that might obscure the element have been dismissed.

- Before interacting with the search input '#search_product', ensure that any overlaying elements (e.g., modals, banners) are dismissed or have finished loading.

- When adding items to the cart, check for potential modal overlays (e.g., promotional pop-ups) that might obscure the 'Add to cart' button. Close any such modals before attempting to click the button.

- Before interacting with the search input '#search_product', ensure that any modal dialogs or overlays (e.g., advertisements) are closed or dismissed to prevent obstruction.

- Before interacting with the search input field, ensure it is visible and enabled. Implement explicit waiting with error handling.

- Before interacting with the search box (#search_product), ensure any modal dialogs or overlays are closed or dismissed. Implement a retry mechanism with a short delay to handle potential loading delays of the search input.

- Before interacting with the search input field, ensure it is visible and enabled. Consider adding a retry mechanism or explicit wait condition to handle potential delays in the element's availability.

- Before interacting with any element on the page, especially the search bar, wait for the page to fully load and any potential overlays (e.g., advertisements, modals) to disappear or be dismissed. Consider adding a global page load wait strategy.

- Before interacting with the search input field, ensure that the search input is visible and enabled. Consider adding a wait_for_selector with a more generous timeout before attempting to fill the input field.

- Before interacting with any element on the page, especially after a page load or navigation, always wait for the element to be both visible and enabled. Prioritize explicit waits with reasonable timeouts over relying solely on default Playwright timeout.

- Before interacting with the search product field (`#search_product`), ensure it is visible and enabled. Consider adding a short wait or retry mechanism to handle potential loading delays or overlaying elements.

- Before adding an item to the cart, ensure that any modal dialogs (e.g., advertisements or pop-ups) are closed to prevent them from obscuring the 'Add to cart' button.

- Before clicking 'Add to cart', ensure the element is visible and not covered by any overlay or modal. Also, check for dynamically loaded content that might delay the element's appearance.

- Before adding a product to the cart, ensure that the product details page is fully loaded and any loading indicators are no longer present. Implement a retry mechanism for the 'Add to cart' button click if it fails initially.

- Before interacting with core elements (e.g. Continue Shopping), check for and dismiss any modal dialogs or advertisement overlays that may appear dynamically. Prioritize closing any advertisement to prevent obstruction of elements.

- When interacting with elements that may load dynamically or after a delay (e.g., 'Add to Cart' buttons, especially after filtering or page transitions), implement explicit waiting mechanisms (e.g., `wait_for_selector`, `wait_for_function`) with increased timeout duration to ensure element availability before attempting to interact with them. Also, consider re-evaluating the Locator.

- Before interacting with 'Add to cart' button, ensure that any modals or overlays (e.g., promotional popups) are closed to prevent obscuring the target element.

- Before interacting with a search input, ensure it is visible and enabled.  Consider adding a short explicit wait if the element's appearance is dependent on other network requests.

- When interacting with elements found using `.first()`, ensure the element is resolved before attempting actions like `.click()`.  Use `.first().locator('self')` to resolve the element.
