/**
 * AI Element Finder - Uses Gemini AI for intelligent element location
 * Analyzes DOM context to find elements based on natural language descriptions
 */

import { GeminiClient } from '../ai/gemini-client.js';
import { DOMInspector } from './dom-inspector.js'; // Assuming DOMInspector is in the same directory or needs to be imported

export class AIElementFinder {
    constructor(geminiClient) {
        this.gemini = geminiClient;
        this.inspector = new DOMInspector();
        this.elementMap = new WeakMap(); // Track coords for fallback
        this.cache = new Map(); // Cache element locations
    }

    async findElement(description, action, returnReasoning = false) {
        console.log(`[AIElementFinder] Looking for: "${description}" (action: ${action})`);

        // RESILIENCE FALLBACK: Hardcoded common selectors if AI fails for core icons
        const isCartRelated = description.toLowerCase().includes('cart') || description.toLowerCase().includes('badge');

        if (isCartRelated) {
            const commonCartSelectors = [
                '.shopping_cart_badge',
                '.shopping_cart_link',
                '.cart-badge',
                '#shopping_cart_container span',
                '.shopping-cart',
                '#cart_contents_container a'
            ];
            for (const sel of commonCartSelectors) {
                const el = document.querySelector(sel);
                if (el && this.inspector.isVisible(el)) {
                    console.log(`[AIElementFinder] Fallback success for cart element: ${sel}`);
                    const rect = el.getBoundingClientRect();
                    this.elementMap.set(el, {
                        x: Math.round(rect.left + rect.width / 2),
                        y: Math.round(rect.top + rect.height / 2)
                    });
                    return returnReasoning ? { element: el, reasoning: `Found via fallback: ${sel}` } : el;
                }
            }
        }

        // Check cache first
        const cacheKey = `${description}_${action}`;
        if (this.cache.has(cacheKey)) {
            const cachedIndex = this.cache.get(cacheKey);
            const element = this.getElementByIndex(cachedIndex);
            if (element && this.inspector.isVisible(element)) {
                return returnReasoning ? { element, reasoning: "Found in cache" } : element;
            }
            this.cache.delete(cacheKey);
        }

        // Capture current page context
        const context = await this.inspector.capturePageContext();

        if (context.interactiveElements.length === 0) {
            console.warn('[AIElementFinder] No interactive elements found on page');
            return null;
        }

        try {
            // DELEGATE TO BACKGROUND: Fixes Failed to Fetch / CORS
            const response = await chrome.runtime.sendMessage({
                type: 'FIND_ELEMENT_AI',
                payload: { description, action, context }
            });

            if (response && response.data && response.data.found) {
                const result = response.data;
                console.log(`[AIElementFinder] Found: ${result.reasoning}`);

                const element = this.getElementByIndex(result.elementIndex);
                if (element) {
                    this.cache.set(cacheKey, result.elementIndex);

                    // Store coords for fallback
                    const rect = element.getBoundingClientRect();
                    this.elementMap.set(element, {
                        x: Math.round(rect.left + rect.width / 2),
                        y: Math.round(rect.top + rect.height / 2)
                    });

                    return returnReasoning ? { element, reasoning: result.reasoning } : element;
                }
            } else {
                console.warn(`[AIElementFinder] AI could not locate: ${response?.data?.reasoning || 'No match'}`);
            }

        } catch (error) {
            console.error('[AIElementFinder] Delegation Error:', error);
        }

        return null;
    }

    getElementByIndex(index) {
        const selectors = [
            'button',
            'a[href]',
            'input',
            'select',
            'textarea',
            '[role="button"]',
            '[onclick]',
            '[class*="btn"]',
            '[class*="button"]',
            '.shopping_cart_link', // Ensure specific icon classes are included
            '.shopping_cart_badge', // Include badges
            '[class*="badge"]',
            '[class*="count"]'
        ];

        const elements = document.querySelectorAll(selectors.join(', '));
        const visibleElements = Array.from(elements).filter(el => this.inspector.isVisible(el));

        return visibleElements[index] || null;
    }

    clearCache() {
        this.cache.clear();
    }
}
