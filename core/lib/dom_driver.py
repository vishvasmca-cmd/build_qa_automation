
# This script is designed for "2026-style" agentic browsing.
# It extracts only the essential interactive surface of the page,
# including visibility, spatial coordinates, and semantic labels.

DOM_EXTRACTION_SCRIPT = """
(offset = 0) => {
    const INTERACTIVE_SELECTORS = [
        'a', 'button', 'input', 'textarea', 'select', 'details', 
        '[role="button"]', '[role="checkbox"]', '[role="radio"]', 
        '[role="link"]', '[role="menuitem"]', '[role="tab"]',
        '[contenteditable="true"]', '[onclick]', '[tabindex]:not([tabindex="-1"])',
        'iframe', '[id*="captcha"]', '[class*="captcha"]', '#px-captcha', '#px-captcha-wrapper'
    ];

    const items = [];
    let idCounter = offset;

    function isVisible(el) {
        if (!el) return false;
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        
        return rect.width > 0 && rect.height > 0 && 
               style.display !== 'none' && 
               style.visibility !== 'hidden' && 
               style.opacity !== '0';
    }

    function getSemanticLabel(el, root = document) {
        // Prioritize what a user actually sees or what an assistive tool reads
        let label = el.getAttribute('aria-label') || 
                    el.getAttribute('placeholder') || 
                    el.getAttribute('title') || 
                    el.innerText || 
                    el.textContent || "";
        
        // Handle images/SVGs inside buttons (common in modern web)
        if (!label.trim()) {
            const img = el.querySelector('img');
            if (img && img.alt) label = img.alt;
            const svg = el.querySelector('svg');
            if (svg && svg.getAttribute('aria-label')) label = svg.getAttribute('aria-label');
            if (!label.trim() && svg) {
                const title = svg.querySelector('title');
                if (title) label = title.textContent;
            }
        }

        // Handle labeled inputs (Piercing Shadow DOM)
        if (!label.trim() && el.id) {
            try {
                const labelEl = root.querySelector(`label[for="${CSS.escape(el.id)}"]`);
                if (labelEl) {
                    label = labelEl.innerText;
                } else if (root !== document) {
                    // Fallback to global search if not found in same shadow root
                    const globalLabel = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
                    if (globalLabel) label = globalLabel.innerText;
                }
            } catch (e) {}
        }

        return label.trim().slice(0, 100).replace(/\\s+/g, ' ');
    }

    function traverse(node, currentRoot = document) {
        if (!node) return;

        // 1. Process node if it matches interactive intent
        let isInteractive = false;
        try {
            if (node.nodeType === 1) { // Element node
                if (INTERACTIVE_SELECTORS.some(s => node.matches && node.matches(s))) {
                    isInteractive = true;
                } else if (window.getComputedStyle(node).cursor === 'pointer') {
                    isInteractive = true;
                }

                if (isInteractive && isVisible(node)) {
                    idCounter++;
                    const rect = node.getBoundingClientRect();
                    
                    // Inject the agent ID for physical cross-referencing
                    node.setAttribute('data-agent-id', idCounter);

                    items.push({
                        elementId: idCounter,
                        tagName: node.tagName.toLowerCase(),
                        text: getSemanticLabel(node, currentRoot),
                        type: node.getAttribute('type') || "",
                        role: node.getAttribute('role') || "",
                        testId: node.getAttribute('data-testid') || node.getAttribute('data-test') || "",
                        attributes: {
                            id: node.id || "",
                            name: node.getAttribute('name') || "",
                            class: node.className || "",
                            href: node.getAttribute('href') || "",
                            placeholder: node.getAttribute('placeholder') || "",
                            title: node.getAttribute('title') || "",
                            src: node.getAttribute('src') || ""
                        },
                        center: { 
                            x: Math.round(rect.left + rect.width / 2), 
                            y: Math.round(rect.top + rect.height / 2) 
                        },
                        rect: {
                            x: Math.round(rect.left),
                            y: Math.round(rect.top),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        }
                    });
                }
            }
        } catch (e) {}

        // 2. Recurse into Shadow DOM if present
        if (node.shadowRoot) {
            try {
                Array.from(node.shadowRoot.children).forEach(child => traverse(child, node.shadowRoot));
            } catch (e) {}
        }

        // 3. Recurse into children
        try {
            if (node.children) {
                Array.from(node.children).forEach(child => traverse(child, currentRoot));
            }
        } catch (e) {}
    }

    traverse(document.body);
    return { elements: items, lastId: idCounter };
}
"""
