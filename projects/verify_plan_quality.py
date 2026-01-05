import sys
import os

# Adjust path to find core/
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.spec_synthesizer import SpecSynthesizer

def verify_full_plan_generation():
    print("📋 Generating Strategic Plan for Demoblaze...")
    project_dir = os.path.join(os.getcwd(), 'projects/https___www_demoblaze_com__regression')
    os.makedirs(project_dir, exist_ok=True)
    
    syn = SpecSynthesizer(project_dir)
    url = "https://www.demoblaze.com"
    
    plan = syn.generate_master_plan(
        url=url,
        testing_type="regression",
        goal="Verify the checkout flow and product catalog."
    )
    
    if plan:
        print("\n✅ Plan Generated Successfully!")
        print("-" * 40)
        # Check for keywords from the e-commerce playbook
        if "Authentication" in plan and "Cart" in plan and "Checkout" in plan:
            print("🚀 SUCCESS: Plan contains E-commerce modules.")
        else:
            print("⚠️ WARNING: Some modules might be missing.")
            
        if "Smoke" in plan and "Regression" in plan:
             print("🚀 SUCCESS: Plan distinguishes between Smoke and Regression.")
        
        # Save excerpt to verify
        print("\n--- Plan Excerpt ---")
        print("\n".join(plan.split('\n')[:20]))
    else:
        print("❌ FAILED to generate plan.")

if __name__ == "__main__":
    verify_full_plan_generation()
