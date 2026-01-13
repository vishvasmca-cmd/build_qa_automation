
- ⚠️ PROHIBITED: DON'T assume the username field is immediately available; the page might be loading or rendering elements dynamically.

- ✅ PREFERRED: DO use `locator.fill` with an increased timeout or `locator.wait_for` to ensure the element is present and visible before attempting to interact with it.

- ⚠️ PROHIBITED: DON'T use the `fill` action on button elements or any element that is not designed for text input.

- ✅ PREFERRED: DO use the `fill` action only on appropriate input fields (e.g., elements located by `getByRole('textbox')` or `getByLabel()`). Verify the element type before attempting to fill it.

- ⚠️ PROHIBITED: DON'T assume that an element is immediately visible and clickable after page load; always verify its visibility before attempting to interact with it.

- ✅ PREFERRED: DO implement explicit waits or assertions to ensure that elements are visible and enabled before attempting to click them, especially after page transitions or dynamic content updates.

- ⚠️ PROHIBITED: DON'T use the `fill` action on button elements or any element that is not an input field, textarea, select element, or an element with a contenteditable attribute.

- ✅ PREFERRED: DO use the `click` action for button elements to trigger their associated functionality. Use `fill` only on appropriate input elements.

- ⚠️ PROHIBITED: DON'T assume an element is immediately visible and clickable after page load; always verify its visibility before attempting to interact with it.

- ✅ PREFERRED: DO use `locator.is_visible()` or `locator.wait_for()` with `state='visible'` to ensure an element is visible before attempting to click it.

- ⚠️ PROHIBITED: DON'T use the `fill` action on elements that are not input fields, textareas, select elements, or elements with contenteditable and appropriate ARIA roles.

- ✅ PREFERRED: DO verify the element type before attempting to use the `fill` action. Use appropriate actions like `click` for buttons or `type` for input fields.

- ⚠️ PROHIBITED: DON'T rely solely on `get_by_text` without considering potential ambiguity or dynamic content changes. A more specific locator is needed.

- ✅ PREFERRED: DO use more resilient locators, such as `getByRole` or `getByTestId`, combined with explicit waits for element visibility and enabled state before attempting to click.

- ✅ PREFERRED: DO use the `fill` action only on appropriate input fields (e.g., `<input>`, `<textarea>`) or elements with `contenteditable` attribute. ALWAYS verify the element type before attempting to fill it.

- ⚠️ PROHIBITED: DON'T assume that elements are immediately visible after navigation; always explicitly wait for them to appear.

- ✅ PREFERRED: DO use `locator.wait_for()` with `visible: true` option before interacting with elements, especially after navigation or state changes.

- ⚠️ PROHIBITED: DON'T use the `fill` action on button elements or any element that is not an input, textarea, select, or contenteditable element.

- ✅ PREFERRED: DO use the `fill` action only on input, textarea, select, or contenteditable elements. Verify the element type before attempting to fill it.

- ⚠️ PROHIBITED: DON'T assume that menu items are immediately available after page load; always implement a wait strategy.

- ✅ PREFERRED: DO use explicit waits with `page.locator(...).wait_for()` or `page.wait_for_selector()` before interacting with elements, especially after navigation or significant page changes.
