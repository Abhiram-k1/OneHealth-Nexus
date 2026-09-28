# OneHealth Nexus: Large-Scale NLP and Temporal Knowledge Graphs for Emerging Disease Intelligence

**An Integrated Big Data & Spatio-Temporal Intelligence Platform for Zoonotic Disease Surveillance**  
**Core Technologies:** Apache Spark, Scala, spaCy, NetworkX, Streamlit, Plotly, Pandas, NCBI Entrez, GBIF API

---

## Executive Summary & Abstract

Emerging infectious diseases (EIDs) pose severe threats to global biosecurity and public health. Over 70% of emerging human pathogens are zoonotic, originating at the interface where humans, domestic livestock, and wild animal populations intersect with changing environmental conditions. Despite the availability of rich open-access biological and epidemiological data, disease surveillance remains fundamentally fragmented:
1. **Clinical & Epidemiological Reports:** Stored in unstructured text bulletins (e.g., World Health Organization Disease Outbreak News).
2. **Biomedical Literature:** Buried in millions of peer-reviewed scientific articles (e.g., NCBI PubMed/MEDLINE).
3. **Biodiversity & Ecological Vectors:** Documented in structured species occurrence repositories (e.g., Global Biodiversity Information Facility — GBIF).

Because these domains are analyzed in isolation, cross-species transmission pathways, reservoir host distributions, and early warning signals of disease emergence often remain hidden until widespread outbreaks occur.

**OneHealth Nexus** addresses this gap by engineering an integrated, large-scale analytical framework that unifies distributed Big Data processing, natural language processing (NLP), temporal knowledge graphs, and geospatial biodiversity analytics. Using **Apache Spark 4.0.1** and **Scala 2.13.16**, raw heterogeneous textual records are cleaned, deduplicated, and transformed into 2,550 standardized documents. An NLP pipeline powered by **spaCy** extracts multi-domain biomedical entities (diseases, pathogens, animal hosts, geographic locations, and dates) and maps their semantic relationships. A directed Knowledge Graph built with **NetworkX** models **2,720 entities and 10,946 semantic relationships**, enabling network topology and centrality analysis. Spatio-temporal intelligence modules analyze longitudinal disease patterns across 53 calendar years (1965–2027) and spatial animal host occurrences across India (**3,000 GPS coordinates**, Lat $6.94^\circ - 33.82^\circ\text{ N}$, Lon $68.97^\circ - 95.95^\circ\text{ E}$). An analytical **Emerging Signal Indicator** synthesizes recency, source diversity, and mention volume to rank potential disease threats. The complete intelligence layer is deployed via an interactive, high-performance **Streamlit Dashboard** featuring seven dedicated intelligence modules.

---

## Data Milestone Status: Achieving 5,550+ Points Toward 10k Target

