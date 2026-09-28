import pandas as pd
import os

input_file = "data/processed/spark_output/processed_documents.txt"

output_dir = "analysis"
os.makedirs(output_dir, exist_ok=True)

output_csv = "analysis/emerging_signals.csv"

print("======================================")
print(" ONEHEALTH NEXUS - SIGNAL DETECTION")
print("======================================")

# Load processed documents
df = pd.read_csv(
    input_file,
    sep="\t",
    dtype=str
).fillna("")

print("\nTotal documents:", len(df))

# Extract year robustly
df["year"] = pd.to_numeric(df["date"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
df = df.dropna(subset=["year"]).copy()
df["year"] = df["year"].astype(int)

# Disease keywords
disease_keywords = [
    "influenza",
    "avian influenza",
    "bird flu",
    "covid",
    "covid-19",
    "coronavirus",
    "dengue",
    "malaria",
    "cholera",
    "ebola",
    "mpox",
    "monkeypox",
    "rabies",
    "tuberculosis",
    "typhoid",
    "measles",
    "nipah",
    "hepatitis"
]

results = []

# Analyze each disease
for disease in disease_keywords:

    mask = df["clean_text"].str.lower().str.contains(
        disease,
        regex=False,
        na=False
    )

    disease_df = df[mask].copy()

    if len(disease_df) == 0:
        continue

    total_mentions = len(disease_df)

    # Recent records
    max_year = df["year"].max()

    recent_df = disease_df[
        disease_df["year"] >= max_year - 1
    ]

    recent_mentions = len(recent_df)

    # Number of different sources
    source_count = disease_df["source"].nunique()

    # Number of different years
    year_count = disease_df["year"].nunique()

    # Simple emerging signal score
    recency_score = recent_mentions / total_mentions
    source_score = min(source_count / 3, 1)
    activity_score = min(total_mentions / 20, 1)

    signal_score = (
        0.5 * recency_score +
        0.3 * source_score +
        0.2 * activity_score
    ) * 100

    results.append({
        "disease": disease,
        "total_mentions": total_mentions,
        "recent_mentions": recent_mentions,
        "source_count": source_count,
        "year_count": year_count,
        "signal_score": round(signal_score, 2)
    })

signals = pd.DataFrame(results)

# Sort by score
signals = signals.sort_values(
    by="signal_score",
    ascending=False
)

print("\n======================================")
print("EMERGING SIGNAL RESULTS")
print("======================================")

if len(signals) > 0:
    print(
        signals.to_string(index=False)
    )
else:
    print("No disease signals detected.")

signals.to_csv(
    output_csv,
    index=False
)

print("\nResults saved to:")
print(output_csv)

print("\n======================================")
print("SIGNAL DETECTION COMPLETED")
print("======================================")