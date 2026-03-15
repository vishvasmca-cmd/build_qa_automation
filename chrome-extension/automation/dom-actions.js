/**
 * DOM Actions - Browser-native automation
 * Replaces Playwright with pure JavaScript DOM manipulation
 */

export class DOMActions {
    constructor() {
        this.defaultTimeout = 10000; // 10 seconds
    }

    async navigate(url) {
        console.log(`[DOM-ACTIONS] Navigating to: ${url}`);
        window.location.href = url;

        // Wait for page load
        return new Promise(resolve => {
            if (document.readyState === 'complete') {
                resolve();
            } else {
                window.addEventListener('load', resolve, { once: true });
            }
        });
    }

    async click(element, options = {}) {
        if (!element) throw new Error('Element is null or undefined');

        console.log(`[DOM-ACTIONS] Clicking element:`, element);

        // Scroll element into view
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        await this.wait(300);

        // Highlight element for visual feedback
        if (options.highlight !== false) {
            this.highlightElement(element);
        }

        // Check if it's a select option
        if (element.tagName === 'OPTION') {
            const select = element.closest('select');
            if (select) {
                select.value = element.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                return;
            }
        }

        // Perform click
        element.click();
        await this.wait(500); // Wait for click handlers
    }

    async clickAtCoordinates(x, y, options = {}) {
        console.log(`[DOM-ACTIONS] Clicking at coordinates: (${x}, ${y})`);

        // Find element at coordinates
        const element = document.elementFromPoint(x, y);
        if (element) {
            console.log(`[DOM-ACTIONS] Element at point: ${element.tagName}`);
            if (options.highlight !== false) {
                this.highlightElement(element);
            }
        }

        // Dispatch mouse event sequence
        const mouseEvents = ['mousedown', 'mouseup', 'click'];
        for (const type of mouseEvents) {
            const event = new MouseEvent(type, {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: x,
                clientY: y
            });

            if (element) {
                element.dispatchEvent(event);
            } else {
                document.dispatchEvent(event);
            }
            await this.wait(50);
        }

        await this.wait(500);
    }

    async fill(element, value, options = {}) {
        if (!element) throw new Error('Element is null or undefined');

        console.log(`[DOM-ACTIONS] Filling element with: ${value}`);

        // Scroll into view
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        await this.wait(200);

        // Highlight element
        if (options.highlight !== false) {
            this.highlightElement(element);
        }

        // Focus element
        element.focus();

        // Clear existing value
        element.value = '';
        element.dispatchEvent(new Event('input', { bubbles: true }));

        // Type character by character for realistic simulation
        if (options.realistic !== false) {
            for (const char of value) {
                element.value += char;
                element.dispatchEvent(new Event('input', { bubbles: true }));
                await this.wait(50 + Math.random() * 50); // Human-like typing speed
            }
        } else {
            element.value = value;
            element.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Trigger change event
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.blur();
    }

    async hover(element) {
        if (!element) throw new Error('Element is null or undefined');

        console.log(`[DOM-ACTIONS] Hovering element:`, element);

        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        const rect = element.getBoundingClientRect();
        const mouseEvent = new MouseEvent('mouseover', {
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: rect.left + rect.width / 2,
            clientY: rect.top + rect.height / 2
        });

        element.dispatchEvent(mouseEvent);
        element.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
    }

    async validate(element, expectedValue) {
        if (!element) throw new Error('Element is null or undefined');

        console.log(`[DOM-ACTIONS] Validating element:`, element);

        const actualValue = this.getElementValue(element);

        if (actualValue !== expectedValue) {
            throw new Error(`Validation failed: expected "${expectedValue}", got "${actualValue}"`);
        }

        return true;
    }

    getElementValue(element) {
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            return element.value;
        }
        return element.textContent.trim();
    }

    highlightElement(element, duration = 2000) {
        const originalOutline = element.style.outline;
        const originalBoxShadow = element.style.boxShadow;

        element.style.outline = '3px solid #38bdf8';
        element.style.boxShadow = '0 0 10px #38bdf8';

        setTimeout(() => {
            element.style.outline = originalOutline;
            element.style.boxShadow = originalBoxShadow;
        }, duration);
    }

    async waitForElement(selector, timeout = this.defaultTimeout) {
        const startTime = Date.now();

        return new Promise((resolve, reject) => {
            const check = () => {
                const element = document.querySelector(selector);
                if (element) {
                    resolve(element);
                } else if (Date.now() - startTime > timeout) {
                    reject(new Error(`Timeout waiting for element: ${selector}`));
                } else {
                    setTimeout(check, 100);
                }
            };
            check();
        });
    }

    async waitForNavigation(timeout = this.defaultTimeout) {
        return new Promise((resolve, reject) => {
            const timeoutId = setTimeout(() => {
                reject(new Error('Navigation timeout'));
            }, timeout);

            const listener = () => {
                clearTimeout(timeoutId);
                resolve();
            };

            // Listen for various navigation events
            window.addEventListener('load', listener, { once: true });

            // Also check if page is already loaded
            if (document.readyState === 'complete') {
                clearTimeout(timeoutId);
                resolve();
            }
        });
    }

    async wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Utility: Check if element is visible
    isVisible(element) {
        if (!element) return false;

        const style = window.getComputedStyle(element);
        const rect = element.getBoundingClientRect();

        return (
            style.display !== 'none' &&
            style.visibility !== 'hidden' &&
            style.opacity !== '0' &&
            rect.width > 0 &&
            rect.height > 0
        );
    }

    // Utility: Get all visible text on page
    getPageText() {
        return document.body.innerText;
    }

    // Utility: Take screenshot (via Chrome Extension API)
    async takeScreenshot() {
        return new Promise((resolve) => {
            chrome.runtime.sendMessage({ type: 'CAPTURE_SCREENSHOT' }, (response) => {
                resolve(response?.dataUrl || null);
            });
        });
    }
}