The platform is designed around a multi-stage data scaling architecture aiming for **10,000+ multi-modal data points**. Currently, **5,550 verified data points (>55% of the final milestone)** are fully ingested, cleaned, and integrated into the active analytics engine:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ONEHEALTH NEXUS — ACTIVE DATA MILESTONE                      │
├───────────────────────────────┬───────────────────────────────┬─────────────────┤
│ Data Stream                   │ Modality                      │ Record Count    │
├───────────────────────────────┼───────────────────────────────┼─────────────────┤
│ WHO Disease Outbreak News     │ Clinical Outbreak Bulletins   │ 50 Bulletins    │
│ NCBI PubMed / MEDLINE         │ Peer-Reviewed Literature      │ 2,500 Articles  │
│ GBIF Biodiversity (India)     │ Georeferenced Coordinates     │ 3,000 Points    │
├───────────────────────────────┼───────────────────────────────┼─────────────────┤
│ TOTAL ACTIVE DATA POINTS      │ All Integrated Modalities     │ 5,550 RECORDS   │
└───────────────────────────────┴───────────────────────────────┴─────────────────┘
```

> For full feature dictionaries, statistical distributions, missing value audits, and recommendations for scaling to 10,000+ records, refer to [`DATA_STUDY.md`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/DATA_STUDY.md).

---

## System Architecture

```
                          ┌──────────────────────────────────────────────────────────┐
                          │                HETEROGENEOUS DATA SOURCES                │
                          └──────────────────────────────────────────────────────────┘
                                   │                      │                     │
                     ┌─────────────▼─────────┐ ┌──────────▼─────────┐ ┌─────────▼─────────┐
                     │ WHO Outbreak News API │ │  PubMed NCBI API   │ │  GBIF India API   │
                     │  (50 Outbreak DONs)   │ │  (2500 Articles)   │ │  (3000 Records)   │
                     └─────────────┬─────────┘ └──────────┬─────────┘ └─────────┬─────────┘
                                   │                      │                     │
                                   └──────────────┬───────┘                     │
                                                  ▼                             ▼
                                   ┌─────────────────────────────┐ ┌────────────────────────┐
                                   │  COLAB INGESTION & CLEANING │ │  GEO-VALIDATION (IND)  │
                                   │   cleaned_documents.csv     │ │    cleaned_gbif.csv    │
                                   └──────────────┬──────────────┘ └────────────┬───────────┘
                                                  ▼                             │
                                   ┌─────────────────────────────┐              │
                                   │    APACHE SPARK + SCALA     │              │
                                   │ (Distributed Cleaning/Dedup)│              │
                                   │  2,550 Processed Documents  │              │
                                   └──────────────┬──────────────┘              │
                                                  ▼                             │
                                   ┌─────────────────────────────┐              │
                                   │       PYTHON + spaCy        │              │
                                   │  Named Entity & Rel. Extr.  │              │
                                   │  Disease, Pathogen, Host,   │              │
                                   │  Location, Date, Document   │              │
                                   └──────────────┬──────────────┘              │
                                                  ▼                             │
                                   ┌─────────────────────────────┐              │
                                   │   NETWORKX KNOWLEDGE GRAPH  │              │
                                   │   2,720 Nodes | 10,946 Rels │              │
                                   │   Topological Centralities  │              │
                                   └──────────────┬──────────────┘              │
                                                  │                             │
                                 ┌────────────────┴────────────────┐            │
                                 ▼                                 ▼            ▼
                   ┌───────────────────────────┐     ┌────────────────────────────────────┐
                   │    TEMPORAL INTELLIGENCE  │     │   SPATIAL BIODIVERSITY OCCURRENCE  │
                   │ (53-Year Longitudinal Pan)│     │ (3000 GBIF Coordinates in India)   │
                   └─────────────┬─────────────┘     └──────────────────┬─────────────────┘
                                 │                                      │
                                 └────────────────┬─────────────────────┘
                                                  ▼
                                   ┌─────────────────────────────┐
                                   │  EMERGING SIGNAL DETECTION  │
                                   │  (Recency + Diversity + Vol)│
                                   └──────────────┬──────────────┘
                                                  ▼
                                   ┌─────────────────────────────┐
                                   │  STREAMLIT DASHBOARD (UI)   │
                                   │ 7-Page Multi-View Analytics │
                                   └─────────────────────────────┘
