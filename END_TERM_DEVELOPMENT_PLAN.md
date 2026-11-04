# ONEHEALTH NEXUS: END-TERM DEVELOPMENT PLAN & PROGRESS TRACKER

**Project Title:** ONEHEALTH NEXUS: An Evidence-Grounded Knowledge Graph for Integrated Human, Animal and Environmental Disease Intelligence  
**Evaluation:** End-Term Academic Submission  
**Framework:** Apache Spark 4.0.1 / Scala / PySpark, Biomedical NLP (spaCy vs. PubMedBERT), NetworkX Multi-Hop Knowledge Graph, Open-Meteo Environmental Intelligence, Streamlit Surveillance Dashboard  
**Status Date:** November 2026  
**Overall Completion:** **100% COMPLETED (All End-Term Objectives Verified & Tested)**

---

## 1. Master Objectives & Progress Tracker

| ID | Objective | Priority | Completion Criteria | Status | Actual Result / Verification |
|:---|:---|:---:|:---|:---:|:---|
| **O1** | **Improve existing NLP extraction** | High | Validated disease, animal, pathogen, location, date extraction with normalization, word-boundary preservation, and sentence-level provenance | **COMPLETED** | Upgraded `nlp/entity_extraction.py`: 5,208 nodes, 16,031 edges, 26,024 sentence provenance links in `knowledge_graph/entity_provenance.csv` |
| **O2** | **Implement PubMedBERT NER** | High | Trained/fine-tuned PubMedBERT token classification model on biomedical One Health corpus with BIO tagging and saved weights/tokenizer | **COMPLETED** | Fine-tuned `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext` across One Health corpus; weights & tokenizer saved to `models/pubmedbert_ner/` |
| **O3** | **Compare both NLP models** | High | Common held-out test dataset, precision, recall, F1-score per entity, confusion matrix, inference latency, error analysis, and comparative report | **COMPLETED** | Evaluated on held-out test split. Pipeline A: F1=0.8754 (4.04ms). Pipeline B: F1=0.8384 (251.76ms). Full report in `COMPARATIVE_ANALYSIS_REPORT.md` |
| **O4** | **Integrate weather data** | High | Open-Meteo environmental dataset (temperature, precipitation, dates, coordinates) linked to KG locations with longitudinal charts | **COMPLETED** | Collected 3,650 historical daily observations across 10 surveillance hubs (`data/processed/weather_data.csv`) |
| **O5** | **Evidence-based dashboard alerts** | High | Traceable alerts linking WHO, PubMed, GBIF, and Weather with explicit evidence status (`SUPPORTED`, `NEEDS_REVIEW`, `LIMITED_EVIDENCE`) | **COMPLETED** | Generated 6 evidence-grounded alerts in `analysis/evidence_alerts.json` with multi-source attribution and confidence grades |
| **O6** | **Cross-source verification** | Medium | Verification layer comparing disease, pathogen, animal, location, and dates across independent sources | **COMPLETED** | Implemented `src/verification_engine.py` cross-referencing clinical, literature, vector, and climate streams |
| **O7** | **Add animal-health data source** | Medium | Integration of official animal disease surveillance data (WOAH WAHIS / FAO EMPRES-i) with source attribution | **COMPLETED** | Standardized 10 official veterinary outbreak records in `data/processed/cleaned_animal_health.csv` with official portal URLs |
| **O8** | **Incremental data pipeline** | Medium | Deduplication and incremental ingestion mechanism processing new records without historical recomputation | **COMPLETED** | Built `src/incremental_pipeline.py` with SHA-256 state manifest (`ingestion_manifest.json`), preventing duplicate historical computation |
| **O9** | **Dashboard improvements** | High | Refactored 8-module Streamlit dashboard supporting all intelligence sections and live model comparison | **COMPLETED** | Refactored `dashboard/app.py` into 8 dedicated surveillance modules with interactive dual-model sandbox and high-contrast styling |
| **O10** | **Final testing and documentation** | High | End-to-end assert-based tests, comparative evaluation report, and updated academic documentation | **COMPLETED** | Automated test suite `tests/test_end_to_end.py` passed all 6 validation tiers (14,210 harmonized data points verified) |

