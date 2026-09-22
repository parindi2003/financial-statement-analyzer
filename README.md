#  AI-Powered Financial Statement Analyst Agent

An AI agent that analyzes financial statements — Pandas calculates the ratios, AI explains them in plain language.

#  What it does

Upload a company's financial statement (CSV/Excel with revenue, expenses, assets, liabilities), then ask questions like *"Is this company financially healthy?"* in natural language. The system automatically calculates financial ratios and uses AI to explain them in a way anyone can understand.

#  Architecture — Hybrid Approach

This project uses a **hybrid deterministic + AI architecture**:

##  Part A: Calculation Engine — Complete ✅

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

##  Part B: AI Reasoning Layer — In Progress

This layer uses the **Google Gemini API** to turn the numbers from Part A into plain-language explanations. Critically, the AI is never given raw, unverified data — it only receives ratios that have already been calculated and verified deterministically. The prompt explicitly instructs the model not to recalculate or question the numbers, only to interpret them.

**How it works:**
1. Part A produces a dictionary of verified ratios (e.g. `{"Net Profit Margin (%)": 9.74, ...}`)
2. This dictionary is inserted into a structured prompt template
3. The prompt is sent to Gemini, which returns a short, human-readable analysis covering profitability, financial health, and any notable strengths or concerns

This keeps the system's core guarantee intact: **numbers come from Pandas, meaning comes from AI** — never the other way around.

##  Integration Milestone: Full Pipeline Working

The system now runs end-to-end from the command line:

CSV file → load_financials() → pivot_by_year() → calculate_ratios()
↓
(real, verified numbers)
↓
explain_ratios()
↓
Plain-language AI analysis


**Example output** (using the sample dataset, 2023 data):

> Calculated ratios: Net Profit Margin 9.74%, ROE 20.55%, Debt-to-Equity 0.92, Current Ratio 2.57
>
> AI explanation: *"Yes, the company is highly profitable, keeping nearly 10% of its revenue as pure profit and delivering a strong 20.55% return on shareholder investment. It is also in excellent financial health, maintaining a manageable debt level and strong liquidity..."*

This confirms the system's central design goal: **every number shown to the user is 100% deterministic and verifiable (Pandas), while the interpretation is handled by AI** — with no risk of the AI inventing or miscalculating a figure.

 ##  Backend API (FastAPI)

The system is now exposed as a web API using **FastAPI**, making it accessible over HTTP rather than only through the command line. This is the layer the React frontend will connect to.

**Endpoint implemented:**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check — confirms the API is running |
| GET | `/analyze?year=2023` | Runs the full pipeline (CSV → ratios → AI explanation) for a given year and returns the result as JSON |

**Example response from `/analyze`:**

```json
{
  "year": 2023,
  "ratios": {
    "Gross Profit Margin (%)": 40.0,
    "Net Profit Margin (%)": 9.74,
    "Return on Equity - ROE (%)": 20.55,
    "...": "..."
  },
  "ai_explanation": "Yes, the company is highly profitable, keeping nearly 10% of its revenue as pure profit..."
}
```

This confirms the backend can now serve both the deterministic financial data and the AI-generated interpretation through a single, structured API call — exactly what a frontend needs to consume and display.

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

##  Frontend (React) — In Progress

The frontend is built as a **3-screen user flow**: Welcome → Analyzing → Results. It communicates with the FastAPI backend over HTTP.

### Design Direction

A clean, ledger-inspired aesthetic — warm paper-white backgrounds, serif headings, monospace numbers, and a muted teal/amber accent palette — chosen to feel trustworthy and financial rather than like a generic SaaS dashboard.

### Screen 1: Welcome Screen —  Complete

- Introduces the app in one sentence
- Lets the user upload their own CSV, or click "Try with sample company data" for an instant demo
- Displays a clear error message if the backend request fails (e.g. server not running)

### Screen 2: Analyzing (Loading State) —  Complete

Shown while the request to the backend is in flight (the pipeline includes a live AI API call, so this can take a few seconds).

### Screen 3: Results Screen —  Basic version working

- **Full pipeline connected end-to-end**: clicking "Try sample data" triggers a real request to the FastAPI `/analyze` endpoint, and the returned ratios + AI explanation render on screen
- Currently displayed as raw JSON for verification — the next step is turning this into a proper dashboard:
  - Categorized ratio cards (Profitability / Liquidity / Leverage)
  - A rules-based financial health verdict (deterministic Python logic, not AI-generated — consistent with this project's "AI explains, never decides" principle)
  - The AI's plain-language explanation, styled as a highlighted narrative section
  - A follow-up Q&A chat input

### Technical Notes

- **CORS**: the FastAPI backend explicitly allows requests from the React dev server (`http://localhost:5173`) via `CORSMiddleware`, since browsers block cross-origin requests by default
- **State management**: a single `screen` state variable (`"welcome" | "loading" | "results"`) controls which view is rendered, using conditional rendering rather than a routing library — appropriate for this app's simple, linear flow

### Planned Next Steps
1. Build the styled Results dashboard (ratio cards, verdict, AI narrative)
2. Add the rules-based health verdict logic
3. Add follow-up Q&A chat

##  Project Status

- [x] Project setup, Git & GitHub configured
- [x] Part A: Calculation engine — **complete**
  - [x] CSV loading with Pandas
  - [x] Data pivoting (long format → wide format)
  - [x] All 8 core financial ratios implemented & verified
- [x] Part B: AI reasoning layer — **complete**
  - [x] Gemini API connected and authenticated
  - [x] `explain_ratios()` function — converts calculated ratios into a natural-language prompt and returns a plain-English explanation
- [x] Part A + Part B Integration — **complete**
  - [x] Real calculated ratios (not dummy data) are automatically passed to the AI layer
  - [x] End-to-end pipeline verified: CSV → Pandas ratios → AI explanation
- [x] Backend API (FastAPI) — **complete**
  - [x] `/analyze` endpoint — runs the full pipeline and returns ratios + AI explanation as JSON
- [x] **Frontend (React) — in progress** 
  - [x] Project scaffolded with Vite
  - [x] Welcome screen UI — file upload area + "try sample data" option, styled to match a clean, ledger-inspired design
  - [ ] Connect upload/sample button to backend `/analyze` endpoint
  - [ ] Loading state while analysis runs
  - [ ] Results screen — ratios display, AI explanation, verdict, follow-up chat
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