```

---

## Technology Stack & Module Matrix

| Tier / Module | Technology | Version | Primary Purpose |
|---|---|---|---|
| **Data Ingestion** | Python, `requests`, `urllib` | 3.12 / Standard | Automated REST harvesting with retry exponential backoff from WHO, PubMed, GBIF |
| **Big Data Engine** | Apache Spark, Scala, SBT | Spark 4.0.1, Scala 2.13.16 | Large-scale resilient text preprocessing, schema filtering, deduplication, JVM I/O |
| **NLP & Entity Extraction** | Python, spaCy, RegEx | spaCy 3.7+, `en_core_web_sm` | Named Entity Recognition (NER) for GPE, DATE, Disease, Pathogen, Animal taxa |
| **Knowledge Graph Engine** | NetworkX, Neo4j driver | NetworkX 3.3+, Neo4j 5.20+ | Multi-relational directed graph modeling, degree centrality, betweenness, subgraph rendering |
| **Temporal & Spatial Analytics** | Pandas, NumPy, Matplotlib | Pandas 2.2+, Matplotlib 3.8+ | Longitudinal trend aggregation, India bounding box spatial validation, signal scoring |
| **Emerging Signal Scoring** | Analytical Heuristic Formulation | Custom Python Engine | Multi-factor risk composite: Recency (50%) + Diversity (30%) + Volume (20%) |
| **Interactive Dashboard** | Streamlit, Plotly Express | Streamlit 1.40+, Plotly 5.20+ | Responsive web interface featuring 7 analytics tabs, interactive KPI cards, charts, and tables |

---

## Detailed Pipeline Stages

### Stage 1: Multi-Source Heterogeneous Data Collection
Data collection targets three distinct domains reflecting the One Health paradigm:
1. **WHO Disease Outbreak News (DONs):** 50 outbreak reports covering international public health emergencies (Ebola, Cholera, Avian Influenza, Dengue, MERS, etc.).
2. **PubMed / NCBI Entrez Biomedical Literature:** 2,500 articles retrieved using targeted domain search queries: `One Health`, `Zoonotic disease`, `Zoonoses`, `Emerging infectious disease`, `Spillover`, `Nipah virus`, `Kyasanur Forest disease`, `Scrub typhus`, `Leptospirosis`.
3. **GBIF Species Occurrence (Animalia in India):** 3,000 verified animal occurrences with valid geographic coordinates across classes *Mammalia*, *Aves*, *Reptilia*, and *Amphibia*.

### Stage 2: Initial Normalization & Preprocessing
- Strips HTML/XML markup, decodes HTML entities, replaces carriage returns, and removes whitespace irregularities.
- Merges the text datasets into a 4-column canonical schema:
  $$\text{Schema} = \left[ \text{document\_id}, \text{source}, \text{date}, \text{clean\_text} \right]$$
- Exports normalized datasets: `cleaned_documents.csv`, `cleaned_gbif.csv`, and `data_summary.csv`.

### Stage 3: Distributed Big Data Processing with Apache Spark + Scala
- Written in **Scala 2.13.16** utilizing **Apache Spark 4.0.1** with SBT project configuration.
- Reads `data/processed/cleaned_documents.csv` via Spark SQL DataFrame API.
- Implements distributed filtering: null elimination, length checks (`length(trim(col("clean_text"))) > 0`), and text deduplication (`dropDuplicates("clean_text")`).
- Output: Exactly **2,550 verified unique documents** exported as a tab-delimited corpus (`processed_documents.txt`).

### Stage 4: Biomedical Natural Language Processing (spaCy / RegEx Engine)
- Extracts multi-domain biomedical entities:
  - `Disease`: Influenza, Avian Influenza, COVID-19, Dengue, Malaria, Cholera, Ebola, Mpox, Rabies, Tuberculosis, Typhoid, Measles, Nipah, Hepatitis, Leptospirosis, Kyasanur Forest Disease, Scrub Typhus, Anthrax, Brucellosis.
  - `Pathogen`: Virus, Influenza virus, Coronavirus, SARS-CoV-2, H5N1, H7N9, Ebolavirus, Bacteria, Orientia tsutsugamushi, Leptospira, Bacillus anthracis.
  - `Animal Host`: Bird, Poultry, Chicken, Duck, Pig, Swine, Bat, Dog, Cat, Cattle, Cow, Livestock, Horse, Goat, Sheep, Wildlife, Rodent, Monkey, Primate.
  - `Location (GPE)`: Geopolitical entities and epicenters (India, Kerala, Tamil Nadu, Karnataka, Maharashtra, Delhi, Assam, China, Egypt, etc.).
  - `Date (DATE)`: Chronological references spanning 1965 to 2027.
- Generates **2,720 unique nodes** and **10,946 directed relationships**.

### Stage 5: Temporal Knowledge Graph Construction (NetworkX)
- Constructed as a directed graph $G = (V, E)$ in NetworkX.
- **Graph Scale:**
  - **Total Nodes ($|V|$):** **2,720**
  - **Total Relationships ($|E|$):** **10,946**
  - **Graph Density:** $0.00148$
- **Node Breakdown:**
  - Documents: 2,550
  - Dates: 83
  - Animals: 25
  - Locations: 24
  - Diseases: 23
  - Pathogens: 15
- **Relationship Semantics:**
  - `Document` $\xrightarrow{\text{MENTIONS\_DISEASE}}$ `Disease`
  - `Document` $\xrightarrow{\text{MENTIONS\_PATHOGEN}}$ `Pathogen`
  - `Document` $\xrightarrow{\text{MENTIONS\_ANIMAL}}$ `Animal`
  - `Document` $\xrightarrow{\text{MENTIONS\_LOCATION}}$ `Location`
  - `Document` $\xrightarrow{\text{HAS\_DATE}}$ `Date`

### Stage 6: Spatio-Temporal Intelligence & Signal Detection
1. **Temporal Intelligence:** Converts dates to ISO years, tracks longitudinal publication and outbreak patterns across 53 calendar years (1965 to 2027), with major contemporary volume in 2024 (641 docs), 2025 (518 docs), and 2026 (744 docs).
2. **Spatial Biodiversity Intelligence:** Maps **3,000 GBIF animal occurrences across India**, bounding the entire subcontinent from South (Lat $6.94^\circ\text{ N}$) to North (Lat $33.82^\circ\text{ N}$), and West (Lon $68.97^\circ\text{ E}$) to East (Lon $95.95^\circ\text{ E}$).
3. **Emerging Signal Detection Indicator:**
   Calculates a multi-factor analytical scoring heuristic:
   $$\text{Signal Score} = \left( 0.5 \times \text{Recency Score} + 0.3 \times \text{Source Diversity Score} + 0.2 \times \text{Mention Volume Score} \right) \times 100$$

   **Top Ranked Signals (Expanded Corpus):**
   1. **Dengue:** 309 mentions, 172 recent $\rightarrow$ **Score: 57.83**
   2. **Malaria:** 13 mentions, 6 recent, 2 sources $\rightarrow$ **Score: 56.08**
   3. **Mpox / Monkeypox:** 312 mentions, 148 recent $\rightarrow$ **Score: 53.79 / 53.40**
   4. **Avian Influenza / Influenza:** 238 mentions, 62 recent, 2 sources $\rightarrow$ **Score: 53.16 / 53.03**
   5. **Coronavirus:** 28 mentions, 6 recent, 2 sources $\rightarrow$ **Score: 50.71**
   6. **Ebola:** 312 mentions, 63 recent, 2 sources $\rightarrow$ **Score: 50.10**
   7. **Nipah:** 26 mentions, 8 recent $\rightarrow$ **Score: 45.38**
   8. **COVID-19:** 52 mentions, 4 recent $\rightarrow$ **Score: 43.85**

### Stage 7: Streamlit Interactive Intelligence Dashboard
The interactive application (`dashboard/app.py`) provides 7 synchronized analytical views:
- **Tab 1: 🏠 Intelligence Overview** — Top-level metrics cards (2,550 documents, 2,720 nodes, 10,946 relationships, 3,000 GBIF records), top signal banner, and architecture flow diagram.
- **Tab 2: 🚨 Emerging Signals** — Ranked alert cards with composite scores, recency breakdowns, and source diversity tags.
- **Tab 3: 📈 Temporal Intelligence** — Interactive Plotly time-series charts showing outbreak dynamics across 53 years.
- **Tab 4: 🌎 Spatial Intelligence** — Scatter distribution map plotting 3,000 GBIF wildlife/domestic occurrences across Indian states and latitude/longitude bounds.
- **Tab 5: 🕸️ Knowledge Graph** — Subgraph visualizer and topological metrics table (top in-degree and out-degree central entities).
- **Tab 6: 🧬 Entity Intelligence** — Frequency breakdowns by entity type (Diseases, Pathogens, Animals, Locations, Dates).
- **Tab 7: 🔬 Methodology** — Full algorithmic transparency, formulas, One Health principles, and clinical disclaimer.

---

## Repository Directory Structure

```
OneHealth-Nexus/
├── .gitignore                      # Git exclusion rules (.venv, target, metals, pycache)
├── README.md                       # Core Technical Specification & Platform Architecture
├── PSEUDO.md                       # Layman-Friendly Implementation Walkthrough & Viva Guide
├── DATA_STUDY.md                   # Comprehensive Data Study, Feature Dictionaries & 10k Roadmap
├── build.sbt                       # Scala / SBT dependencies (Spark 4.0.1, Scala 2.13.16)
├── requirements.txt                # Python dependencies (Streamlit, spaCy, NetworkX, Plotly, etc.)
├── run_all.ps1                     # Complete turnkey PowerShell pipeline orchestrator
├── analysis/                       # Spatio-temporal and signal detection scripts
│   ├── emerging_signals.py         # Signal scoring engine
│   ├── emerging_signals.csv        # Output ranked signal dataset
│   ├── spatial_analysis.py         # GBIF geospatial mapping script
│   ├── spatial_summary.csv         # India bounding coordinates summary (3,000 points)
│   ├── spatial_distribution.png    # India animal occurrence scatter plot
│   ├── temporal_analysis.py        # Longitudinal time series script (53 years)
│   ├── temporal_summary.csv        # Output document counts by year
│   ├── temporal_trend.png          # Longitudinal trend line chart
│   └── run_analysis.py             # Unified analysis module coordinator
├── dashboard/                      # Web dashboard tier
│   └── app.py                      # 7-page interactive Streamlit intelligence application
├── data/                           # Data storage tier
│   ├── raw/                        # Raw API datasets (who_outbreaks.csv, pubmed.csv, gbif.csv)
│   ├── processed/                  # Normalized datasets (cleaned_documents.csv, cleaned_gbif.csv)
│   └── processed/spark_output/     # Spark output corpus (processed_documents.txt - 2,550 docs)
├── docs/                           # Documentation, presentations, and design specifications
│   ├── TA AND BDA.pptx             # Slide presentation
│   ├── architecture_stack.jpeg     # Tech stack mapping diagram
│   ├── spark_scala_plan.txt        # Spark + Scala data processing plan
│   └── data_collection_plan.txt    # Data collection & schema architecture specification
├── knowledge_graph/                # Graph modeling tier
│   ├── build_graph.py              # NetworkX graph generator & centrality analyzer
│   ├── load_neo4j.py               # Neo4j property graph ingestion utility
│   ├── nodes.csv                   # Graph nodes (2,720 entities)
│   ├── relationships.csv           # Graph edges (10,946 relationships)
│   ├── graph_summary.csv           # Summary graph statistics & densities
│   ├── important_entities.csv      # Degree centrality ranked entities
│   └── onehealth_subgraph.png      # High-resolution subgraph visualization
├── nlp/                            # NLP information extraction tier
│   ├── entity_extraction.py        # spaCy NER + domain keyword extraction engine
│   └── pipeline.py                 # Alternative multi-source regex entity extractor
├── notebooks/                      # Exploratory & ingestion notebooks
│   └── TA_AND_BDA_PROJECT.ipynb    # Google Colab data harvesting & cleaning notebook
├── project/                        # SBT build metadata
│   └── build.properties            # SBT version definition (1.10.7)
└── src/main/scala/                 # Apache Spark distributed processing source
    └── OneHealthPreprocessing.scala# Spark SQL filtering and deduplication job
