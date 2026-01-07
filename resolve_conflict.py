import os

def resolve_json_conflict(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_conflict = False
    for line in lines:
        if line.startswith('<<<<<<<'):
            in_conflict = True
            continue
        if line.startswith('======='):
            continue
        if line.startswith('>>>>>>>'):
            in_conflict = False
            continue
        new_lines.append(line)
        
    # Standardize result: ensure it ends with ] correctly if markers were messy
    content = "".join(new_lines).strip()
    if not content.endswith(']'):
        if content.endswith(','):
            content = content[:-1] + '\n]'
        else:
            content = content + '\n]'
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    resolve_json_conflict(r'c:\Users\vishv\.gemini\antigravity\playground\inner-event\knowledge\failures.json')
