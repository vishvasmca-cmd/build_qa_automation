import os
import sys
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

class CodeReviewer:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)

    def review_and_fix(self, file_path):
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False

        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        print(f"🕵️  Reviewing {os.path.basename(file_path)}...")

        system_prompt = """You are a Principal Software Engineer in Test (SDET) with 15+ years of experience.
Your job is to CODE REVIEW and AUTO-FIX the provided Playwright Python script.

**REVIEW CRITERIA (The "Bar"):**
1.  **No Hardcoded Waits**: Remove `time.sleep()`. Use `expect(...).to_be_visible()` or `wait_for_load_state`.
2.  **Robust Locators**: If you see brittle XPaths (`/div[3]/span[2]`), warn about them (or replace if obvious context exists).
3.  **Assertions**: Code MUST have assertions (`expect(...)`). If missing, add logical ones based on variable names/context.
4.  **Error Handling**: Ensure critical actions are wrapped in try/except or use Safe Actions (like the `smart_action` helper).
5.  **Code Style**: Ensure PEP8 compliance, clean variable names, and proper typing hints where useful.
6.  **Redundancy**: Remove duplicate checks or useless print statements.

**OUTPUT FORMAT**:
You must output a JSON object with this EXACT structure:
{
  "status": "APPROVED" or "FIXED",
  "review_summary": "Brief bullet points of what you fixed or why it's good.",
  "final_code": "The complete, valid Python code (original or fixed)."
}
"""
        
        user_msg = f"""
        Please review this Python Playwright test file:
        
        ```python
        {code_content}
        ```
        """

        try:
            resp = self.llm.invoke([
                ("system", system_prompt),
                ("human", user_msg)
            ])
            
            # Clean response
            clean_resp = resp.content.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_resp)
            
            # Action
            if result["status"] == "FIXED":
                print("⚠️ Code Issues Detected & Fixed:")
                print(result["review_summary"])
                
                # Write back the fixed code
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(result["final_code"])
                print("✅ Applied Fixes to File.")
            else:
                print("✅ Code Approved (No major issues found).")
            
            return True

        except Exception as e:
            print(f"❌ Review Agent Crashed: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py <path_to_test_file>")
        sys.exit(1)
    
    path = sys.argv[1]
    reviewer = CodeReviewer()
    reviewer.review_and_fix(path)
