/**
 * Semantic Page Model
 * Generates a clean, deterministic JSON representation of the page state for AI consumption.
 * Concepts borrowed from: Page Object Model (QA), Data Layers (Analytics), and Accessibility Trees.
 */
export class SemanticPageModel {
    constructor() {
        this.state = {
            pageType: 'unknown',
            url: window.location.href,
            user: { loggedIn: false },
            cart: { count: 0, total: 0 },
            products: [],
            availableActions: []
        };
    }

    /**
     * Main method to analyze the DOM and return the semantic state.
     */
    getState() {
        this._detectPageType();
        this._detectUserState();
        this._detectCartState();
        this._detectProducts();
        this._deriveActions();

        // Expose to window for debugging/external agents
        window.__MCP_STATE__ = this.state;
        return this.state;
    }

    _detectPageType() {
        const url = window.location.href.toLowerCase();
        if (url.includes('inventory')) this.state.pageType = 'inventory';
        else if (url.includes('cart')) this.state.pageType = 'cart';
        else if (url.includes('checkout-step-one')) this.state.pageType = 'checkout_info';
        else if (url.includes('checkout-step-two')) this.state.pageType = 'checkout_summary';
        else if (url.includes('checkout-complete')) this.state.pageType = 'checkout_complete';
        else if (url.includes('id=')) this.state.pageType = 'product_detail';
        else if (document.querySelector('#login-button')) this.state.pageType = 'login';
        else this.state.pageType = 'general';
    }

    _detectUserState() {
        // Robust check for login state
        const inventoryList = document.querySelector('.inventory_list');
        const cartBadge = document.querySelector('.shopping_cart_link');
        const menuButton = document.querySelector('#react-burger-menu-btn');

        this.state.user.loggedIn = !!(inventoryList || cartBadge || menuButton) && this.state.pageType !== 'login';
    }

    _detectCartState() {
        const badge = document.querySelector('.shopping_cart_badge');
        this.state.cart.count = badge ? parseInt(badge.textContent) : 0;

        // Try to find total if on cart/checkout pages
        const totalLabel = document.querySelector('.summary_total_label');
        if (totalLabel) {
            const match = totalLabel.textContent.match(/[\d,]+\.\d{2}/);
            this.state.cart.total = match ? parseFloat(match[0].replace(/,/g, '')) : 0;
        }
    }

    _detectProducts() {
        this.state.products = [];
        const items = document.querySelectorAll('.inventory_item, .cart_item');

        items.forEach(item => {
            const name = item.querySelector('.inventory_item_name')?.textContent;
            const priceText = item.querySelector('.inventory_item_price')?.textContent;
            const price = priceText ? parseFloat(priceText.replace('$', '')) : 0;
            const button = item.querySelector('button');
            const inCart = button?.textContent.toLowerCase().includes('remove') || item.classList.contains('cart_item');

            // Capture Robust Selector
            let selector = null;
            if (button) {
                if (button.id) selector = `#${button.id}`;
                else if (button.dataset.test) selector = `[data-test="${button.dataset.test}"]`;
            }

            if (name) {
                this.state.products.push({
                    name,
                    price,
                    inCart,
                    selector,
                    actions: inCart ? ['remove_from_cart'] : ['add_to_cart']
                });
            }
        });

        // Also capture cart items if on cart page (avoid duplicates logic preserved)
        if (this.state.pageType === 'cart' || this.state.pageType === 'checkout_summary') {
            const cartItems = document.querySelectorAll('.cart_item');
            cartItems.forEach(item => {
                const name = item.querySelector('.inventory_item_name')?.textContent;
                // ... (simplified for brevity, main logic is above)
            });
        }
    }

    _deriveActions() {
        this.state.availableActions = ['navigate_home', 'view_cart']; // Global actions

        switch (this.state.pageType) {
            case 'login':
                this.state.availableActions = ['login'];
                break;
            case 'inventory':
                this.state.availableActions.push('sort_products', 'filter_products', 'logout');
                if (this.state.products.some(p => !p.inCart)) this.state.availableActions.push('add_to_cart');
                break;
            case 'cart':
                this.state.availableActions.push('checkout', 'continue_shopping', 'remove_from_cart');
                break;
            case 'checkout_info':
                this.state.availableActions.push('fill_shipping_details', 'cancel_checkout');
                break;
            case 'checkout_summary':
                this.state.availableActions.push('place_order', 'cancel_checkout');
                break;
            case 'checkout_complete':
                this.state.availableActions = ['navigate_home', 'logout'];
                break;
        }
    }
}
