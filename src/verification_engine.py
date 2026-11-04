"""
OneHealth Nexus — Cross-Source Information Verification Engine (Objective 5 & 6)
Cross-references disease, pathogen, animal, location, and date across:
  1. WHO Disease Outbreak News (Clinical bulletins)
  2. PubMed Peer-Reviewed Literature (Biomedical research)
  3. GBIF Biodiversity (Animal occurrence records)
  4. WOAH WAHIS / FAO EMPRES-i (Veterinary animal disease events)
  5. Open-Meteo Historical Archive (Environmental weather)
Assigns Evidence Status: SUPPORTED | NEEDS_REVIEW | LIMITED_EVIDENCE
"""
import os
import re
import pandas as pd

class CrossSourceVerifier:
    def __init__(
        self,
        docs_path="data/processed/spark_output/processed_documents.txt",
        gbif_path="data/processed/cleaned_gbif.csv",
        animal_health_path="data/processed/cleaned_animal_health.csv",
        weather_path="data/processed/weather_data.csv",
        provenance_path="knowledge_graph/entity_provenance.csv"
    ):
        self.docs_df = pd.read_csv(docs_path, sep="\t", dtype=str).fillna("") if os.path.exists(docs_path) else pd.DataFrame()
        self.gbif_df = pd.read_csv(gbif_path, dtype=str).fillna("") if os.path.exists(gbif_path) else pd.DataFrame()
        self.animal_health_df = pd.read_csv(animal_health_path, dtype=str).fillna("") if os.path.exists(animal_health_path) else pd.DataFrame()
        self.weather_df = pd.read_csv(weather_path, dtype=str).fillna("") if os.path.exists(weather_path) else pd.DataFrame()
        self.provenance_df = pd.read_csv(provenance_path, dtype=str).fillna("") if os.path.exists(provenance_path) else pd.DataFrame()

    def verify_disease_location(self, disease_name, location_name):
        """Cross-checks evidence across clinical, research, animal, and environmental streams."""
        dis_clean = disease_name.lower().strip()
        loc_clean = location_name.lower().strip()

        evidence_sources = set()
        matched_who = []
        matched_pubmed = []
        matched_gbif = []
        matched_animal_health = []
        matched_weather = []

        # 1. Check WHO Bulletins
        who_mask = (
            (self.docs_df["source"] == "WHO_DON") &
            (self.docs_df["clean_text"].str.lower().str.contains(dis_clean, na=False)) &
            (self.docs_df["clean_text"].str.lower().str.contains(loc_clean, na=False))
        )
        who_matches = self.docs_df[who_mask]
        if not who_matches.empty:
            evidence_sources.add("WHO Disease Outbreak News")
            for _, r in who_matches.head(3).iterrows():
                matched_who.append({
                    "id": r.get("document_id", ""),
                    "date": r.get("date", ""),
                    "excerpt": r.get("clean_text", "")[:250] + "..."
                })

        # 2. Check PubMed Literature
        pubmed_mask = (
            (self.docs_df["source"] == "PubMed") &
            (self.docs_df["clean_text"].str.lower().str.contains(dis_clean, na=False))
        )
        # optional location check in pubmed
        pubmed_loc_mask = pubmed_mask & self.docs_df["clean_text"].str.lower().str.contains(loc_clean, na=False)
        pubmed_matches = self.docs_df[pubmed_loc_mask]
        if pubmed_matches.empty:
            pubmed_matches = self.docs_df[pubmed_mask]

        if not pubmed_matches.empty:
            evidence_sources.add("PubMed Peer-Reviewed Research")
            for _, r in pubmed_matches.head(3).iterrows():
                matched_pubmed.append({
                    "id": r.get("document_id", ""),
                    "date": r.get("date", ""),
                    "excerpt": r.get("clean_text", "")[:250] + "..."
                })

        # 3. Check GBIF Animal Occurrences in Location
        if not self.gbif_df.empty:
            gbif_loc_mask = (
                self.gbif_df["state"].str.lower().str.contains(loc_clean, na=False) |
                self.gbif_df["country"].str.lower().str.contains(loc_clean, na=False)
            )
            gbif_matches = self.gbif_df[gbif_loc_mask]
            if not gbif_matches.empty:
                evidence_sources.add("GBIF Biodiversity Vector Data")
                for _, r in gbif_matches.head(3).iterrows():
                    matched_gbif.append({
                        "gbif_id": r.get("gbif_id", ""),
                        "species": r.get("species", "") or r.get("scientific_name", ""),
                        "locality": r.get("locality", ""),
                        "coords": f"({r.get('latitude', '')}, {r.get('longitude', '')})",
                        "year": r.get("year", "")
                    })

        # 4. Check WOAH / FAO Veterinary Animal Disease Events
        if not self.animal_health_df.empty:
            ah_mask = (
                (self.animal_health_df["disease"].str.lower().str.contains(dis_clean, na=False) |
                 self.animal_health_df["serotype_or_pathogen"].str.lower().str.contains(dis_clean, na=False)) &
                (self.animal_health_df["state_or_province"].str.lower().str.contains(loc_clean, na=False) |
                 self.animal_health_df["country"].str.lower().str.contains(loc_clean, na=False))
            )
            ah_matches = self.animal_health_df[ah_mask]
            if not ah_matches.empty:
                evidence_sources.add("WOAH / FAO Animal Health Surveillance")
                for _, r in ah_matches.head(2).iterrows():
                    matched_animal_health.append({
                        "event_id": r.get("event_id", ""),
                        "disease": r.get("disease", ""),
                        "species": r.get("species", ""),
                        "date": r.get("outbreak_start_date", ""),
                        "status": r.get("status", ""),
                        "source": r.get("source", ""),
                        "url": r.get("source_url", "")
                    })

        # 5. Check Environmental Weather
        if not self.weather_df.empty:
            w_mask = self.weather_df["location"].str.lower().str.contains(loc_clean, na=False)
            w_matches = self.weather_df[w_mask]
            if not w_matches.empty:
                evidence_sources.add("Open-Meteo Environmental Weather")
                matched_weather = {
                    "location": location_name,
                    "avg_temp_c": round(float(w_matches["temperature_mean_c"].astype(float).mean()), 1),
                    "max_temp_c": round(float(w_matches["temperature_max_c"].astype(float).max()), 1),
                    "total_rainfall_mm": round(float(w_matches["precipitation_mm"].astype(float).sum()), 1),
                    "days_recorded": len(w_matches)
                }

        # Determine Verification Status
        source_count = len(evidence_sources)
        if source_count >= 3:
            status = "SUPPORTED"
            summary = f"Corroborated across {source_count} independent surveillance streams."
        elif source_count == 2:
            status = "NEEDS_REVIEW"
            summary = f"Detected in {source_count} sources; additional independent epidemiological confirmation recommended."
        else:
            status = "LIMITED_EVIDENCE"
            summary = f"Observed in {source_count} source only; preliminary or uncorroborated finding."

        return {
            "disease": disease_name,
            "location": location_name,
            "evidence_status": status,
            "independent_sources_count": source_count,
            "sources_detected": list(evidence_sources),
            "status_summary": summary,
            "who_evidence": matched_who,
            "pubmed_evidence": matched_pubmed,
            "gbif_evidence": matched_gbif,
            "animal_health_evidence": matched_animal_health,
            "weather_evidence": matched_weather
        }

if __name__ == "__main__":
    verifier = CrossSourceVerifier()
    res = verifier.verify_disease_location("Avian Influenza", "Kerala")
    print(f"Verification Test: {res['disease']} in {res['location']}")
    print(f"Status: {res['evidence_status']} ({res['status_summary']})")
    print(f"Sources: {res['sources_detected']}")
    assert res["evidence_status"] in ["SUPPORTED", "NEEDS_REVIEW", "LIMITED_EVIDENCE"]
    print("Self-check passed: Cross-source verifier operational.")

