import json
import os
import glob
import sys

def merge_knowledge_banks(input_pattern, output_file):
    """Merges multiple KB/Target JSON files into one."""
    print(f"📦 Merging files matching: {input_pattern}")
    
    files = glob.glob(input_pattern)
    if not files:
        print("⚠️ No files found to merge.")
        return

    merged_data = {}
    
    # KNOWLEDGE BANK MERGE STRATEGY
    # Structure: { "domain": { ... }, "patterns": [...] }
    # We need to merge deep keys.
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check formatting (list vs dict)
                if isinstance(data, list):
                    # It's a list (like training_targets.json or traces)
                    if "items" not in merged_data: merged_data["items"] = []
                    merged_data["items"].extend(data)
                elif isinstance(data, dict):
                    # It's a dict (Knowledge Bank)
                    for key, value in data.items():
                        if key not in merged_data:
                            merged_data[key] = value
                        else:
                            # Conflict Resolution: Deep Merge or Append?
                            # For Knowledge Bank details like specific sites, just update.
                            if isinstance(value, dict):
                                merged_data[key].update(value)
                            elif isinstance(value, list):
                                merged_data[key].extend(value)
                            else:
                                merged_data[key] = value # Overwrite simple values
                                
            print(f"   + Merged: {file_path}")
        except Exception as e:
            print(f"   ❌ Failed to merge {file_path}: {e}")

    # If it was a list merge, unwrap
    if "items" in merged_data and len(merged_data.keys()) == 1:
        final_output = merged_data["items"]
    else:
        final_output = merged_data

    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)
    
    print(f"✅ Successfully created {output_file} with {len(files)} inputs.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_kb.py <glob_pattern> <output_file>")
        sys.exit(1)
        
    merge_knowledge_banks(sys.argv[1], sys.argv[2])
