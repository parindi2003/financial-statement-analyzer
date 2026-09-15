from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Financial Statement Analysis API is running!"}

from calculations import load_financials,pivot_by_year,calculate_ratios
from ai_service import explain_ratios

@app.get("/analyze")
def analyze(year:int = 2023):
    data = load_financials("../data/sample_financials.csv")
    wide = pivot_by_year(data)
    ratios = calculate_ratios(wide,year)
    explanation = explain_ratios(ratios, year)

    return{
        "year":year,
        "ratios":ratios,
        "ai_explanation": explanation
    }
