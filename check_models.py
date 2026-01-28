"""
Check available Gemini models with your API key
"""
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ API key not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Available Models:\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display: {model.display_name}")
            print()
except Exception as e:
    print(f"❌ Error: {e}")