```

---

## Setup & Execution Guide

### Prerequisites
1. **Python 3.10+ / 3.12** installed and available in system PATH.
2. **Java JDK 17+** (required for Apache Spark).
3. **sbt (Scala Build Tool)** installed (required for running the Scala preprocessing job).

### Step 1: Environment Setup
```powershell
# Clone or navigate to the repository
cd "c:\Users\abhi8\OneDrive\Desktop\ACADEMIC DOCS\SEM-5\TA&BDA\OneHealth-Nexus"

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install all project dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download the spaCy English language model
python -m spacy download en_core_web_sm
```

### Step 2: One-Click End-to-End Pipeline Execution
```powershell
.\run_all.ps1
```
This orchestrates:
1. Scala + Apache Spark distributed preprocessing (`sbt run`) $\rightarrow$ generates `processed_documents.txt` (2,550 documents).
2. spaCy NLP Entity Extraction (`nlp/entity_extraction.py`) $\rightarrow$ extracts entities and relationships into `nodes.csv` and `relationships.csv` (2,720 nodes, 10,946 edges).
3. NetworkX Knowledge Graph Construction (`knowledge_graph/build_graph.py`) $\rightarrow$ builds graph, computes centralities, exports `important_entities.csv` and `onehealth_subgraph.png`.
4. Analytical Modules (`analysis/run_analysis.py`) $\rightarrow$ generates temporal trends across 53 years, spatial distributions over 3,000 India coordinates, and emerging signal scores.

### Step 3: Launching the Interactive Streamlit Dashboard
```powershell
streamlit run dashboard\app.py
```
Open your browser at `http://localhost:8501` to access the interactive OneHealth Nexus Intelligence Center.

