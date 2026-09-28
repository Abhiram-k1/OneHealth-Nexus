"""
OneHealth Nexus - Spark Batch Preprocessing Script (Python Engine)
Mirror of Scala Spark processing for distributed or standalone environments.
"""

import os
import pandas as pd

def main():
    print("======================================")
    print("   ONEHEALTH NEXUS - PREPROCESSING")
    print("======================================")

    input_path = "data/processed/cleaned_documents.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    print(f"\nInput records: {len(df)}")
    print(f"Input columns: {list(df.columns)}")

    # Deduplicate and filter valid clean text
    cleaned_df = df[df["clean_text"].notna() & (df["clean_text"].astype(str).str.strip().str.len() > 0)]
    cleaned_df = cleaned_df.drop_duplicates(subset=["clean_text"])
    print(f"\nRecords after preprocessing: {len(cleaned_df)}")

    # Output directories
    for out_dir in ["spark_output", "data/processed/spark_output"]:
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "processed_documents.txt")
        cleaned_df[["document_id", "source", "date", "clean_text"]].to_csv(
            out_file, sep="\t", index=False
        )
        print(f"Output saved to: {out_file}")

    print("\n======================================")
    print("Preprocessing completed successfully!")
    print(f"Final records: {len(cleaned_df)}")
    print("======================================")

if __name__ == "__main__":
    main()
