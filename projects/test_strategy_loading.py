import sys
import os

# Adjust path to find core/
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.strategy_loader import FrameworkStrategyLoader

def test_loader():
    print("🧪 Testing Strategy Loader...")
    loader = FrameworkStrategyLoader()
    
    # 1. Test Domain Detection
    print("\n[Step 1] Domain Detection:")
    url = "https://www.demoblaze.com"
    domain = loader.detect_domain(url)
    print(f"URL: {url} -> Detected: {domain}")
    assert domain == 'ecommerce', "Failed to detect e-commerce domain"
    
    # 2. Test Strategy Loading
    print("\n[Step 2] Loading 'ecommerce' Strategy:")
    context = loader.load_strategy('ecommerce')
    print(f"Context Length: {len(context)} chars")
    
    if "DOMAIN PLAYBOOK: E-COMMERCE" in context:
        print("✅ SUCCESS: E-commerce playbook loaded.")
    else:
        print("❌ FAILURE: E-commerce playbook NOT found in context.")
        print("--- Context Dump ---")
        print(context[:500] + "...")
        
    if "GLOBAL TESTING STRATEGY" in context:
        print("✅ SUCCESS: Global test types loaded.")
    else:
        print("❌ FAILURE: Global test types NOT found.")

if __name__ == "__main__":
    test_loader()
