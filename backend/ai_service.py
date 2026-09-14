import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API Key loaded successfully!")
    print(f"Key starts with: {api_key[:10]}...")
else:
    print("ERROR: API Key not found. Check your .env file.")

import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.6-flash")
response = model.generate_content("Say hello in short sentence")
print(response.text)