*Status Labels: `NOT STARTED` | `IN PROGRESS` | `COMPLETED` | `BLOCKED`*

---

## 2. Verified Active Ingestion Metrics (14,210 Total Records)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            ONEHEALTH NEXUS — ACTIVE DATA MILESTONE                               │
├─────────────────────────────────────┬─────────────────────────────────┬──────────────────────────┤
│ Data Stream                         │ Surveillance Modality           │ Record Count             │
├─────────────────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ WHO Disease Outbreak News (DONs)    │ Human Clinical Outbreaks        │ 50 Outbreak Bulletins    │
│ NCBI PubMed / MEDLINE Corpus        │ Biomedical Literature           │ 5,000 Research Articles  │
│ GBIF Biodiversity (India)           │ Animal Vector Occurrences       │ 5,500 Geocoded Points    │
│ Open-Meteo Historical Archive       │ Environmental Climate & Weather │ 3,650 Daily Records      │
│ WOAH WAHIS & FAO EMPRES-i           │ Veterinary Animal Disease       │ 10 Validated Events      │
├─────────────────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ TOTAL HARMONIZED DATA POINTS        │ Integrated Surveillance Streams │ 14,210 TOTAL RECORDS     │
└─────────────────────────────────────┴─────────────────────────────────┴──────────────────────────┘
```

---

## 3. Knowledge Graph Topology & Cross-Domain Relations

- **Nodes:** 5,208 total nodes (5,050 Documents, 83 Dates, 28 Locations, 23 Diseases, 12 Pathogens, 12 Animals).
- **Relationships:** 16,031 total relationships including direct semantic multi-hop edges:
  - `MENTIONS_ANIMAL`: 4,790
  - `MENTIONS_DISEASE`: 3,729
  - `HAS_DATE`: 3,471
  - `MENTIONS_LOCATION`: 1,859
  - `MENTIONS_PATHOGEN`: 1,831
  - `REPORTED_IN` (*Disease $\rightarrow$ Location*): 228
  - `ASSOCIATED_WITH` (*Animal $\rightarrow$ Disease*): 60
  - `HOST_RESERVOIR_OF` (*Animal $\rightarrow$ Pathogen*): 38
  - `CAUSES_DISEASE` (*Pathogen $\rightarrow$ Disease*): 25
- **Evidentiary Provenance:** 26,024 sentence-level context records in `knowledge_graph/entity_provenance.csv`.

---

## 4. NLP Comparative Benchmark Summary

Evaluated on held-out test split (`data/evaluation/biomedical_ner_dataset.json`):
- **Pipeline A (Existing NLP Engine):** Accuracy = 0.8939, Weighted F1 = 0.8754, Inference Latency = 4.04 ms/sentence.
- **Pipeline B (PubMedBERT Token Classifier):** Accuracy = 0.8636, Weighted F1 = 0.8384, Inference Latency = 251.76 ms/sentence.
- **Key Finding:** Pipeline A achieves ~62x higher throughput for bulk Spark preprocessing; PubMedBERT demonstrates superior out-of-vocabulary spatial generalization (Location F1: 1.0000 vs. 0.6000). A two-tier hybrid architecture is recommended.

---

## 5. End-to-End Validation Execution Log

Execution of `tests/test_end_to_end.py` confirmed 100% test pass rate:
- `[1/6] Ingestion Data Integrity`: Verified 14,210 multi-source records.
- `[2/6] NLP Model Artifacts & Evaluation`: Verified Pipeline A and Pipeline B metrics.
- `[3/6] Knowledge Graph Topology`: Verified 5,208 nodes, 16,031 relationships, and 9 edge types.
- `[4/6] Environmental Weather Quality`: Verified 3,650 daily observations without missing values.
- `[5/6] Explainable Alerts`: Verified 6 multi-source alerts with explicit status attribution.
- `[6/6] Incremental Pipeline`: Verified SHA-256 state manifest with 0 redundant recomputations.
