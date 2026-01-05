import json
import os
import glob
import sys

def merge_failures(output_file="knowledge/failures.json", input_patern="failures_tmp/*/failures.json"):
    all_failures = []
    
    # Load existing if any (though usually we start fresh or append to repo version)
    if os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                content = json.load(f)
                if isinstance(content, list):
                    all_failures.extend(content)
        except Exception as e:
            print(f"⚠️ Could not read existing {output_file}: {e}")

    # Find new failure files
    new_files = glob.glob(input_patern, recursive=True)
    print(f"Found {len(new_files)} failure logs to merge.")

    for file_path in new_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_failures.extend(data)
                    print(f"✅ Merged {len(data)} entries from {file_path}")
        except Exception as e:
            print(f"❌ Failed to parse {file_path}: {e}")

    # Write back
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(all_failures, f, indent=2)
        print(f"📝 Wrote {len(all_failures)} total failures to {output_file}")
    except Exception as e:
        print(f"❌ Failed to write merged file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Allow args for paths
    out = sys.argv[1] if len(sys.argv) > 1 else "knowledge/failures.json"
    inp = sys.argv[2] if len(sys.argv) > 2 else "failures_tmp/*/failures.json"
    merge_failures(out, inp)
