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

- When interacting with locators, ensure that the correct action method (e.g., `.click()`) is called on the locator object, and that the locator is correctly identifying the target element.

- Before clicking 'View Cart', ensure the page is fully loaded and any potential overlays (e.g., promotional modals) are closed.

- Before clicking 'View Cart', ensure any modals or overlays are closed to prevent element occlusion. Also, wait for the page to fully load and any dynamic content to render before attempting to interact with the cart link.

- When targeting a specific product element, avoid using generic class names like `.productinfo`. Instead, use a more specific locator strategy that includes unique attributes or text content to ensure you target the intended element.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any overlaying elements (e.g., promotional pop-ups) are dismissed. Consider adding an explicit wait for product details to load.

- Before clicking 'Add to cart', ensure the product details are fully loaded and visible. Implement a check for a loading spinner or a specific element indicating readiness.

- When locating elements by visible text in Playwright, use the `:has-text()` selector or `filter()` method instead of passing `text` directly to the `locator()` method.

- Before interacting with the search input field, ensure that the page has fully loaded and any overlays or modals that might obscure the element have been dismissed. Consider adding a short delay or explicit wait for a parent element to be visible before attempting to fill the search input.

- When locating elements by visible text in Playwright, use the `filter()` method with the `has_text` option instead of passing `text` directly to the `locator()` method.

- When locating elements by attribute in Playwright, use attribute selectors (e.g., `a[title='Add to cart']`) instead of passing attributes as keyword arguments to the `locator()` method.

- Before clicking 'Add to cart', ensure the product details page is fully loaded and any overlaying elements (e.g., modals, spinners) are dismissed. Consider adding an explicit wait for a specific element on the product details page to confirm it's ready.

- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Consider waiting for a specific element related to the product details to load before attempting to add it to the cart.

- Before clicking 'Add to cart', ensure any overlaying elements (e.g., modals, banners) are dismissed or the button is fully visible and interactable. Consider adding a short delay or explicit wait for the element to be stable.

- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Consider adding a short explicit wait or checking for a loading spinner to disappear.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any overlaying elements (e.g., loading spinners, modals) are dismissed. Consider adding an explicit wait for the product image to load as a proxy for full page load.

- When navigating to '/products', implement a retry mechanism with exponential backoff to handle potential network latency or server delays. Also, verify the presence of a loading indicator to ensure the application is actively processing the navigation request.

- When navigating to '/products', implement a retry mechanism with exponential backoff to handle potential network latency or server delays. Also, check for modal dialogs or overlays that might prevent the page from loading correctly.

- When navigating to '/products', implement a retry mechanism with exponential backoff to handle potential network latency or server delays. Also, check for any overlaying elements (e.g., modals, banners) that might prevent the page from loading correctly.

<<<<<<< Updated upstream
- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Consider waiting for a specific element related to the product details to load before attempting to add it to the cart.

- Before clicking 'Add to cart', ensure the element is visible and stable. Implement a retry mechanism with a short delay to handle potential loading delays or transient overlays.

- Before clicking 'Add to cart', ensure the product is fully loaded and visible. Consider waiting for a specific product element to load before attempting to add it to the cart.
=======
- Before interacting with the search input field, ensure the page is fully loaded and any overlays or animations that might obscure the element have completed. Consider adding a short delay or a wait-for-selector before attempting to fill the field.

- Before interacting with the search input field, ensure the page is fully loaded and any overlays or animations that might obscure the element have completed. Consider adding a short wait or using `locator.wait_for()` with a `state='visible'` option.

- Before interacting with the search input field, ensure the page is fully loaded and any overlays or animations that might obscure the element have completed. Consider adding a short delay or a wait-for-selector before attempting to fill the field.
>>>>>>> Stashed changes

- When locating elements by title attribute within a parent locator, use `locator('xpath=//a[@title="Add to cart"]')` instead of passing title directly to the locator method.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any overlaying elements (e.g., promotional modals, loading spinners) are dismissed. Consider adding explicit waits for relevant product details to load.

- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Check for any overlaying elements (e.g., modals, banners) that might be blocking the button and handle them accordingly.

- When navigating to '/products', implement a retry mechanism with exponential backoff to handle potential network latency or server-side delays. Also, check for modal dialogs or overlays that might prevent the navigation from completing.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any overlaying elements (e.g., promotional modals) are dismissed. Consider adding a short explicit wait for the element to become stable.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any loading indicators are dismissed. Consider adding an explicit wait for the product image or description to be visible.

- Before clicking 'Add to cart', ensure any overlaying elements (e.g., modals, banners) are dismissed or the button is fully visible and interactable. Consider adding a short delay or explicit wait for the element to be stable.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any overlaying elements (e.g., modals, banners) are dismissed. Consider adding a short wait or using `element.wait_for_element_state('visible')` before attempting to click.

- When interacting with 'Add to cart' buttons on the product page, implement a retry mechanism with exponential backoff to handle potential loading delays or dynamic content updates. Also, check for overlaying elements that might prevent the click.

<<<<<<< Updated upstream
- When navigating to '/products', implement a retry mechanism with exponential backoff to handle potential slow server responses or intermittent network issues. Also, verify the page title or a unique element on the '/products' page to confirm successful navigation, rather than relying solely on the URL.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any promotional overlays are dismissed. Implement a retry mechanism with a short delay if the element is not immediately found.

- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Consider waiting for a specific product detail element to load before attempting to add the product to the cart.
=======
- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Consider waiting for a specific element related to the product details to load before attempting to add it to the cart.

- Before clicking 'Add to cart', ensure the product is fully loaded and visible on the page. Consider waiting for a specific product element to load before attempting to add it to the cart.

- Before clicking 'Add to cart', ensure the product details are fully loaded and any overlaying elements (e.g., promotional pop-ups) are dismissed. Consider adding a short explicit wait for the product details section to be visible.
>>>>>>> Stashed changes
