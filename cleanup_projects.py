import os
import shutil

# Keep these working projects
KEEP_PROJECTS = [
    'dyson_final_test_v2',  # Latest successful Dyson headless test
    'sauce_final_test',     # Successful SauceDemo test
    '__pycache__',          # Python cache
    '__init__.py'           # Module init
]

projects_dir = 'projects'
removed_count = 0
kept_count = 0

print("🧹 Cleaning up test projects...")
print(f"📌 Keeping: {', '.join([p for p in KEEP_PROJECTS if p not in ['__pycache__', '__init__.py']])}")
print()

for item in os.listdir(projects_dir):
    item_path = os.path.join(projects_dir, item)
    
    if item in KEEP_PROJECTS:
        kept_count += 1
        print(f"✅ Keeping: {item}")
    else:
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                removed_count += 1
                print(f"🗑️  Removed: {item}")
            elif item != '__init__.py':
                os.remove(item_path)
                removed_count += 1
                print(f"🗑️  Removed: {item}")
        except Exception as e:
            print(f"⚠️  Failed to remove {item}: {e}")

print()
print(f"✅ Cleanup complete!")
print(f"   Kept: {kept_count} projects")
print(f"   Removed: {removed_count} projects")
