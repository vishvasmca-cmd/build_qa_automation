import subprocess
import os
from termcolor import colored

class GitManager:
    @staticmethod
    def sync():
        print(colored("🔄 Git: Fetching and Merging...", "cyan"))
        try:
            subprocess.run(["git", "fetch", "--all"], capture_output=True, check=True)
            # Try to merge, but handle cases where there's no tracking branch or conflicts
            ret = subprocess.run(["git", "merge", "origin/master"], capture_output=True, text=True)
            if ret.returncode != 0:
                print(colored(f"⚠️ Git Merge Warning: {ret.stderr.strip()}", "yellow"))
            else:
                print(colored("✅ Git: Synced with remote.", "green"))
        except Exception as e:
            print(colored(f"⚠️ Git Sync Failed: {e}", "yellow"))

    @staticmethod
    def commit_and_push(message):
        print(colored(f"🚀 Git: Committing changes - {message}", "cyan"))
        try:
            # Add knowledge and projects - the core areas of change
            subprocess.run(["git", "add", "knowledge/", "projects/"], capture_output=True)
            
            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if not status.stdout.strip():
                print(colored("ℹ️ Git: No changes to commit.", "grey"))
                return

            subprocess.run(["git", "commit", "-m", message], capture_output=True, check=True)
            
            print(colored("📤 Git: Pushing to remote...", "cyan"))
            subprocess.run(["git", "push"], capture_output=True, check=True)
            print(colored("✅ Git: Changes pushed successfully.", "green"))
        except Exception as e:
            print(colored(f"⚠️ Git Push Failed: {e}", "yellow"))
