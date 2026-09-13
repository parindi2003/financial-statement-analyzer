#  AI-Powered Financial Statement Analyst Agent

An AI agent that analyzes financial statements — Pandas calculates the ratios, AI explains them in plain language.

#  What it does

Upload a company's financial statement (CSV/Excel with revenue, expenses, assets, liabilities), then ask questions like *"Is this company financially healthy?"* in natural language. The system automatically calculates financial ratios and uses AI to explain them in a way anyone can understand.

#  Architecture — Hybrid Approach

This project uses a **hybrid deterministic + AI architecture**:

## 🧮 Part A: Calculation Engine — Complete ✅

The calculation engine (`backend/calculations.py`) does the following:

1. **Loads raw financial data** from a CSV file structured in "long format" (`Year, Line_Item, Category, Amount` — one row per line item per year).
2. **Pivots the data** into a "wide format" (one row per year, one column per line item) using `pandas.pivot_table()`, so ratio formulas can reference values directly (e.g. `row["Revenue"]`).
3. **Calculates 8 core financial ratios** using standard, auditable formulas, returned together as a dictionary for a given year:

   | Ratio | Formula |
   |---|---|
   | Gross Profit Margin | (Revenue − COGS) / Revenue |
   | Operating Margin | Operating Income / Revenue |
   | Net Profit Margin | Net Profit / Revenue |
   | Return on Assets (ROA) | Net Profit / Total Assets |
   | Return on Equity (ROE) | Net Profit / Shareholders Equity |
   | Debt-to-Equity Ratio | Total Liabilities / Shareholders Equity |
   | Current Ratio | Current Assets / Current Liabilities |
   | Quick Ratio | (Current Assets − Inventory) / Current Liabilities |

Every ratio was manually cross-checked against hand-calculated values before being trusted in the pipeline — for example, 2023 Net Profit Margin was verified at 9.74% (487,000 / 5,000,000 × 100), matching the engine's output exactly.

This engine deliberately contains **zero AI logic** — every number is produced by deterministic Python/Pandas arithmetic, which is the foundation the AI explanation layer (Part B) will build on top of.

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

## 🚧 Project Status

- [x] Project setup, Git & GitHub configured
- [x] Part A: Calculation engine — **complete**
  - [x] CSV loading with Pandas
  - [x] Data pivoting (long format → wide format)
  - [x] All 8 core financial ratios implemented & verified
- [ ] AI reasoning layer (Part B) — Gemini API integration
- [ ] Backend API (FastAPI endpoints)
- [ ] Frontend (React) — file upload + chat interface
- [ ] End-to-end testing with real company data

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