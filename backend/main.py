from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from calculations import load_financials, pivot_by_year, calculate_ratios, get_verdict
from ai_service import explain_ratios, answer_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    year: int
    question: str
@app.get("/")
def home():
    return {"message": "Financial Statement Analysis API is running!"}

from calculations import load_financials,pivot_by_year,calculate_ratios
from ai_service import explain_ratios

@app.get("/analyze")
def analyze(year: int = 2023):
    data = load_financials("../data/sample_financials.csv")
    wide = pivot_by_year(data)
    ratios = calculate_ratios(wide, year)
    verdict = get_verdict(ratios)
    explanation = explain_ratios(ratios, year)

    return {
        "year": year,
        "ratios": ratios,
        "verdict": verdict,
        "ai_explanation": explanation
    }

@app.post("/ask")
def ask(request: QuestionRequest):
    data = load_financials("../data/sample_financials.csv")
    wide = pivot_by_year(data)
    ratios = calculate_ratios(wide, request.year)
    answer = answer_question(ratios, request.year, request.question)

    return {"answer": answer}