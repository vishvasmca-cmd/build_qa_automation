"""
Pre-tested Playwright Helper Functions
These are validated once and reused across all tests.
"""
import os
import sys
from playwright.sync_api import Page

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def wait_for_stability(page):
    """Ensures page is stable before interaction"""
    try:
        page.wait_for_load_state('domcontentloaded', timeout=5000)
        page.wait_for_load_state('networkidle', timeout=3000)
    except:
        pass
    # Check for blocking overlays
    page.evaluate("""() => {
        const overlays = document.querySelectorAll('.modal.show, .modal-backdrop.show, .overlay, [role="dialog"]');
        overlays.forEach(el => {
            if (window.getComputedStyle(el).display !== 'none') {
                console.log('Found overlay, waiting/hiding:', el);
                // el.style.display = 'none'; // Optional: Aggressively hide if needed
            }
        });
    }""")


def smart_action(page, primary_locator, action_type, value=None):
    """Robust, Self-Healing Action Wrapper"""
    wait_for_stability(page)
    loc = None
    
    print(f"🤖 Executing {action_type} on: {primary_locator}")
    
    try:
        # 1. Parsing Locator
        if isinstance(primary_locator, str):
            if primary_locator.startswith("page."):
                # Direct Playwright call (e.g. page.get_by_role(...))
                # We still need to evaluate this safely.
                safe_vars = {'page': page, 're': __import__('re')}
                try:
                    loc = eval(primary_locator, safe_vars)
                except Exception as e:
                    print(f"⚠️ Eval failed for {primary_locator}: {e}")
                    loc = page.locator(primary_locator)
            else:
                loc = page.locator(primary_locator)
        else:
            loc = primary_locator # Already a locator object

        # 2. Execution with Retries/Fallbacks
        def _perform_action(l):
            if action_type == 'click':
                l.click(timeout=10000)
            elif action_type == 'fill':
                l.fill(str(value), timeout=10000)
            elif action_type == 'select':
                l.select_option(str(value), timeout=10000)
            return True

        try:
            _perform_action(loc)
        except Exception as e:
            msg = str(e).lower()
            if "strict mode violation" in msg:
                print(f"⚠️ Strict mode violation. Falling back to .first")
                _perform_action(loc.first)
            elif "not visible" in msg or "not stable" in msg:
                print(f"⚠️ Visibility/Stability issue. Forcing action.")
                if action_type == 'click':
                    loc.click(force=True, timeout=5000)
                else:
                    _perform_action(loc)
            else:
                raise e
        
        return True

    except Exception as e:
        print(f"🚑 Healing triggered for: {primary_locator} (Reason: {str(e)[:100]})")
        
        # 3. Self-Healing Fallback
        try:
            # First, try to clear any blocking overlays that might have appeared
            print("   🚑 Clearing blocking overlays...")
            page.evaluate("""() => {
                const selectors = '[class*="overlay"], [class*="modal"], [role="dialog"], [aria-modal="true"]';
                document.querySelectorAll(selectors).forEach(el => {
                    const style = window.getComputedStyle(el);
                    if (style.position === 'fixed' || style.position === 'absolute') {
                        el.remove();
                    }
                });
            }""")
            
            # Extract keyword for fuzzy matching
            import re
            keyword = ""
            match = re.search(r"['\"](.*?)['\"]", str(primary_locator))
            if match:
                keyword = match.group(1).lower()

            if keyword:
                print(f"🔍 Searching for fallback with keyword: '{keyword}'")
                # Try common roles
                for role in ['button', 'link', 'checkbox', 'menuitem']:
                    healed = page.get_by_role(role, name=re.compile(keyword, re.IGNORECASE))
                    if healed.count() > 0:
                        print(f"✨ Healed via Role({role}) match!")
                        _perform_action(healed.first)
                        return True
                
                # Try direct text match
                healed = page.get_by_text(re.compile(keyword, re.IGNORECASE))
                if healed.count() > 0:
                    print("✨ Healed via direct text match!")
                    _perform_action(healed.first)
                    return True
                
                # Try labels/placeholders
                for method in ['get_by_label', 'get_by_placeholder']:
                    try:
                        healed = getattr(page, method)(re.compile(keyword, re.IGNORECASE))
                        if healed.count() > 0:
                            print(f"✨ Healed via {method} match!")
                            _perform_action(healed.first)
                            return True
                    except: pass

            # Coordinate Fallback (Last Resort for clicks)
            if action_type == 'click' and loc:
                try:
                    box = loc.bounding_box()
                    if box:
                        print("🎯 Using coordinate-based click fallback.")
                        page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
                        return True
                except: pass
        except Exception as heal_error:
            print(f"❌ Healing failed: {heal_error}")
        
        print(f"❌ Final failure for action '{action_type}' on '{primary_locator}'")
        raise e

def take_screenshot(page, name, project_name):
    """Consistent screenshot utility"""
    path = os.path.join(f'projects/{project_name}/outputs/screenshots', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        page.screenshot(path=path)
        # Using ASCII-safe print to avoid Windows encoding issues
        print(f'[SCREENSHOT] Saved: {path}')
    except Exception as e:
        # Using ASCII-safe print to avoid Windows encoding issues
        print(f'[WARNING] Screenshot failed: {str(e)}')
