import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "models/gemini-flash-latest",
    "models/gemini-pro-latest"
]

print("🧪 Testing Models...")

for m in models_to_test:
    try:
        model = genai.GenerativeModel(m)
        resp = model.generate_content("Hello")
        print(f"✅ Success with {m}")
    except Exception:
        continue
