import re

def extract_workflow_keywords(workflow_description):
    """
    Extracts relevant keywords from the workflow description.
    Includes quoted strings, common finance/ecommerce terms, and capitalized names.
    """
    if not workflow_description:
        return set()
    
    # 1. Quoted strings (e.g., 'AAPL', 'Dyson')
    quotes = set(re.findall(r"['\"]([^'\"]+)['\"]", workflow_description))
    
    # 2. Clean workflow into words
    clean_text = re.sub(r"[^a-zA-Z0-9\s]", " ", workflow_description)
    words = set(clean_text.split())
    
    # 3. Filter for significant words (longer than 2 chars, not common stop words)
    stop_words = {"the", "and", "for", "with", "this", "that", "from", "into", "onto", "under", "over", "phase", "step", "verify", "click", "navigate"}
    significant_words = {w for w in words if len(w) > 3 and w.lower() not in stop_words}
    
    # 4. Action-related keywords (essential targets)
    action_keywords = {"search", "logo", "menu", "input", "button", "link", "submit", "login", "price", "stock", "chart", "news", "markets", "summary"}
    
    return quotes.union(significant_words).union(action_keywords)

def score_element_relevance(element, keywords):
    """
    Scores an element's relevance (0.0 to 1.0) based on keywords.
    """
    if not keywords:
        return 1.0
        
    score = 0
    text_content = (element.get('text') or "").lower()
    tag_name = (element.get('tagName') or "").lower()
    attributes = element.get('attributes', {})
    attr_string = json_to_string(attributes).lower()
    
    # Priority 1: Direct matches in text (Primary)
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in text_content:
            score += 0.8
        if kw_lower in attr_string:
            score += 0.6
            
    # Priority 2: Interaction-heavy tags (Bonus)
    interaction_tags = {'button', 'a', 'input', 'select', 'textarea'}
    if tag_name in interaction_tags:
        score += 0.2
        
    return min(score, 1.0)

def json_to_string(obj):
    """Simple helper to flatten attributes for searching"""
    if isinstance(obj, dict):
        return " ".join(str(v) for v in obj.values())
    return str(obj)