---

## Empirical Results Summary

| Metric Dimension | Measured Empirical Value | Primary File / Artifact |
|---|---|---|
| **Raw WHO Outbreak Reports** | 50 records | `data/raw/who_outbreaks.csv` |
| **Raw PubMed Scientific Articles** | 2,500 articles | `data/raw/pubmed.csv` |
| **Raw GBIF Species Occurrences** | 3,000 records | `data/raw/gbif.csv` |
| **Total Ingested Data Points** | **5,550 Data Points** (>55% of 10k target) | `data/processed/data_summary.csv` |
| **Cleaned Document Corpus Size** | 2,550 unique documents | `data/processed/cleaned_documents.csv` |
| **Spark Preprocessed Documents** | **2,550 documents** | `data/processed/spark_output/processed_documents.txt` |
| **Knowledge Graph Nodes** | **2,720 nodes** | `knowledge_graph/nodes.csv` |
| **Knowledge Graph Relationships** | **10,946 relationships** | `knowledge_graph/relationships.csv` |
| **Graph Density** | $0.00148$ | `knowledge_graph/graph_summary.csv` |
| **Document Nodes** | 2,550 nodes | `knowledge_graph/graph_summary.csv` |
| **Temporal Date Nodes** | 83 nodes | `knowledge_graph/graph_summary.csv` |
| **Geographic Location Nodes** | 24 nodes | `knowledge_graph/graph_summary.csv` |
| **Animal Host Nodes** | 25 nodes | `knowledge_graph/graph_summary.csv` |
| **Disease Target Nodes** | 23 nodes | `knowledge_graph/graph_summary.csv` |
| **Pathogen Nodes** | 15 nodes | `knowledge_graph/graph_summary.csv` |
| **GBIF Valid Geographic Occurrences**| **3,000 coordinates (India)** | `analysis/spatial_summary.csv` |
| **Geographic Coverage (India)** | Lat: $6.94^\circ - 33.82^\circ\text{ N}$, Lon: $68.97^\circ - 95.95^\circ\text{ E}$ | `analysis/spatial_distribution.png` |
| **Temporal Coverage** | 53 Calendar Years (1965 – 2027) | `analysis/temporal_summary.csv` |
| **Top Detected Emerging Signals** | Dengue (57.83), Malaria (56.08), Mpox (53.79), Avian Flu (53.16) | `analysis/emerging_signals.csv` |

