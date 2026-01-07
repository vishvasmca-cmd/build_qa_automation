# Locator Golden Set (Playwright + Python)

## Principles

- Prefer **role + accessible name** (`get_by_role`, `get_by_label`) over CSS/XPath.
- Prefer **data-testid** when available, combined with text filters when needed.
- Avoid positional selectors (`nth-child`) and style‑driven classes unless there is no alternative.
- Use semantic actions (`check`, `uncheck`, `fill`, `click`) on the right element (input vs label, etc.).

---

## Example 1 – Button with ARIA name
```html
<button type="submit" aria-label="Save changes">
  <span class="icon-save"></span>
  Save
</button>
```

**Good**
```python
page.get_by_role("button", name="Save changes")
page.get_by_role("button", name="Save")
```

**Bad**
```python
page.locator("button.icon-save")
page.locator("button[type='submit']")
page.locator("text=Save")
```
**Rule**: Use button role + accessible name. CSS classes and generic attributes are last resort.

---

## Example 2 – Labeled input
```html
<label for="email">Email address</label>
<input id="email" name="email" type="email" />
```

**Good**
```python
page.get_by_label("Email address")
```

**OK fallback**
```python
page.locator("#email")
page.locator("input[name='email']")
```

**Bad**
```python
page.locator("input[type='email']")
page.get_by_text("Email address").click()
```
**Rule**: Always start with get_by_label for form controls.

---

## Example 3 – Data-testid for complex elements
```html
<div data-testid="user-card" data-user-id="42">
  <span class="user-name">Alice Johnson</span>
  <span class="user-role">Admin</span>
</div>
```

**Good**
```python
page.get_by_test_id("user-card")
page.get_by_test_id("user-card").filter(has_text="Alice Johnson")
```

**Bad**
```python
page.locator("div[data-user-id='42']")
page.locator(".user-name:has-text('Alice')")
```
**Rule**: data-testid is the primary hook; combine with text instead of internal IDs or styling classes.

---

## Example 4 – List items
```html
<ul role="list">
  <li role="listitem">Dashboard</li>
  <li role="listitem">Settings</li>
  <li role="listitem">Logout</li>
</ul>
```

**Good**
```python
page.get_by_role("listitem", name="Settings")
```

**OK fallback**
```python
page.locator("li", has_text="Settings")
```

**Bad**
```python
page.locator("ul li:nth-child(2)")
page.locator("text=Settings")
```
**Rule**: Select by role + name, never by position when avoidable.

---

## Example 5 – Table row + inner button
```html
<tr data-testid="order-row" data-order-id="A123">
  <td class="order-id">A123</td>
  <td class="order-status">Shipped</td>
  <td><button>Details</button></td>
</tr>
```

**Good**
```python
row = page.get_by_test_id("order-row").filter(has_text="A123")
row.get_by_role("button", name="Details").click()
```

**OK composite**
```python
row = page.locator("tr[data-testid='order-row']", has_text="A123")
row.locator("button", has_text="Details").click()
```

**Bad**
```python
page.locator("tr:nth-child(1) button").click()
page.locator("text=Details").click()
```
**Rule**: First select the row instance, then act on a child control.

---

## Example 6 – Nav link with accessible label
```html
<nav>
  <a href="/settings" aria-label="Account settings">
    <i class="icon-settings"></i>
  </a>
</nav>
```

**Good**
```python
page.get_by_role("link", name="Account settings")
```

**OK fallback**
```python
page.locator('a[href="/settings"]')
```

**Bad**
```python
page.locator(".icon-settings").click()
```
**Rule**: Prefer link role + label; never target a purely decorative icon.

---

## Example 7 – Checkbox
```html
<label>
  <input type="checkbox" name="terms" />
  I agree to the Terms and Conditions
</label>
```

**Good**
```python
checkbox = page.get_by_label("I agree to the Terms and Conditions")
checkbox.check()
checkbox.uncheck()
```

**Bad**
```python
page.locator("input[name='terms']").click()
page.get_by_text("Terms and Conditions").click()
```
**Rule**: Use label-based locator and semantic check() / uncheck().

---

## Example 8 – Dropdowns (Select)
```html
<label for="sort">Sort by</label>
<select id="sort">
  <option value="price_asc">Price (low to high)</option>
  <option value="price_desc">Price (high to low)</option>
</select>
```

**Good**
```python
page.get_by_label("Sort by").select_option(label="Price (low to high)")
# OR by value
page.get_by_label("Sort by").select_option("price_asc")
```

**Bad**
```python
# NEVER try to click an <option> directly
page.get_by_role("option", name="Price (low to high)").click()
page.locator("select").click()
page.locator("option[value='price_asc']").click()
```
**Rule**: Use `select_option()` on the `<select>` element (via label or role). Never `click()` an `<option>`.
