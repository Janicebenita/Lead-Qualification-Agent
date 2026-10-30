# Lead Qualification Agent Explainability

## Decision and Reasoning Process

The agent's decision combines available fit, need, authority, budget, timing, and engagement indicators using declared scoring rules. Its reasoning lists the strongest positive and negative factors and explains the recommended next action.

## Inputs and Data Sources Used

Input data may include CRM fields, inquiry forms, campaign engagement, meeting notes, and user-provided qualification criteria. Only supplied or authorized data sources are used, and missing values remain explicitly unknown.

## Outputs and Supporting Evidence

The agent outputs a score, qualification category, contributing factors, missing information, and recommended follow-up. Supporting evidence is tied to the exact lead fields used rather than unsupported assumptions.

## Limits, Constraints, and Known Issues

A key limitation is that incomplete or stale CRM data can produce an unreliable score. The agent cannot confirm purchasing authority, genuine intent, available budget, or future conversion without verified information.

## Uncertainty and Human Review

Uncertainty increases when important fields are missing or signals conflict. Human review is required before rejecting a lead, changing ownership, offering commercial terms, or making consequential customer decisions.

## Implementation in This Repository

The executable implementation is in `app.py`. Its `qualify` function converts the six declared qualification fields to bounded numeric values, requires at least three present fields, calculates a normalized weighted score from the `WEIGHTS` mapping, assigns Hot, Warm, Cold, or Needs Review, and returns the score, confidence, next action, and reasoning used by the Streamlit interface.

The same file loads either a user-uploaded CSV or `sample_data.csv`, verifies the required columns, applies `qualify` to each row, displays the sorted results, and offers the exact results as `qualified_leads.csv`. This implementation is deterministic for the same input data and thresholds; it does not call an external model or silently enrich CRM records.

