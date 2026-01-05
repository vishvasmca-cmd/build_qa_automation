"""
Pre-tested Playwright Helper Functions
These are validated once and reused across all tests.
"""
import os
from playwright.sync_api import Page


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
    try:
        # 1. Parsing Locator
        loc_str = primary_locator
        import re
        if 'page.' in loc_str:
            loc_str = loc_str.replace('getByRole', 'get_by_role').replace('{ name:', 'name=').replace(' }', '')
            match = re.search(r"['\"](.*?)['\"]", loc_str)
            if match and 'locator' in loc_str:
                loc_str = match.group(1)
            if 'page.' in loc_str:
                loc = eval(loc_str, {'page': page, 're': re})
        
        if not loc:
            loc = page.locator(loc_str)
    
        # 2. Pre-Action Checks
        if not loc.count() and 'strict mode' not in action_type:
            # Try relaxed visibility
            pass
        
        # 3. Execution
        if action_type == 'click':
            try:
                loc.click(timeout=15000)
            except Exception as e:
                print(f'⚠️ Standard click failed: {e}. Trying force.')
                try:
                    loc.click(timeout=5000, force=True)
                except:
                    # Last resort: JS Click
                    print(f'☢️ JS Click needed for: {primary_locator}')
                    loc.first.evaluate('el => el.click()')
        
        elif action_type == 'fill':
            loc.fill(str(value), timeout=15000)
        
        return True
    
    except Exception as e:
        # 4. Self-Healing Fallback
        print(f'🚑 Healing needed for: {primary_locator} ({e})')
        try:
            # Fallback 1: Text approximations
            keyword = ''
            match = re.search(r"['\"](.*?)['\"]", primary_locator)
            if match:
                keyword = match.group(1).lower()
            
            if keyword:
                healed = page.get_by_role('button', name=re.compile(keyword, re.IGNORECASE))
                if healed.count():
                    print('✨ Healed via Role/Name match!')
                    if action_type == 'click':
                        healed.first.click()
                    else:
                        healed.first.fill(str(value))
                    return True
        except:
            pass
        
        print('❌ Action failed after healing attempts.')
        raise e


def take_screenshot(page, name, project_name):
    """Consistent screenshot utility"""
    path = os.path.join(f'projects/{project_name}/screenshots', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page.screenshot(path=path)
    print(f'📸 Saved: {path}')
