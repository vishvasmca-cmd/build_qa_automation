/**
 * DOM Inspector - Captures page context for AI element finding
 * Provides rich structural and semantic information about the page
 */

export class DOMInspector {
    async capturePageContext() {
        return {
            url: window.location.href,
            title: document.title,
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            interactiveElements: this.getInteractiveElements(),
            visibleText: this.getVisibleText(),
            pageType: this.detectPageType(),
            isLoggedIn: this.detectLoginStatus()
        };
    }

    getInteractiveElements() {
        const selectors = [
            'button',
            'a[href]',
            'input',
            'select',
            'textarea',
            'h1',
            'h2',
            'h3',
            '[role="button"]',
            '[onclick]',
            '[class*="btn"]',
            '[class*="button"]',
            '[class*="title"]',
            '[data-test="title"]',
            '.shopping_cart_badge', // Semantic Badge
            '.cart-badge',
            '[class*="badge"]',
            '[class*="count"]'
        ];

        const elements = document.querySelectorAll(selectors.join(', '));
        const results = [];

        elements.forEach((el, index) => {
            if (!this.isVisible(el)) return;

            const rect = el.getBoundingClientRect();
            results.push({
                index,
                tag: el.tagName.toLowerCase(),
                id: el.id || null,
                classes: Array.from(el.classList),
                text: this.getElementText(el),
                placeholder: el.placeholder || null,
                type: el.type || null,
                name: el.name || null,
                value: el.value || null,
                href: el.href || null,
                role: el.getAttribute('role') || null,
                ariaLabel: el.getAttribute('aria-label') || null,
                dataTestId: el.getAttribute('data-test') || el.getAttribute('data-testid') || null,
                position: {
                    x: Math.round(rect.left),
                    y: Math.round(rect.top),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                }
            });
        });

        return results;
    }

    getElementText(element) {
        // Get direct text content, limit to 150 chars
        let text = '';

        // For inputs, use value or placeholder
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            text = element.value || element.placeholder || '';
        } else {
            // Get text content, excluding child scripts
            const clone = element.cloneNode(true);
            clone.querySelectorAll('script, style').forEach(el => el.remove());
            text = clone.textContent || '';
        }

        return text.trim().replace(/\\s+/g, ' ').substring(0, 150);
    }

    getVisibleText() {
        // Get main visible text from page for context
        const body = document.body;
        if (!body) return '';

        const walker = document.createTreeWalker(
            body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: (node) => {
                    if (!node.textContent.trim()) return NodeFilter.FILTER_REJECT;
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    if (parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE') {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (!this.isVisible(parent)) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        const texts = [];
        let node;
        while (node = walker.nextNode()) {
            texts.push(node.textContent.trim());
        }

        return texts.join(' ').replace(/\\s+/g, ' ').substring(0, 1000);
    }

    detectPageType() {
        const url = window.location.href.toLowerCase();
        const pathname = window.location.pathname.toLowerCase();

        if (url.includes('login') || pathname.includes('login')) return 'login';
        if (url.includes('cart') || pathname.includes('cart')) return 'cart';
        if (url.includes('checkout') || pathname.includes('checkout')) return 'checkout';
        if (url.includes('inventory') || pathname.includes('inventory') || pathname.includes('products')) return 'inventory';
        if (url.includes('product') || pathname.includes('item')) return 'product';

        return 'other';
    }

    detectLoginStatus() {
        const loginIndicators = [
            'logout', 'sign out', 'log out', 'my account', 'profile', 'order history'
        ];

        // Search for indicators in links, buttons, and text
        const elements = document.querySelectorAll('a, button, span, div');
        for (const el of elements) {
            const text = el.textContent.toLowerCase();
            if (loginIndicators.some(indicator => text.includes(indicator))) {
                if (this.isVisible(el)) return true;
            }
        }

        // Check for common URL patterns
        const url = window.location.href.toLowerCase();
        if (url.includes('inventory.html') || url.includes('dashboard') || url.includes('account')) {
            return true;
        }

        return false;
    }

    isVisible(element) {
        if (!element) return false;

        const style = window.getComputedStyle(element);
        const rect = element.getBoundingClientRect();

        return (
            style.display !== 'none' &&
            style.visibility !== 'hidden' &&
            style.opacity !== '0' &&
            rect.width > 0 &&
            rect.height > 0 &&
            rect.top < window.innerHeight &&
            rect.bottom > 0
        );
    }

    // Helper: Get selector path for an element
    getSelectorPath(element) {
        if (element.id) {
            return `#${element.id}`;
        }

        if (element.getAttribute('data-test')) {
            return `[data-test="${element.getAttribute('data-test')}"]`;
        }

        const path = [];
        while (element && element.nodeType === Node.ELEMENT_NODE) {
            let selector = element.nodeName.toLowerCase();

            if (element.className) {
                const classes = Array.from(element.classList).join('.');
                if (classes) selector += `.${classes}`;
            }

            path.unshift(selector);
            element = element.parentElement;

            if (path.length > 3) break; // Limit depth
        }

        return path.join(' > ');
    }
}
