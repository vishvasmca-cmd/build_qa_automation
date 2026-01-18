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
            model="gemini-2.0-flash",
            temperature=0.0,
            model_kwargs={"response_mime_type": "application/json"}
        )

    def log(self, msg: str, color: str = None):
        if color:
            print(colored(msg, color), flush=True)
        else:
            print(msg, flush=True)

    async def run(self, base_url: str, max_depth: int = 2, max_pages: int = 20):
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
                                self.sitemap.append({
                                    "url": current_url,
                                    "title": await page.title(),
                                    "summary": summary
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

    async def _summarize_page(self, page: Page) -> str:
        """Uses LLM to summarize page capability."""
        try:
            title = await page.title()
            text_content = await page.evaluate("document.body.innerText.substring(0, 2000)")
            
            prompt = f"""
            Summarize functional purpose: {title}
            Content: {text_content[:500]}...
            Format: JSON {{ "summary": "..." }}
            """
            
            # Reduced context for speed
            resp = await self.llm.ainvoke(prompt)
            data = try_parse_json(resp)
            return data.get("summary", "Unknown") if data else "Unknown"
        except:
            return "Analysis error"

async def main():
    parser = argparse.ArgumentParser(description="Discovery Agent")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--url", required=True, help="Start URL")
    
    args = parser.parse_args()
    
    # Default to 3 workers for speed
    agent = DiscoveryAgent(args.project, concurrency=3)
    await agent.run(args.url)

if __name__ == "__main__":
    asyncio.run(main())
