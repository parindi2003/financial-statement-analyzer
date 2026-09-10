#  AI-Powered Financial Statement Analyst Agent

An AI agent that analyzes financial statements — Pandas calculates the ratios, AI explains them in plain language.

#  What it does

Upload a company's financial statement (CSV/Excel with revenue, expenses, assets, liabilities), then ask questions like *"Is this company financially healthy?"* in natural language. The system automatically calculates financial ratios and uses AI to explain them in a way anyone can understand.

#  Architecture — Hybrid Approach

This project uses a **hybrid deterministic + AI architecture**:

- **Part A — Deterministic (Pandas/NumPy):** All financial ratio calculations are done with plain Python math. 100% accurate, no AI involved.
- **Part B — AI Reasoning (LLM):** The AI only receives already-calculated, verified numbers and explains them in plain language — it never does the math itself.

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