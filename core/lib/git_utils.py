import subprocess
import os
from termcolor import colored

class GitManager:
    @staticmethod
    def _get_branch():
        try:
            res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
            return res.stdout.strip() or "main"
        except:
            return "main"

    @staticmethod
    def sync():
        branch = GitManager._get_branch()
        print(colored(f"🔄 Git: Fetching and Rebasing on {branch}...", "cyan"))
        try:
            subprocess.run(["git", "fetch", "--all"], capture_output=True, check=True)
            # Use rebase for cleaner history and use -Xtheirs for metadata files like failures.json
            ret = subprocess.run(["git", "pull", "--rebase", "origin", branch, "-Xtheirs"], capture_output=True, text=True)
            if ret.returncode != 0:
                print(colored(f"⚠️ Git Sync Warning: {ret.stderr.strip()}", "yellow"))
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
            res = subprocess.run(["git", "push"], capture_output=True, text=True)
            if res.returncode != 0:
                # If push fails, try one sync and push again (re-sync might be needed)
                if "behind" in res.stderr.lower() or "rejected" in res.stderr.lower():
                    print(colored("🔄 Git: Behind remote. Attempting auto-sync...", "yellow"))
                    GitManager.sync()
                    subprocess.run(["git", "push"], capture_output=True, check=True)
                    print(colored("✅ Git: Changes pushed successfully after sync.", "green"))
                else:
                    raise Exception(res.stderr.strip())
            else:
                print(colored("✅ Git: Changes pushed successfully.", "green"))
        except Exception as e:
            print(colored(f"⚠️ Git Push Failed: {e}", "yellow"))
