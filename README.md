# AI-Powered Financial Statement Analyst Agent

An AI agent that analyzes financial statements — Pandas calculates the ratios, AI explains them in plain language.

## What it does

Upload a company's financial statement (CSV/Excel with revenue, expenses, assets, liabilities), then ask questions like *"Is this company financially healthy?"* in natural language. The system automatically calculates financial ratios and uses AI to explain them in a way anyone can understand.

##  Project Status: Complete

- [x] Project setup, Git & GitHub configured
- [x] Part A: Calculation engine — complete (8 financial ratios, verified)
- [x] Part B: AI reasoning layer — complete (Gemini API integration)
- [x] Part A + Part B Integration — complete (verified end-to-end)
- [x] Backend API (FastAPI) — complete (`/analyze`, `/ask` endpoints)
- [x] Financial health verdict — complete (rules-based, deterministic)
- [x] Frontend (React) — complete (Welcome → Loading → Results screens)
- [x] Follow-up Q&A chat — complete
- [x] End-to-end testing — **passed** 

All core features are implemented, connected, and tested end-to-end: a user can upload (or use sample) financial data, see calculated ratios and a deterministic health verdict, read an AI-generated plain-language explanation, and ask follow-up questions — all grounded in the same verified numbers throughout.

## Architecture — Hybrid Approach

This project uses a **hybrid deterministic + AI architecture**.

### Why this approach?

LLMs can hallucinate numbers. In financial data, a wrong number presented confidently is a serious risk. By separating calculation (Pandas) from explanation (AI), this system guarantees the numbers are always correct, while still getting the benefit of natural-language interpretation.

## Part A: Calculation Engine — Complete

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

This engine deliberately contains **zero AI logic** — every number is produced by deterministic Python/Pandas arithmetic, which is the foundation the AI explanation layer (Part B) builds on top of.

## Part B: AI Reasoning Layer — Complete

This layer uses the **Google Gemini API** to turn the numbers from Part A into plain-language explanations. Critically, the AI is never given raw, unverified data — it only receives ratios that have already been calculated and verified deterministically. The prompt explicitly instructs the model not to recalculate or question the numbers, only to interpret them.

**How it works:**
1. Part A produces a dictionary of verified ratios (e.g. `{"Net Profit Margin (%)": 9.74, ...}`)
2. This dictionary is inserted into a structured prompt template
3. The prompt is sent to Gemini, which returns a short, human-readable analysis covering profitability, financial health, and any notable strengths or concerns

This keeps the system's core guarantee intact: **numbers come from Pandas, meaning comes from AI** — never the other way around.

## Financial Health Verdict — Complete (Rules-Based, Not AI)

Implemented as a deterministic Python function (`get_verdict()` in `calculations.py`):

```python
def get_verdict(ratios):
    net_margin = ratios["Net Profit Margin (%)"]
    debt_to_equity = ratios["Debt-to-Equity Ratio"]
    current_ratio = ratios["Current Ratio"]

    if net_margin > 8 and debt_to_equity < 1.5 and current_ratio > 1.5:
        return "Strong Health"
    elif net_margin > 0 and current_ratio > 1:
        return "Moderate Health"
    else:
        return "Needs Attention"
```

This runs **before** the ratios are sent to Gemini. The `/analyze` endpoint returns `verdict` alongside `ratios` and `ai_explanation`, and the frontend displays it directly from the backend response. Verified against both years in the sample dataset: 2023 (Net Margin 9.74%) returns "Strong Health", while 2022 (Net Margin 7.15%) correctly returns "Moderate Health" — confirming the logic is genuinely dynamic, not hardcoded.

This design choice matters for the same reason the ratio calculations are kept out of the AI's hands: **a verdict is a decision**, and this project's whole premise is that decisions and numbers come from deterministic code, while the AI's role is strictly limited to interpretation.

## Follow-up Q&A Chat — Complete

A chat interface below the results lets the user ask specific questions about the analyzed company (e.g. *"why is the debt ratio manageable?"*). How it works:

- A backend function, `answer_question(ratios_dict, year, question)`, builds a prompt that includes the already-calculated ratios as context and explicitly instructs the AI to answer **using only those numbers** and to say so clearly if a question can't be answered from them — preventing the AI from inventing financial details not present in the verified data
- A `POST /ask` endpoint accepts `{ year, question }` and returns `{ answer }`
- On the frontend, questions and answers are stored in a `chatHistory` array and rendered as chat bubbles, styled distinctly for user vs. AI messages

**Verified working end-to-end.** Example test:

