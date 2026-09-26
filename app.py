from pathlib import Path
import pandas as pd
import streamlit as st

FIELDS = ["company_fit", "need", "authority", "budget", "urgency", "engagement"]
WEIGHTS = {"company_fit": .20, "need": .20, "authority": .15, "budget": .15, "urgency": .15, "engagement": .15}

def qualify(row, hot, warm):
    values = {f: pd.to_numeric(row.get(f), errors="coerce") for f in FIELDS}
    present = {k: max(0, min(100, float(v))) for k, v in values.items() if pd.notna(v)}
    missing = [f for f in FIELDS if f not in present]
    if len(present) < 3:
        return pd.Series({"score": 0, "category": "Needs Review", "confidence": "Low", "next_action": "Complete missing qualification fields", "reasoning": f"Insufficient evidence; missing: {', '.join(missing)}"})
    denominator = sum(WEIGHTS[k] for k in present)
    score = sum(present[k] * WEIGHTS[k] for k in present) / denominator
    category = "Hot" if score >= hot else "Warm" if score >= warm else "Cold"
    action = {"Hot": "Schedule discovery or proposal discussion", "Warm": "Nurture and verify missing qualification details", "Cold": "Low-frequency nurture or manual review"}[category]
    strongest = sorted(present, key=present.get, reverse=True)[:2]
    reason = f"Strongest factors: {', '.join(strongest)}. Missing: {', '.join(missing) if missing else 'none'}."
    return pd.Series({"score": round(score, 1), "category": category, "confidence": "High" if not missing else "Medium", "next_action": action, "reasoning": reason})

st.set_page_config(page_title="Lead Qualification Agent", page_icon="🎯", layout="wide")
st.title("🎯 Lead Qualification Agent")
st.caption("Explainable lead prioritization. Human review remains authoritative.")
uploaded = st.file_uploader("Upload lead CSV", type="csv")
source = uploaded if uploaded else Path(__file__).with_name("sample_data.csv")
df = pd.read_csv(source)
hot = st.sidebar.slider("Hot threshold", 60, 95, 75)
warm = st.sidebar.slider("Warm threshold", 30, hot - 1, 55)
missing_cols = [c for c in ["lead", *FIELDS] if c not in df.columns]
if missing_cols:
    st.error("Missing columns: " + ", ".join(missing_cols))
    st.stop()
results = pd.concat([df, df.apply(qualify, axis=1, args=(hot, warm))], axis=1).sort_values("score", ascending=False)
st.metric("Leads analyzed", len(results))
st.dataframe(results, use_container_width=True, hide_index=True)
st.download_button("Download results", results.to_csv(index=False), "qualified_leads.csv", "text/csv")

