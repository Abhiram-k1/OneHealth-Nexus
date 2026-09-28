import pandas as pd
import matplotlib.pyplot as plt
import os

input_file = "data/processed/cleaned_gbif.csv"

output_dir = "analysis"
os.makedirs(output_dir, exist_ok=True)

output_csv = "analysis/spatial_summary.csv"
output_png = "analysis/spatial_distribution.png"

print("======================================")
print("     ONEHEALTH NEXUS - SPATIAL")
print("======================================")

# Load GBIF data
df = pd.read_csv(input_file, dtype=str).fillna("")

print("\nTotal GBIF records:", len(df))

print("\nAvailable columns:")
print(df.columns.tolist())

# Detect latitude and longitude columns
lat_col = None
lon_col = None

for col in df.columns:
    c = col.lower()

    if "lat" in c:
        lat_col = col

    if "lon" in c or "lng" in c:
        lon_col = col

print("\nLatitude column:", lat_col)
print("Longitude column:", lon_col)

if lat_col is None or lon_col is None:
    print("\nERROR: Latitude/Longitude columns not found.")
    exit()

# Convert coordinates
df["latitude"] = pd.to_numeric(df[lat_col], errors="coerce")
df["longitude"] = pd.to_numeric(df[lon_col], errors="coerce")

valid_df = df.dropna(subset=["latitude", "longitude"]).copy()

print("\nRecords with valid coordinates:", len(valid_df))

# Basic geographic summary
summary = pd.DataFrame({
    "metric": [
        "Total GBIF records",
        "Records with valid coordinates",
        "Minimum latitude",
        "Maximum latitude",
        "Minimum longitude",
        "Maximum longitude"
    ],
    "value": [
        len(df),
        len(valid_df),
        valid_df["latitude"].min(),
        valid_df["latitude"].max(),
        valid_df["longitude"].min(),
        valid_df["longitude"].max()
    ]
})

print("\n======================================")
print("SPATIAL SUMMARY")
print("======================================")

print(summary.to_string(index=False))

summary.to_csv(output_csv, index=False)

print("\nSpatial summary saved to:", output_csv)

# Plot geographic distribution
if len(valid_df) > 0:

    plt.figure(figsize=(10, 7))

    plt.scatter(
        valid_df["longitude"],
        valid_df["latitude"],
        alpha=0.6,
        s=20
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("GBIF Animal Occurrence Distribution")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        output_png,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Spatial distribution saved to:", output_png)

print("\n======================================")
print("SPATIAL ANALYSIS COMPLETED")
print("======================================")
