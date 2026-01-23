import asyncio
import json
import os
import sys
import argparse
from datetime import datetime
from termcolor import colored
from typing import Dict, Any, List, Set, Tuple
from playwright.async_api import async_playwright, Page, BrowserContext

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    pass

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.lib.llm_utils import SafeLLM, try_parse_json

class DiscoveryAgent:
    """
    Crawls a website (BFS) using PARALLEL tab workers to build a semantic sitemap faster.
    """
    def __init__(self, project_dir: str, headed: bool = False, concurrency: int = 3):
        self.project_dir = os.path.abspath(project_dir)
        self.sitemap_path = os.path.join(self.project_dir, "sitemap.json")
        
        # Ensure project directory exists
        os.makedirs(self.project_dir, exist_ok=True)
        
        self.headed = headed
        self.concurrency = concurrency
        self.visited_urls: Set[str] = set()
        self.sitemap: List[Dict] = []
        
        self.llm = SafeLLM(
            model=None,
            temperature=0.0,
            model_kwargs={"response_mime_type": "application/json"}
        )

    def log(self, msg: str, color: str = None):
        if color:
            print(colored(msg, color), flush=True)
        else:
            print(msg, flush=True)

    async def run(self, base_url: str, max_depth: int = 2, max_pages: int = 20, deep: bool = False):
        if deep:
            max_depth = 3
            max_pages = 50
            self.log("🚀 [DEEP] Extensive mapping enabled (Depth: 3, Pages: 50)", "yellow")
        
        self.log(f"\n🗺️ [DISCOVERY] Starting Parallel Semantic Crawl on {base_url} (Workers: {self.concurrency})", "blue")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not self.headed)
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            
            queue = asyncio.Queue()
            queue.put_nowait((base_url, 0))
            self.visited_urls.add(base_url)
            
            processed_count = 0
            
            async def worker(worker_id: int):
                nonlocal processed_count
                while True:
                    try:
                        # Wait for a task
                        try:
                            item = await queue.get()
                        except asyncio.CancelledError:
                            return

                        current_url, depth = item
                        
                        # Stop if limits reached (but consume queue to avoid blocks if using join?)
                        # actually queue.join just waits for task_done.
                        if processed_count >= max_pages:
                             queue.task_done()
                             continue
                             
                        if depth > max_depth:
                            queue.task_done()
                            continue

                        self.log(f"  🔍 [Worker {worker_id}] Visiting ({depth}): {current_url}", "cyan")
                        
                        page = await context.new_page()
                        try:
                            await page.goto(current_url, wait_until="domcontentloaded", timeout=15000)
                            
                            summary_task = self._summarize_page(page)
                            links_task = self._extract_links(page, base_url)
                            summary, links = await asyncio.gather(summary_task, links_task)
                            
                            if processed_count < max_pages:
                                # summary is now a Dict with structured data
                                self.sitemap.append({
                                    "url": current_url,
                                    "title": await page.title(),
                                    **summary  # Unpack all structured fields
                                })
                                processed_count += 1
                            
                            if depth < max_depth:
                                for link in links:
                                    if link not in self.visited_urls:
                                        self.visited_urls.add(link)
                                        queue.put_nowait((link, depth + 1))
                                        
                        except Exception as e:
                            self.log(f"    ❌ [Worker {worker_id}] Failed {current_url}: {e}", "red")
                        finally:
                            await page.close()
                            queue.task_done()
                            
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        self.log(f"Worker crashed: {e}", "red")
                        # Ensure we don't block join on crash
                        try: queue.task_done()
                        except: pass
            
            # Start workers
            workers = [asyncio.create_task(worker(i)) for i in range(self.concurrency)]
            
            # Wait for all tasks to be completed
            # This handles the race condition perfectly: browser won't close until queue is fully drained and processed
            await queue.join()
            
            # Cancel workers
            for w in workers: w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
            
            await browser.close()
            
            with open(self.sitemap_path, 'w', encoding='utf-8') as f:
                json.dump(self.sitemap, f, indent=2)
                
            self.log(f"✅ Discovery Complete. Mapped {len(self.sitemap)} pages.", "green")

    async def _extract_links(self, page: Page, base_domain: str) -> List[str]:
        """Extracts unique internal links."""
        try:
            links = await page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('a[href]'))
                        .map(a => a.href)
                        .filter(href => href.startsWith('http')) 
                }
            """)
            
            from urllib.parse import urlparse
            base_netloc = urlparse(base_domain).netloc.replace("www.", "")
            
            internal_links = []
            for link in links:
                clean_link = link.split('#')[0].rstrip('/')
                parsed = urlparse(clean_link)
                if base_netloc in parsed.netloc:
                    if not any(clean_link.endswith(ext) for ext in ['.jpg', '.png', '.pdf', '.css', '.js']):
                         internal_links.append(clean_link)
            return list(set(internal_links))
        except:
            return []

    async def _summarize_page(self, page: Page) -> Dict:
        """Enhanced structured page analysis for rich test generation."""
        try:
            # Run all analysis in parallel for speed
            (page_type, raw_elements, forms, business_rules, relationships, summary_text) = await asyncio.gather(
                self._classify_page_type(page),
                self._extract_interactive_elements(page),
                self._extract_forms(page),
                self._detect_business_rules(page),
                self._map_page_relationships(page),
                self._get_text_summary(page),
                return_exceptions=True
            )
            
            # Semantic Filtering: Use LLM to verify if elements make sense for this page type
            validated_elements = raw_elements
            if not isinstance(page_type, Exception) and not isinstance(raw_elements, Exception):
                self.log(f"    🧠 Semantically validating {len(raw_elements.get('buttons', []))} buttons for {page_type} page...", "yellow")
                validated_elements = await self._semantically_filter_elements(page_type, raw_elements, summary_text)
            
            # Handle any failures gracefully
            return {
                "page_type": page_type if not isinstance(page_type, Exception) else "unknown",
                "elements": validated_elements,
                "forms": forms if not isinstance(forms, Exception) else [],
                "business_rules": business_rules if not isinstance(business_rules, Exception) else {},
                "relationships": relationships if not isinstance(relationships, Exception) else {},
                "summary": summary_text if not isinstance(summary_text, Exception) else "Analysis error"
            }
        except Exception as e:
            self.log(f"    ⚠️ Page analysis failed: {e}", "yellow")
            return {
                "page_type": "unknown",
                "elements": {},
                "forms": [],
                "business_rules": {},
                "relationships": {},
                "summary": "Analysis error"
            }
    
    async def _get_text_summary(self, page: Page) -> str:
        """Original text summary for backward compatibility."""
        try:
            title = await page.title()
            text_content = await page.evaluate("document.body.innerText.substring(0, 2000)")
            
            prompt = f"""
            Summarize functional purpose: {title}
            Content: {text_content[:500]}...
            Format: JSON {{ "summary": "..." }}
            """
            
            resp = await self.llm.ainvoke(prompt)
            data = try_parse_json(resp)
            return data.get("summary", "Unknown") if data else "Unknown"
        except:
            return "Analysis error"
    
    async def _classify_page_type(self, page: Page) -> str:
        """Classify page type using DOM patterns + heuristics."""
        try:
            url = page.url.lower()
            title = (await page.title()).lower()
            
            # Fast heuristic classification
            if any(x in url for x in ["product_details", "/product/", "/p/", "/item/"]):
                return "product_detail"
            elif any(x in url for x in ["/products", "/shop", "/catalog", "/category"]):
                return "product_list"
            elif any(x in url for x in ["/cart", "/basket", "/bag"]):
                return "cart"
            elif any(x in url for x in ["/checkout", "/payment"]):
                return "checkout"
            elif any(x in url for x in ["/login", "/signin", "/signup", "/register", "/account"]):
                return "login"
            elif "contact" in url or "contact" in title:
                return "contact_form"
            elif url.rstrip("/").endswith(page.url.split("//")[1].split("/")[0]) or "home" in url:
                return "homepage"
            
            # DOM-based detection for ambiguous cases
            dom_indicators = await page.evaluate("""
                () => {
                    return {
                        hasProductGrid: !!document.querySelector('.product, .item, [data-product], .product-card'),
                        hasAddToCart: !!document.querySelector('[data-product-id], button:contains("Add to Cart"), .add-to-cart'),
                        hasCheckoutButton: !!document.querySelector('button:contains("Checkout"), a[href*="checkout"]'),
                        hasLoginForm: !!document.querySelector('input[type="password"]'),
                        hasContactForm: !!(document.querySelector('textarea') && document.querySelector('input[type="email"]'))
                    };
                }
            """)
            
            # Classify based on DOM indicators
            if dom_indicators.get("hasLoginForm"):
                return "login"
            elif dom_indicators.get("hasContactForm"):
                return "contact_form"
            elif dom_indicators.get("hasAddToCart") and not dom_indicators.get("hasProductGrid"):
                return "product_detail"
            elif dom_indicators.get("hasProductGrid"):
                return "product_list"
            elif dom_indicators.get("hasCheckoutButton"):
                return "cart"
            
            return "other"
        except:
            return "unknown"
    
    async def _extract_interactive_elements(self, page: Page) -> Dict:
        """Extract all interactive elements with metadata."""
        try:
            elements = await page.evaluate("""
                () => {
                    const result = {
                        buttons: [],
                        inputs: [],
                        dropdowns: [],
                        links: []
                    };
                    
                    // Buttons
                    document.querySelectorAll('button, input[type="button"], input[type="submit"], a.btn, .button').forEach(btn => {
                        const text = (btn.textContent || btn.value || '').trim();
                        // VISIBILITY CHECK: Only include if element is actually visible to user
                        const isVisible = !!(btn.offsetWidth || btn.offsetHeight || btn.getClientRects().length);
                        
                        if (isVisible && text && text.length < 50 && text.length > 0) {
                            const item = {text: text};
                            if (btn.id) item.selector = '#' + btn.id;
                            else if (btn.className) item.selector = '.' + btn.className.split(' ')[0];
                            
                            // Collect data attributes
                            Array.from(btn.attributes).forEach(attr => {
                                if (attr.name.startsWith('data-')) {
                                    item[attr.name] = attr.value;
                                }
                            });
                            result.buttons.push(item);
                        }
                    });
                    
                    // Inputs
                    document.querySelectorAll('input:not([type="hidden"]), textarea').forEach(input => {
                        const isVisible = !!(input.offsetWidth || input.offsetHeight || input.getClientRects().length);
                        if (isVisible && input.type !== 'submit' && input.type !== 'button') {
                            result.inputs.push({
                                name: input.name || input.id || input.placeholder,
                                type: input.type || 'text',
                                placeholder: input.placeholder,
                                required: input.required
                            });
                        }
                    });
                    
                    // Dropdowns
                    document.querySelectorAll('select').forEach(select => {
                        const options = Array.from(select.options).map(o => o.text.trim()).filter(t => t);
                        if (options.length > 0) {
                            result.dropdowns.push({
                                name: select.name || select.id,
                                options: options.slice(0, 10),  // Limit to 10 options
                                required: select.required
                            });
                        }
                    });
                    
                    // Important links (limit to visible, meaningful ones)
                    const linkTexts = new Set();
                    document.querySelectorAll('a[href]:not(.hidden)').forEach(link => {
                        const text = link.textContent?.trim();
                        if (text && text.length < 50 && text.length > 0 && !linkTexts.has(text)) {
                            linkTexts.add(text);
                            if (result.links.length < 20) {  // Limit to 20 unique links
                                result.links.push({
                                    text: text,
                                    href: link.getAttribute('href')
                                });
                            }
                        }
                    });
                    
                    return result;
                }
            """)
            return elements
        except:
            return {"buttons": [], "inputs": [], "dropdowns": [], "links": []}
    
    async def _extract_forms(self, page: Page) -> List[Dict]:
        """Extract all forms with field metadata."""
        try:
            forms = await page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('form')).map((form, idx) => {
                        const fields = [];
                        Array.from(form.elements).forEach(field => {
                            if (field.tagName !== 'BUTTON' && field.type !== 'submit') {
                                fields.push({
                                    name: field.name || field.id,
                                    type: field.type,
                                    label: field.labels?.[0]?.textContent?.trim(),
                                    placeholder: field.placeholder,
                                    required: field.required
                                });
                            }
                        });
                        
                        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                        
                        return {
                            id: form.id || `form_${idx}`,
                            action: form.action,
                            method: form.method || 'GET',
                            fields: fields,
                            submitText: submitBtn?.textContent?.trim() || submitBtn?.value || 'Submit'
                        };
                    });
                }
            """)
            return forms
        except:
            return []
    
    async def _detect_business_rules(self, page: Page) -> Dict:
        """Detect business logic rules."""
        try:
            rules = await page.evaluate("""
                () => {
                    const bodyText = document.body.textContent || '';
                    return {
                        requires_login: !!(
                            document.querySelector('a[href*="login"], .login-required') ||
                            bodyText.includes('Please log in') ||
                            bodyText.includes('Sign in to continue')
                        ),
                        has_captcha: !!document.querySelector('.g-recaptcha, [data-captcha]'),
                        has_variants: !!document.querySelector('select[name*="size"], select[name*="color"], .variant-selector'),
                        has_quantity: !!document.querySelector('input[name*="quantity"], input[type="number"]')
                    };
                }
            """)
            
            # Get quantity limits if exists
            if rules.get("has_quantity"):
                qty_el = await page.query_selector('input[name*="quantity"], input[type="number"]')
                if qty_el:
                    rules["quantity_limits"] = {
                        "min": await qty_el.get_attribute("min") or "1",
                        "max": await qty_el.get_attribute("max") or "999"
                    }
            
            return rules
        except:
            return {}
    
    async def _semantically_filter_elements(self, page_type: str, elements: Dict, summary: str) -> Dict:
        """Filters out ghost or irrelevant elements using LLM semantic analysis."""
        try:
            prompt = f"""
            Analyze these discovered interactive elements for a {page_type} page.
            Page Summary: {summary}
            
            RAW ELEMENTS:
            {json.dumps(elements, indent=2)}
            
            TASK:
            1. Filter out "ghost" elements or items that seem like part of a hidden template (e.g., repeating buttons that aren't actually on screen).
            2. Remove elements that are irrelevant to the primary functional purpose of this page.
            3. Return the sanitized version of the JSON elements.
            
            Format: JSON only.
            """
            
            resp = await self.llm.ainvoke(prompt)
            sanitized = try_parse_json(resp)
            return sanitized if sanitized else elements
        except:
            return elements

    async def _map_page_relationships(self, page: Page) -> Dict:
        """Map page relationships and flow position."""
        try:
            relationships = await page.evaluate("""
                () => {
                    const result = {parent: null, children: []};
                    
                    // Detect breadcrumbs
                    const breadcrumb = document.querySelector('.breadcrumb, [aria-label*="breadcrumb" i], .breadcrumbs');
                    if (breadcrumb) {
                        const crumbs = Array.from(breadcrumb.querySelectorAll('a, span')).map(el => ({
                            text: el.textContent?.trim(),
                            href: el.href || null
                        })).filter(c => c.text);
                        
                        if (crumbs.length > 1) {
                            result.parent = crumbs[crumbs.length - 2];
                            result.flow_position = `step ${crumbs.length}`;
                        }
                    }
                    
                    // Detect next steps from prominent CTAs
                    const ctas = Array.from(document.querySelectorAll('button, a.btn, .cta, [class*="button"]'))
                        .map(btn => ({
                            text: btn.textContent?.trim(),
                            href: btn.href || null
                        }))
                        .filter(a => a.text && a.text.length < 50)
                        .slice(0, 5);  // Top 5
                    
                    result.children = ctas;
                    return result;
                }
            """)
            return relationships
        except:
            return {}

async def main():
    parser = argparse.ArgumentParser(description="Discovery Agent")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--url", required=True, help="Start URL")
    parser.add_argument("--deep", action="store_true", help="Enable deep extensive mapping")
    
    args = parser.parse_args()
    
    # Default to 3 workers for speed
    agent = DiscoveryAgent(args.project, concurrency=3)
    await agent.run(args.url, deep=args.deep)

if __name__ == "__main__":
    asyncio.run(main())
