#  AI-Powered Financial Statement Analyst Agent

An AI agent that analyzes financial statements — Pandas calculates the ratios, AI explains them in plain language.

#  What it does

Upload a company's financial statement (CSV/Excel with revenue, expenses, assets, liabilities), then ask questions like *"Is this company financially healthy?"* in natural language. The system automatically calculates financial ratios and uses AI to explain them in a way anyone can understand.

#  Architecture — Hybrid Approach

This project uses a **hybrid deterministic + AI architecture**:

##  Part A: Calculation Engine — Progress

The calculation engine (`backend/calculations.py`) currently does the following:

1. **Loads raw financial data** from a CSV file structured in "long format" (`Year, Line_Item, Category, Amount` — one row per line item per year).
2. **Pivots the data** into a "wide format" (one row per year, one column per line item) using `pandas.pivot_table()`, so ratio formulas can reference values directly (e.g. `row["Revenue"]`).
3. **Calculates financial ratios** using standard, auditable formulas — currently implemented and manually verified:
   -  **Net Profit Margin** = (Net Profit / Revenue) × 100

Each ratio is cross-checked by hand against the raw numbers before being trusted in the pipeline. For example, with 2023 Revenue = 5,000,000 and Net Profit = 487,000, the engine correctly outputs a 9.74% margin — matching the manual calculation.

**Ratios planned next:** Gross Profit Margin, Operating Margin, Return on Assets (ROA), Return on Equity (ROE), Debt-to-Equity Ratio, Current Ratio, Quick Ratio.


##  Note on Sample Data

The `sample_financials.csv` file is synthetic test data created to verify the calculation logic against known, hand-calculated expected values before testing against real-world financial data. This is standard practice for validating logic in a controlled way before introducing real-world complexity.

### Why this approach?

LLMs can hallucinate numbers. In financial data, a wrong number presented confidently is a serious risk. By separating calculation (Pandas) from explanation (AI), this system guarantees the numbers are always correct, while still getting the benefit of natural-language interpretation.

##  Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Calculation Engine | Pandas, NumPy |
| AI/LLM | Google Gemini API |
| Frontend | React |
| Data | CSV/Excel (no database) |

##  Project Status

This project is being built incrementally. Progress so far:

- [x] Project setup & Git/GitHub configured
- [ ] Calculation engine (Part A)
- [ ] AI reasoning layer (Part B)
- [ ] Backend API (FastAPI)
- [ ] Frontend (React)
- [ ] End-to-end testing

##  Project Structure

```
financial-statement-analyzer/
├── backend/
│   ├── calculations.py      → Pandas ratio calculations (Part A)
│   ├── ai_service.py        → Gemini API integration (Part B)
│   └── main.py               → FastAPI server
├── frontend/                → React app (UI)
├── data/
│   └── sample_financials.csv → Sample dataset for testing
└── README.md
```