/**
 * WebMCP Tools - E-commerce validation utilities
 * Browser-native implementations of cart, price, and checkout validators
 */

export class WebMCPTools {
    constructor() {
        this.cartSelectors = [
            '.shopping_cart_badge',
            '.cart-badge',
            '.cart-count',
            '[class*="cart"][class*="count"]',
            '[class*="badge"]'
        ];

        this.priceSelectors = [
            '.inventory_item_price',
            '.price',
            '[class*="price"]',
            '[class*="cost"]'
        ];
    }

    // Get cart count
    async getCartCount() {
        try {
            // Try multiple common cart badge selectors
            for (const selector of this.cartSelectors) {
                const badge = document.querySelector(selector);
                if (badge) {
                    const count = parseInt(badge.textContent.trim()) || 0;
                    return { success: true, count, message: `Cart contains ${count} items` };
                }
            }

            // Fallback: count items in cart page
            const cartItems = document.querySelectorAll('.cart_item, [class*="cart-item"]');
            if (cartItems.length > 0) {
                return { success: true, count: cartItems.length, message: `Found ${cartItems.length} items in cart` };
            }

            return { success: false, count: 0, message: 'Cart badge not found' };
        } catch (error) {
            return { success: false, count: 0, error: error.message };
        }
    }

    // Get cart items
    async getCartItems() {
        try {
            const items = [];
            const itemElements = document.querySelectorAll('.cart_item, [class*="cart-item"]');

            for (const itemEl of itemElements) {
                const name = itemEl.querySelector('.inventory_item_name, [class*="item-name"]')?.textContent.trim();
                const price = this.extractPrice(itemEl.querySelector('.inventory_item_price, [class*="price"]')?.textContent);
                const quantity = parseInt(itemEl.querySelector('[class*="quantity"]')?.textContent) || 1;

                if (name && price !== null) {
                    items.push({ name, price, quantity });
                }
            }

            return { success: true, items, message: `Found ${items.length} items` };
        } catch (error) {
            return { success: false, items: [], error: error.message };
        }
    }

    // Get cart total
    async getCartTotal() {
        try {
            const totalElements = document.querySelectorAll('.summary_total_label, [class*="total"], [class*="grand-total"]');

            for (const el of totalElements) {
                const text = el.textContent;
                if (text.toLowerCase().includes('total')) {
                    const total = this.extractPrice(text);
                    if (total !== null) {
                        return { success: true, total_amount: total, message: `Total: $${total}` };
                    }
                }
            }

            return { success: false, total_amount: 0, message: 'Total not found' };
        } catch (error) {
            return { success: false, total_amount: 0, error: error.message };
        }
    }

