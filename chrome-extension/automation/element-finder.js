/**
 * Element Finder - Smart locator strategies
 * Finds elements using multiple fallback strategies
 */

export class ElementFinder {
    constructor() {
        this.strategies = [
            this.byId,
            this.byTestId,
            this.byRole,
            this.byPlaceholder,
            this.byLabel,
            this.byText,
            this.byPartialText,
            this.byCssSelector,
            this.byXPath
        ];
    }

    async find(description, action = 'click', options = {}) {
        console.log(`[ELEMENT-FINDER] Searching for: "${description}" (action: ${action})`);

        // Try each strategy in order
        for (const strategy of this.strategies) {
            try {
                const element = await strategy.call(this, description, action);
                if (element && this.isValidForAction(element, action)) {
                    console.log(`[ELEMENT-FINDER] Found via strategy: ${strategy.name}`);
                    return element;
                }
            } catch (e) {
                // Continue to next strategy
            }
        }

        console.warn(`[ELEMENT-FINDER] No element found for: "${description}"`);
        return null;
    }

    byId(description) {
        // Try exact ID match
        const id = description.replace(/[^a-zA-Z0-9_-]/g, '-').toLowerCase();
        return document.getElementById(id) || document.getElementById(description);
    }

    byTestId(description) {
        // data-testid, data-test, data-qa attributes
        const testId = description.toLowerCase().replace(/\s+/g, '-');
        return (
            document.querySelector(`[data-testid="${testId}"]`) ||
            document.querySelector(`[data-test="${testId}"]`) ||
            document.querySelector(`[data-qa="${testId}"]`)
        );
    }

    byRole(description, action) {
        // Map common descriptions to roles
        const roleMap = {
            'button': 'button',
            'link': 'link',
            'input': 'textbox',
            'checkbox': 'checkbox',
            'radio': 'radio'
        };

        for (const [key, role] of Object.entries(roleMap)) {
            if (description.toLowerCase().includes(key)) {
                const elements = document.querySelectorAll(`[role="${role}"]`);
                for (const el of elements) {
                    if (this.textMatches(el, description)) {
                        return el;
                    }
                }
            }
        }

        return null;
    }

    byPlaceholder(description) {
        // Find by placeholder text
        const inputs = document.querySelectorAll('input[placeholder], textarea[placeholder]');
        for (const input of inputs) {
            if (this.normalizeText(input.placeholder).includes(this.normalizeText(description))) {
                return input;
            }
        }
        return null;
    }

    byLabel(description) {
        // Find input by associated label
        const labels = document.querySelectorAll('label');
        for (const label of labels) {
            if (this.textMatches(label, description)) {
                // Try to find associated input
                if (label.htmlFor) {
                    return document.getElementById(label.htmlFor);
                }
                // Or input inside label
                return label.querySelector('input, textarea, select');
            }
        }
        return null;
    }

    byText(description) {
        // Exact text match
        const elements = this.getAllInteractiveElements();
        for (const el of elements) {
            if (this.normalizeText(el.textContent) === this.normalizeText(description)) {
                return el;
            }
        }
        return null;
    }

    byPartialText(description) {
        // Partial text match (fuzzy)
        const normalized = this.normalizeText(description);
        const elements = this.getAllInteractiveElements();

        let bestMatch = null;
        let bestScore = 0;

        for (const el of elements) {
            const text = this.normalizeText(el.textContent);
            const score = this.calculateSimilarity(text, normalized);

            if (score > bestScore && score > 0.6) {
                bestScore = score;
                bestMatch = el;
            }
        }

        return bestMatch;
    }

    byCssSelector(description) {
        // Try as CSS selector
        try {
            return document.querySelector(description);
        } catch {
            return null;
        }
    }

    byXPath(description) {
        // Try as XPath
        try {
            const result = document.evaluate(
                description,
                document,
                null,
                XPathValueType.FIRST_ORDERED_NODE_TYPE,
                null
            );
            return result.singleNodeValue;
        } catch {
            return null;
        }
    }

    // Helper: Get all potentially interactive elements
    getAllInteractiveElements() {
        return Array.from(document.querySelectorAll(
            'button, a, input, select, textarea, [role="button"], [role="link"], [onclick], [class*="btn"], [class*="button"]'
        ));
    }

    // Helper: Check if element is valid for action
    isValidForAction(element, action) {
        switch (action.toLowerCase()) {
            case 'fill':
                return ['INPUT', 'TEXTAREA', 'SELECT'].includes(element.tagName);
            case 'click':
                return true; // Any element can be clicked
            case 'hover':
                return true;
            default:
                return true;
        }
    }

    // Helper: Normalize text for comparison
    normalizeText(text) {
        return text
            .toLowerCase()
            .replace(/[^a-z0-9]/g, '')
            .trim();
    }

    // Helper: Check if element text matches description
    textMatches(element, description) {
        const text = this.normalizeText(element.textContent);
        const desc = this.normalizeText(description);
        return text.includes(desc) || desc.includes(text);
    }

    // Helper: Calculate text similarity (simple Levenshtein-like)
    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;

        if (longer.length === 0) return 1.0;

        const editDistance = this.levenshteinDistance(longer, shorter);
        return (longer.length - editDistance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];

        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }

        return matrix[str2.length][str1.length];
    }
}
