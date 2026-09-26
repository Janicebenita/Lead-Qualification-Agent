# Lead Qualification Agent

A transparent Streamlit agent that scores leads using company fit, need, authority, budget, urgency, and engagement. It explains every score, identifies missing information, and recommends a next sales action.

## Features

- Upload a CSV or use bundled sample leads
- Adjustable qualification threshold
- Hot, Warm, Cold, and Needs Review categories
- Factor-level reasoning and missing-data warnings
- Downloadable prioritized results

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Expected CSV columns: `lead,company_fit,need,authority,budget,urgency,engagement`. Score fields accept values from 0 to 100; blanks remain unknown.

## Agent flow

1. Validate lead fields.
2. Calculate a weighted score from available factors.
3. Reduce confidence when important fields are missing.
4. Assign a category and recommended action.
5. Display the factor-level explanation for human review.

## Passport

The repository root includes `agent.yaml`, `SOUL.md`, and `EXPLAINABILITY.md` for OpenGAP passport submission. Category: **Marketing & sales**.