---

## References

1. **One Health High-Level Expert Panel (OHHLEP)** et al., *"Developing One Health surveillance systems,"* *One Health*, vol. 17, Art. no. 100617, 2023. DOI: `10.1016/j.onehlt.2023.100617`.
2. **J. Wu**, *"Construct a Knowledge Graph for China Coronavirus (COVID-19) Patient Information Tracking,"* *Risk Management and Healthcare Policy*, vol. 14, pp. 4321–4337, 2021. DOI: `10.2147/RMHP.S309732`.
3. **S. Consoli, P. Coletti, P. V. Markov, L. Orfei, I. Biazzo, L. Schuh, N. Stefanovitch, L. Bertolini, M. Ceresa, and N. I. Stilianakis**, *"An epidemiological knowledge graph extracted from the World Health Organization’s Disease Outbreak News,"* *Scientific Data*, vol. 12, Art. no. 970, 2025. DOI: `10.1038/s41597-025-05276-2`.
4. **W. J. Chen, S.-Y. Yang, J.-C. Chang, W.-C. Cheng, T.-P. Lu, Y.-N. Wang, M.-H. Juan, R.-T. Hsu, S.-R. Huang, J.-J. Tu, P.-C. Wang, V. W.-S. Feng, and P.-Z. Chang**, *"Development of a semi-structured, multifaceted, computer-aided questionnaire for outbreak investigation: e-Outbreak Platform,"* *Biomedical Journal*, vol. 43, no. 4, pp. 318–324, 2020. DOI: `10.1016/j.bj.2020.06.007`.

---

## Disclaimer
The **OneHealth Nexus** platform and its Emerging Signal Detection indicator are analytical research and decision-support heuristics. They do not constitute official epidemiological diagnostic software or certified clinical outbreak prediction tools.
