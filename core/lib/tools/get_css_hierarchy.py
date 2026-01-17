from .adaptive_tool import AdaptiveTool
from .base_tool import Tool
from playwright.async_api import Page
import random
from termcolor import colored

class GetCssHierarchyTool(AdaptiveTool, Tool):
    """
    Tool for building a unique, reliable CSS selector for a given element or text by 
    traversing its ancestry.
    """
    
    
    def __init__(self):
        AdaptiveTool.__init__(self, "get_css_hierarchy")
        Tool.__init__(self)
        self.name = "get_css_hierarchy"
    
    def get_signature(self) -> dict:
        return {
            "description": "Constructs a unique, robust CSS selector for an element by traversing its DOM hierarchy (parent, ancestor, etc.).",
            "arguments": {
                "text": "The visible text of the element (if targeting by text).",
                "selector": "An initial raw CSS selector or element description to start from.",
                "max_depth": "Maximum levels of ancestry to traverse (default: 5)."
            },
            "example": {
                "text": "Add to Cart",
                "max_depth": 5
            }
        }
    
    async def execute(self, page: Page, text: str = None, selector: str = None, max_depth: int = 5, **kwargs) -> dict:
        print(colored(f"🔍 [GetCssHierarchyTool] Building unique selector for text='{text}' or selector='{selector}'...", "cyan"))
        
        try:
            # Inject a function to find and build the unique hierarchy
            # This logic runs inside the browser context
            unique_selector = await page.evaluate("""
                ({ text, selector, maxDepth }) => {
                    // Helper: Escape CSS special characters
                    const escapeCSS = (str) => {
                         return str.replace(/([!"#$%&'()*+,.\/:;<=>?@[\]^`{|}~])/g, '\\\\$1');
                    };

                    // Helper: Check if a selector is unique in the document
                    const isUnique = (sel) => {
                        return document.querySelectorAll(sel).length === 1;
                    };

                    // Helper: Generate a simple class/id selector for a node
                    const getNodeSelector = (node) => {
                        if (node.id) return '#' + escapeCSS(node.id);
                        if (node.className && typeof node.className === 'string') {
                            const classes = node.className.trim().split(/\s+/).filter(c => c && !c.includes(':')); // Filter out bad classes
                            if (classes.length > 0) return '.' + classes.map(escapeCSS).join('.');
                        }
                        return node.tagName.toLowerCase();
                    };

                    let target = null;
                    if (selector) {
                        try { target = document.querySelector(selector); } catch(e){}
                    }
                    if (!target && text) {
                        // Find by text (approximate XPath -> Element)
                        const xpath = `//*[contains(text(), '${text}')]`;
                        const snapshot = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                        if (snapshot.snapshotLength > 0) {
                             target = snapshot.snapshotItem(0);
                        }
                    }

                    if (!target) return null;

                    // Traversal Logic
                    let current = target;
                    let path = [];
                    for (let i = 0; i < maxDepth; i++) {
                        if (!current || current.tagName === 'BODY' || current.tagName === 'HTML') break;
                        
                        let part = getNodeSelector(current);
                        
                        // Refine part to be specific to siblings if needed
                        const siblings = Array.from(current.parentNode ? current.parentNode.children : []);
                        if (siblings.length > 1) {
                             const sameTag = siblings.filter(s => s.tagName === current.tagName);
                             const index = sameTag.indexOf(current) + 1;
                             if (index > 0 && sameTag.length > 1) {
                                 part += `:nth-of-type(${index})`;
                             }
                        }
                        
                        path.unshift(part);
                        const candidate = path.join(' > ');
                        if (isUnique(candidate)) {
                            return candidate;
                        }
                        
                        current = current.parentNode;
                    }
                    
                    // Fallback to full path if not unique yet
                    return path.join(' > ');
                }
            """, {"text": text, "selector": selector, "maxDepth": max_depth})
            
            if unique_selector:
                print(colored(f"   ✅ Unique Selector Found: {unique_selector}", "green"))
                
                # Highlight to verify visual correctness
                try:
                    await page.locator(unique_selector).first.evaluate("el => { el.style.outline = '3px dashed orange'; }")
                    await asyncio.sleep(0.5)
                except: pass

                return {
                    "status": "success",
                    "output": unique_selector,
                    "generated_selector": unique_selector
                }
            else:
                return {
                    "status": "failure",
                    "error": "Could not generate a unique selector. Element might not be found."
                }

        except Exception as e:
            return {
                "status": "failure",
                "error": f"Hierarchy generation failed: {str(e)}"
            }