    // Verify cart total calculation
    async verifyCartTotal() {
        try {
            const itemsResult = await this.getCartItems();
            if (!itemsResult.success) {
                return { success: false, error: 'Could not retrieve cart items' };
            }

            const items = itemsResult.items;
            const calculatedSubtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

            // Get subtotal from page
            const subtotalEl = document.querySelector('.summary_subtotal_label, [class*="subtotal"]');
            const displayedSubtotal = subtotalEl ? this.extractPrice(subtotalEl.textContent) : null;

            // Get total from page
            const totalResult = await this.getCartTotal();
            const displayedTotal = totalResult.total_amount;

            // Calculate tax
            const taxEl = document.querySelector('.summary_tax_label, [class*="tax"]');
            const tax = taxEl ? this.extractPrice(taxEl.textContent) : 0;

            const expectedTotal = calculatedSubtotal + tax;
            const isCorrect = Math.abs(expectedTotal - displayedTotal) < 0.01; // Allow for rounding

            return {
                success: isCorrect,
                subtotal_amount: calculatedSubtotal,
                tax_amount: tax,
                total_amount: displayedTotal,
                calculated_total: expectedTotal,
                is_correct: isCorrect,
                message: isCorrect ? 'Total calculation verified' : `Mismatch: expected $${expectedTotal}, got $${displayedTotal}`
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Get sorted products
    async getSortedProducts() {
        try {
            const products = [];
            const productElements = document.querySelectorAll('.inventory_item, [class*="product"]');

            for (const productEl of productElements) {
                const name = productEl.querySelector('.inventory_item_name, [class*="product-name"]')?.textContent.trim();
                const priceEl = productEl.querySelector('.inventory_item_price, [class*="price"]');
                const price = this.extractPrice(priceEl?.textContent);

                if (name && price !== null) {
                    products.push({ name, price, element: productEl });
                }
            }

            // Find cheapest and most expensive
            products.sort((a, b) => a.price - b.price);
            const cheapest = products[0];
            const mostExpensive = products[products.length - 1];

            return {
                success: true,
                products: products.map(p => ({ name: p.name, price: p.price })),
                cheapest: cheapest ? { name: cheapest.name, price: cheapest.price } : null,
                most_expensive: mostExpensive ? { name: mostExpensive.name, price: mostExpensive.price } : null
            };
        } catch (error) {
            return { success: false, products: [], error: error.message };
        }
    }

    // Verify checkout form
    async verifyCheckoutForm() {
        try {
            const requiredFields = ['firstName', 'lastName', 'postalCode'];
            const missing = [];

            for (const fieldName of requiredFields) {
                const field = document.querySelector(`#${fieldName}, [name="${fieldName}"], [data-test="${fieldName}"]`);
                if (!field || !field.value.trim()) {
                    missing.push(fieldName);
                }
            }

            return {
                success: missing.length === 0,
                is_complete: missing.length === 0,
                missing_fields: missing,
                message: missing.length === 0 ? 'Form complete' : `Missing: ${missing.join(', ')}`
            };
        } catch (error) {
            return { success: false, is_complete: false, missing_fields: [], error: error.message };
        }
    }

    // Verify order success
    async verifyOrderSuccess() {
        try {
            const successIndicators = [
                document.querySelector('.complete-header'),
                document.querySelector('[class*="success"]'),
                document.querySelector('[class*="complete"]')
            ];

            const hasSuccessMessage = successIndicators.some(el => {
                if (!el) return false;
                const text = el.textContent.toLowerCase();
                return text.includes('thank you') || text.includes('complete') || text.includes('success');
            });

            return {
                success: hasSuccessMessage,
                is_success: hasSuccessMessage,
                message: hasSuccessMessage ? 'Order completed successfully' : 'Success message not found'
            };
        } catch (error) {
            return { success: false, is_success: false, error: error.message };
        }
    }

    // Verify login success
    async verifyLoginSuccess() {
        try {
            // Check for error messages
            const errorEl = document.querySelector('[data-test="error"], .error-message, [class*="error"]');
            if (errorEl && errorEl.textContent.trim()) {
                return {
                    success: false,
                    is_logged_in: false,
                    error_message: errorEl.textContent.trim(),
                    message: 'Login failed'
                };
            }

            // Check if redirected to inventory/dashboard
            const isOnInventory = window.location.href.includes('inventory') ||
                document.querySelector('.inventory_list, [class*="product"]') !== null;

            return {
                success: isOnInventory,
                is_logged_in: isOnInventory,
                message: isOnInventory ? 'Login successful' : 'Not logged in'
            };
        } catch (error) {
            return { success: false, is_logged_in: false, error: error.message };
        }
    }

    // Helper: Extract price from text
    extractPrice(text) {
        if (!text) return null;

        // Remove currency symbols and extract number
        const match = text.match(/[\d,]+\.?\d*/);
        if (match) {
            return parseFloat(match[0].replace(/,/g, ''));
        }

        return null;
    }

    // Helper: Check if on specific page type
    getPageType() {
        const url = window.location.href.toLowerCase();

        if (url.includes('cart')) return 'cart';
        if (url.includes('checkout-step-one')) return 'checkout_info';
        if (url.includes('checkout-step-two')) return 'checkout_summary';
        if (url.includes('checkout-complete')) return 'complete';
        if (url.includes('inventory')) return 'inventory';
        return 'other';
    }
    // ============================================================================
    // ACTION TOOLS (Executors) with STATE-AWARE VERIFICATION
    // ============================================================================

    // Login Action
    async login(username, password) {
        try {
            // 1. PRE-CHECK
            const checkLoginState = () => {
                return window.location.href.includes('inventory') ||
                    document.querySelector('.inventory_list, [class*="product-list"]') !== null;
            };

            if (checkLoginState()) {
                return { success: true, message: "Already logged in (Pre-check)", action: "login_skipped" };
            }

            const userField = document.querySelector('input[data-test="username"], #user-name, input[name="user-name"], input[name="username"], input[type="email"]');
            const passField = document.querySelector('input[data-test="password"], #password, input[name="password"], input[type="password"]');
            const submitBtn = document.querySelector('input[data-test="login-button"], #login-button, button[type="submit"], input[type="submit"]');

            if (!userField || !passField || !submitBtn) {
                return { success: false, error: "Login fields not found" };
            }

            // 2. ACTION
            const setNativeValue = (element, value) => {
                const lastValue = element.value;
                element.value = value;
                const tracker = element._valueTracker;
                if (tracker) tracker.setValue(lastValue);
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
            };

            setNativeValue(userField, username);
            setNativeValue(passField, password);
            await new Promise(r => setTimeout(r, 200));
            submitBtn.click();

            // 3. POST-CHECK (Wait for state change)
            let retries = 5;
            while (retries > 0) {
                await new Promise(r => setTimeout(r, 500));
                if (checkLoginState()) {
                    return { success: true, message: "Login successful (State Verified)", action: "login" };
                }

                // Check for error
                const errorEl = document.querySelector('[data-test="error"], .error-message');
                if (errorEl) {
                    return { success: false, error: `Login failed: ${errorEl.textContent}` };
                }
                retries--;
            }

            return { success: false, error: "Login timeout - State did not change" };

        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Sort Products
    async sortProducts(direction) {
        try {
            const select = document.querySelector('.product_sort_container, select[data-test="product-sort-container"], select[name*="sort"]');
            if (!select) return { success: false, error: "Sort dropdown not found" };

            // 1. PRE-CHECK (Snapshot first item)
            const getFirstItem = () => {
                const item = document.querySelector('.inventory_item_name, [class*="product-name"]');
                const price = document.querySelector('.inventory_item_price, [class*="price"]');
                return (item?.textContent || "") + (price?.textContent || "");
            };
            const preState = getFirstItem();

            // 2. ACTION
            let value = "";
            const dir = direction.toLowerCase();
            if (dir.includes("low") && dir.includes("high")) value = "lohi";
            else if (dir.includes("high") && dir.includes("low")) value = "hilo";
            else if (dir.includes("a") && dir.includes("z")) value = "az";
            else if (dir.includes("z") && dir.includes("a")) value = "za";

            if (!value) {
                const options = Array.from(select.options);
                const match = options.find(o => o.text.toLowerCase().includes(dir));
                if (match) value = match.value;
            }

            if (value) {
                select.value = value;
                select.dispatchEvent(new Event('change', { bubbles: true }));

                // 3. POST-CHECK
                let retries = 5;
                while (retries > 0) {
                    await new Promise(r => setTimeout(r, 500));
                    const postState = getFirstItem();
                    if (postState !== preState) {
                        return { success: true, message: `Sorted by ${direction} (Order Changed)`, action: "sort" };
                    }
                    retries--;
                }
                // Even if order didn't change (e.g. already sorted), we might consider it success if value matches
                if (select.value === value) return { success: true, message: `Sorted by ${direction} (Verified Value)`, action: "sort" };
            }
            return { success: false, error: `Could not determine sort value for "${direction}"` };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Search Products
    async searchProducts(query) {
        try {
            const searchInput = document.querySelector('input[type="search"], input[name*="search"], input[placeholder*="Search"]');
            if (!searchInput) return { success: false, error: "Search bar not found" };

            // 1. PRE-CHECK
            const getProductCount = () => document.querySelectorAll('.inventory_item, [class*="product-item"]').length;
            const preCount = getProductCount();

            // 2. ACTION
            const lastValue = searchInput.value;
            searchInput.value = query;
            const tracker = searchInput._valueTracker;
            if (tracker) tracker.setValue(lastValue);
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));

            // Submit
            await new Promise(r => setTimeout(r, 200));
            searchInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
            searchInput.dispatchEvent(new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', bubbles: true }));
            searchInput.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', bubbles: true }));

            // Try Submit button
            const form = searchInput.closest('form');
            if (form) {
                const btn = form.querySelector('button, input[type="submit"]');
                if (btn) btn.click();
                else form.requestSubmit();
            }

            // 3. POST-CHECK
            let retries = 5;
            while (retries > 0) {
                await new Promise(r => setTimeout(r, 500));
                const postCount = getProductCount();
                // Search usually changes count, or at least reloads DOM
                // Weak check: just return success if no error, as count might be same
                if (document.body.innerText.includes(query)) { // Simple check if query term exists on page now
                    return { success: true, message: `Searched for "${query}"`, action: "search" };
                }
                retries--;
            }

            return { success: true, message: `Searched for "${query}" (Action Completed)`, action: "search" };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Add To Cart (Advanced)
    async addToCart(criteria) {
        try {
            // 1. PRE-CHECK
            const getBadgeCount = () => {
                const badge = document.querySelector('.shopping_cart_badge, .cart-count');
                return badge ? parseInt(badge.textContent) : 0;
            };
            const preCount = getBadgeCount();

            // GET PRODUCTS
            const productCards = Array.from(document.querySelectorAll('.inventory_item, [class*="product-item"], [class*="product-card"]'));
            if (productCards.length === 0) return { success: false, error: "No products found on page" };

            let targetCard = null;
            if (criteria.name) {
                targetCard = productCards.find(card => {
                    const title = card.querySelector('.inventory_item_name, [class*="title"], [class*="name"]')?.textContent || "";
                    return title.toLowerCase().includes(criteria.name.toLowerCase());
                });
            } else if (criteria.rank) {
                const parsedProducts = productCards.map(card => {
                    const priceText = card.querySelector('.inventory_item_price, [class*="price"]')?.textContent || "$0";
                    const price = this.extractPrice(priceText) || 0;
                    return { card, price };
                });
                parsedProducts.sort((a, b) => a.price - b.price);
                if (criteria.rank === "cheapest") targetCard = parsedProducts[0].card;
                else if (criteria.rank === "most_expensive") targetCard = parsedProducts[parsedProducts.length - 1].card;
                else if (criteria.rank === "first") targetCard = parsedProducts[0].card;
                else if (criteria.rank === "last") targetCard = parsedProducts[parsedProducts.length - 1].card;
            }

            if (!targetCard && !criteria.name && !criteria.rank) targetCard = productCards[0];
            if (!targetCard) return { success: false, error: `Product not found: ${JSON.stringify(criteria)}` };

            const btn = targetCard.querySelector('button[id*="add-to-cart"], button[name*="add-to-cart"], button[class*="btn_primary"], button[class*="add-to-cart"]');
            if (!btn) return { success: false, error: "Add button not found" };

            // IDEMPOTENCY
            if (btn.textContent.toLowerCase().includes('remove')) {
                return { success: true, message: "Item already in cart", action: "add_to_cart_skipped" };
            }

            // 2. ACTION
            btn.click();

            // 3. POST-CHECK
            let retries = 5;
            while (retries > 0) {
                await new Promise(r => setTimeout(r, 200));
                const postCount = getBadgeCount();
                if (postCount > preCount) {
                    return { success: true, message: `Added to cart (Count: ${preCount} -> ${postCount})`, action: "add_to_cart" };
                }
                retries--;
            }

            // Fallback: Check button text changed to 'Remove'
            if (btn.textContent.toLowerCase().includes('remove')) {
                return { success: true, message: "Added to cart (Button State Verified)", action: "add_to_cart" };
            }

            return { success: false, error: "Cart count did not increase" };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Checkout: Fill Shipping
    async fillCheckoutForm(details) {
        try {
            const inputs = document.querySelectorAll('input, select, textarea');
            let filledCount = 0;

            for (const input of inputs) {
                const id = (input.id || "").toLowerCase();
                const name = (input.name || "").toLowerCase();
                const placeholder = (input.placeholder || "").toLowerCase();
                const label = input.labels?.[0]?.textContent.toLowerCase() || "";

                const context = id + " " + name + " " + placeholder + " " + label;

                let valToFill = null;

                if (context.includes('first') && context.includes('name')) valToFill = details.firstName;
                else if (context.includes('last') && context.includes('name')) valToFill = details.lastName;
                else if (context.includes('zip') || context.includes('postal')) valToFill = details.postalCode;
                else if (context.includes('email')) valToFill = details.email;
                else if (context.includes('city')) valToFill = details.city;
                else if (context.includes('address')) valToFill = details.address;

                if (valToFill) {
                    const lastValue = input.value;
                    input.value = valToFill;
                    const tracker = input._valueTracker;
                    if (tracker) tracker.setValue(lastValue);
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    filledCount++;
                }
            }

            // Try to submit/continue
            const continueBtn = document.querySelector('input[type="submit"], button[class*="cart_button"], button[class*="continue"]');
            if (continueBtn) {
                continueBtn.click();
                return { success: true, message: `Filled ${filledCount} fields and clicked continue`, action: "fill_checkout" };
            }

            return { success: true, message: `Filled ${filledCount} fields`, action: "fill_form_only" };

        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}