> **Q:** "Why is the debt ratio manageable?"
>
> **A:** "The debt ratio is manageable because the Debt-to-Equity ratio of 0.92 indicates that the company uses less debt than equity to finance its assets. Furthermore, strong liquidity—demonstrated by a Current Ratio of 2.57 and a Quick Ratio of 1.54—ensures ample short-term coverage for financial obligations. Solid profitability, including an Operating Margin of 16.0% and a Net Profit Margin of 9.74%, provides steady earnings support to service its debt load effectively."

Every figure in the answer traces back to a number calculated by `calculations.py` — confirming the AI is grounding its responses in verified data rather than inventing figures.

## Backend API (FastAPI)

The system is exposed as a web API using **FastAPI**, making it accessible over HTTP for the React frontend to consume.

**Endpoints implemented:**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check — confirms the API is running |
| GET | `/analyze?year=2023` | Runs the full pipeline (CSV → ratios → verdict → AI explanation) for a given year and returns the result as JSON |
| POST | `/ask` | Accepts `{ year, question }`, answers the question using the already-calculated ratios as context, returns `{ answer }` |

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
  "verdict": "Strong Health",
  "ai_explanation": "Yes, the company is highly profitable, keeping nearly 10% of its revenue as pure profit..."
}
```

**CORS:** the backend explicitly allows requests from the React dev server (`http://localhost:5173`) via `CORSMiddleware`, since browsers block cross-origin requests by default.

## Frontend (React)

Built as a **3-screen user flow**: Welcome → Analyzing → Results, communicating with the FastAPI backend over HTTP.

### Design Direction

A clean, ledger-inspired aesthetic — warm paper-white backgrounds, serif headings, monospace numbers, and a muted teal/amber accent palette — chosen to feel trustworthy and financial rather than like a generic SaaS dashboard.

### Screen 1: Welcome Screen

- Introduces the app in one sentence
- Lets the user upload their own CSV, or click "Try with sample company data" for an instant demo
- Displays a clear error message if the backend request fails (e.g. server not running)

### Screen 2: Analyzing (Loading State)

Shown while the request to the backend is in flight (the pipeline includes a live AI API call, so this can take a few seconds).

### Screen 3: Results Dashboard

- **Full pipeline connected end-to-end** — clicking "Try sample data" (or uploading a file) triggers a real HTTP request to the FastAPI `/analyze` endpoint. Nothing on this screen is mocked.
- **Categorized ratio cards, rendered dynamically** — rather than hardcoding eight separate elements, the component uses `Object.entries(data.ratios).map(...)` to loop over whatever ratios the backend returns and generate a card for each one automatically. The UI scales automatically if more ratios are added to `calculations.py`.
- **Health badge** — displays `data.verdict` directly from the backend's rules-based logic (not hardcoded).
- **AI explanation panel** — the plain-language analysis from Gemini, displayed in a visually distinct, highlighted section (amber accent), separating "AI-generated interpretation" from the "calculated facts" (ratio cards) at a glance.
- **Follow-up chat** — a chat input and message history for asking specific questions, as described above.

### Technical Notes

- **State management**: a single `screen` state variable (`"welcome" | "loading" | "results"`) controls which view is rendered, using conditional rendering rather than a routing library — appropriate for this app's simple, linear flow

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Calculation Engine | Pandas, NumPy |
| AI/LLM | Google Gemini API |
| Frontend | React (Vite) |
| Data | CSV/Excel (no database) |

## Project Structure

```
financial-statement-analyzer/
├── backend/
│   ├── calculations.py       → Pandas ratio calculations + verdict logic (Part A)
│   ├── ai_service.py         → Gemini API integration (Part B)
│   └── main.py                → FastAPI server (/analyze, /ask endpoints)
├── frontend/                 → React app (UI)
├── data/
│   └── sample_financials.csv → Sample dataset for testing
└── README.md
```

## Note on Sample Data

The `sample_financials.csv` file is synthetic test data created to verify the calculation logic against known, hand-calculated expected values before testing against real-world financial data. This is standard practice for validating logic in a controlled way before introducing real-world complexity.

##  What This Project Demonstrates

- **Hybrid AI system design** — separating deterministic computation from AI interpretation to eliminate hallucination risk in a domain (finance) where accuracy is critical
- **Full-stack development** — a working React frontend, FastAPI backend, and third-party AI API (Gemini) integrated into a single, coherent application
- **Thoughtful architectural decisions** — e.g. the financial health verdict is rule-based rather than AI-generated, so the same input always produces the same, auditable output
- **Practical debugging** — real issues encountered and resolved during development (CORS configuration, environment setup, indentation/naming bugs, API rate limits) rather than a pre-written, frictionless build