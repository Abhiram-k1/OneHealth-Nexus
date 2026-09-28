import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# ONEHEALTH NEXUS - TEMPORAL ANALYSIS
# ============================================================

input_file = "data/processed/spark_output/processed_documents.txt"

output_dir = "analysis"

os.makedirs(output_dir, exist_ok=True)

output_csv = "analysis/temporal_summary.csv"
output_png = "analysis/temporal_trend.png"

print("======================================")
print("   ONEHEALTH NEXUS - TEMPORAL ANALYSIS")
print("======================================")

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

df = pd.read_csv(
    input_file,
    sep="\t",
    dtype=str
).fillna("")

print("\nTotal documents:", len(df))

# Convert date robustly
df["year"] = pd.to_numeric(df["date"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")

# Remove invalid dates
valid_df = df.dropna(subset=["year"]).copy()
valid_df["year"] = valid_df["year"].astype(int)

print(
    "Documents with valid dates:",
    len(valid_df)
)

# ------------------------------------------------------------
# Count documents by year
# ------------------------------------------------------------

yearly = (
    valid_df
    .groupby("year")
    .size()
    .reset_index(name="document_count")
)

print("\n======================================")
print("DOCUMENTS BY YEAR")
print("======================================")

print(yearly.to_string(index=False))

# ------------------------------------------------------------
# Save summary
# ------------------------------------------------------------

yearly.to_csv(
    output_csv,
    index=False
)

print(
    "\nTemporal summary saved to:",
    output_csv
)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

if len(yearly) > 0:

    plt.figure(figsize=(10, 6))

    plt.plot(
        yearly["year"],
        yearly["document_count"],
        marker="o"
    )

    plt.xlabel("Year")
    plt.ylabel("Number of Documents")

    plt.title(
        "OneHealth Documents Over Time"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        output_png,
        dpi=300
    )

    plt.close()

    print(
        "Temporal trend saved to:",
        output_png
    )

# ------------------------------------------------------------
# Completion
# ------------------------------------------------------------

print("\n======================================")
print("TEMPORAL ANALYSIS COMPLETED")
print("======================================")