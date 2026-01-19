import re

# Read the file
with open('core/lib/smart_locator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the escaped quote on line 71
# Replace: \"selector\" with: "selector"
fixed_content = content.replace(r'\"selector\"', '"selector"')

# Write back
with open('core/lib/smart_locator.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Fixed escaped quote in smart_locator.py")
