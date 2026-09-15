import os
from dotenv import load_dotenv
from calculations import load_financials,pivot_by_year,calculate_ratios


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
def explain_ratios(ratios_dict, year):
    """
    Calculate කරපු financial ratios ටික, Gemini AI ට දීලා,
    plain language explanation එකක් ලබාගන්නවා.
    """
    prompt = f"""
You are a financial analyst assistant. Below are the calculated financial ratios 
for a company for the year {year}. These numbers are already verified and accurate — 
your job is only to explain what they mean in simple, clear language for someone 
without a finance background. Do not recalculate or question the numbers.

Financial Ratios:
{ratios_dict}

Provide a short, clear analysis (3-4 sentences) covering:
1. Is the company profitable?
2. Is the company financially healthy (debt, liquidity)?
3. Any concerns or strengths worth noting?
"""
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    data = load_financials("../data/sample_financials.csv")
    wide = pivot_by_year(data)
    real_ratios = calculate_ratios(wide, 2023)

    print("=== Calculated Ratios (from Part A) ===")
    for key, value in real_ratios.items():
        print(f"{key}: {value}")

    print("\n=== AI Explanation (from Part B) ===")
    explanation = explain_ratios(real_ratios, 2023)
    print(explanation)