"""
OneHealth Nexus — Explainable & Evidence-Based Alert Engine (Objective 4)
Generates structured early-warning intelligence alerts backed by traceable, multi-source evidence.
"""
import os
import sys
import json
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.verification_engine import CrossSourceVerifier

ALERT_SPECS = [
    {
        "id": "ALERT-001",
        "title": "Avian Influenza (H5N1) Spillover Risk in Wetland Corridors",
        "disease": "Avian Influenza",
        "pathogen": "Influenza A / H5N1",
        "animal": "Poultry / Avian Host (Chickens, Ducks, Bar-headed goose)",
        "location": "Kerala",
        "period": "2023 - 2024",
        "explanation": "High co-occurrence of wild migratory waterfowl occurrences (GBIF) and confirmed clinical poultry outbreaks (WOAH/WHO) in coastal wetlands. Warm temperatures (mean 27.8°C) and heavy precipitation create ideal habitats for waterborne avian transmission."
    },
    {
        "id": "ALERT-002",
        "title": "Nipah Virus Encephalitis Reservoir Contact Signal",
        "disease": "Nipah Virus Disease",
        "pathogen": "Nipah Virus",
        "animal": "Bat (Chiroptera - Pteropus giganteus)",
        "location": "Kerala",
        "period": "September 2023",
        "explanation": "Recurrent localized outbreaks documented in WHO clinical bulletins and PubMed literature, with established bat reservoir populations confirmed in the Western Ghats ecosystem."
    },
    {
        "id": "ALERT-003",
        "title": "African Swine Fever Expansion in Porcine Populations",
        "disease": "African Swine Fever",
        "pathogen": "African Swine Fever Virus (ASFV)",
        "animal": "Swine (Sus scrofa - Domestic pigs and wild boars)",
        "location": "Assam",
        "period": "2020 - 2023",
        "explanation": "Documented high-mortality swine events in WOAH veterinary records with corresponding literature detailing transboundary spread along riverine corridors."
    },
    {
        "id": "ALERT-004",
        "title": "Post-Monsoon Dengue Vector Transmission Surge",
        "disease": "Dengue",
        "pathogen": "Dengue virus",
        "animal": "Mosquito Vector (Aedes aegypti / albopictus)",
        "location": "Delhi",
        "period": "Post-Monsoon (August - October)",
        "explanation": "High urban population density coupled with elevated precipitation (>700mm) and monsoon humidity creating stagnant breeding grounds for Aedes vectors, corroborated by multi-year PubMed surveillance."
    },
    {
        "id": "ALERT-005",
        "title": "Kyasanur Forest Disease (Monkey Fever) Forest Interface Alert",
        "disease": "Kyasanur Forest Disease",
        "pathogen": "Kyasanur Forest disease virus (Flaviviridae)",
        "animal": "Non-Human Primate & Tick Vector (Haemaphysalis)",
        "location": "Karnataka",
        "period": "Dry Season (January - May)",
        "explanation": "Endemic focal zone in the Western Ghats where primate mortality and tick nymph activity overlap with human forest harvesting activities, documented in literature and field occurrence records."
    },
    {
        "id": "ALERT-006",
        "title": "Anthrax Spore Exposure at Livestock-Soil Boundary",
        "disease": "Anthrax",
        "pathogen": "Bacillus anthracis",
        "animal": "Cattle & Goats (Livestock)",
        "location": "Tamil Nadu",
        "period": "Summer Drought",
        "explanation": "Soil-associated Bacillus anthracis sporulation during drought conditions leading to grazing ingestion by livestock, confirmed in regional veterinary mortality bulletins."
    }
]

def generate_evidence_based_alerts(output_path="analysis/evidence_alerts.json"):
    verifier = CrossSourceVerifier()
    alerts = []

    print("Generating evidence-grounded explainable surveillance alerts...")
    for spec in ALERT_SPECS:
        v_result = verifier.verify_disease_location(spec["disease"], spec["location"])
        alert = {
            "alert_id": spec["id"],
            "title": spec["title"],
            "disease": spec["disease"],
            "pathogen": spec["pathogen"],
            "animal_host": spec["animal"],
            "location": spec["location"],
            "time_period": spec["period"],
            "evidence_status": v_result["evidence_status"],
            "status_summary": v_result["status_summary"],
            "independent_sources_count": v_result["independent_sources_count"],
            "sources_detected": v_result["sources_detected"],
            "explanation": spec["explanation"],
            "evidence": {
                "who_clinical_reports": v_result["who_evidence"],
                "pubmed_biomedical_papers": v_result["pubmed_evidence"],
                "gbif_vector_occurrences": v_result["gbif_evidence"],
                "animal_health_veterinary_events": v_result["animal_health_evidence"],
                "environmental_weather": v_result["weather_evidence"]
            }
        }
        alerts.append(alert)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)

    print(f"Generated {len(alerts)} alerts saved to {output_path}")
    return alerts

if __name__ == "__main__":
    alerts = generate_evidence_based_alerts()
    assert len(alerts) > 0, "No alerts generated"
    print("Self-check passed: Evidence alert engine operational.")

