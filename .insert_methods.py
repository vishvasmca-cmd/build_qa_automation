import re

# Read the explorer.py file
with open('core/agents/explorer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the position to insert (right before _verify_goal_completion)
pattern = r'(\s+)(async def _verify_goal_completion\(self,)'
match = re.search(pattern, content)

if not match:
    print("ERROR: Could not find _verify_goal_completion method")
    exit(1)

# Read the methods to insert
with open('.temp_tool_methods.py', 'r', encoding='utf-8') as f:
    methods_to_insert = f.read()

# Insert position is right before the match
insert_pos = match.start()

# Create new content
new_content = content[:insert_pos] + methods_to_insert + "\n" + content[insert_pos:]

# Write back
with open('core/agents/explorer.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: Inserted methods before _verify_goal_completion")
