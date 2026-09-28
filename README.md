# OneHealth Nexus: Large-Scale NLP and Temporal Knowledge Graphs for Emerging Disease Intelligence

**B.Tech Artificial Intelligence and Data Science (AIDS) — Semester V (UG-III)**  
**Course:** Text Analytics (TA) & Big Data Analytics (BDA)  
**Department of Artificial Intelligence & Data Science, Amrita Vishwa Vidyapeetham, Delhi NCR, Faridabad**

---

## Academic Information & Team Credentials

- **Institution:** Amrita Vishwa Vidyapeetham, Delhi NCR Campus, Faridabad
- **Department:** Department of Artificial Intelligence & Data Science (AIDS)
- **Subject Coordinators & Mentors:**
  - **Dr. Ranjit Panigrahi**, Associate Professor
  - **Dr. Barkha Singh**, Assistant Professor
- **Project Team Members:**
  - **Anagha Manoj** — Roll No: `DL.AI.U4AID24105`
  - **Mimansha Goyal** — Roll No: `DL.AI.U4AID24123`
  - **Tanvi Bhardwaj** — Roll No: `DL.AI.U4AID24136`
  - **Kundurthi Abhiram** — Roll No: `DL.AI.U4AID24144`

---

## Executive Summary & Abstract

Emerging infectious diseases (EIDs) poses existential threats to global public health. More than 70% of emerging human pathogens are zoonotic, originating at the interface where humans, domestic livestock, and wild animal populations intersect with changing environmental conditions. Despite the availability of rich open-access biological and epidemiological data, disease surveillance remains fundamentally fragmented:
1. **Clinical & Epidemiological Reports:** Stored in unstructured text bulletins (e.g., World Health Organization Disease Outbreak News).
2. **Biomedical Literature:** Buried in millions of peer-reviewed scientific articles (e.g., NCBI PubMed/MEDLINE).
3. **Biodiversity & Ecological Vectors:** Documented in structured species occurrence repositories (e.g., Global Biodiversity Information Facility — GBIF).

Because these domains are analyzed in isolation, cross-species transmission pathways, reservoir host distributions, and early warning signals of disease emergence often remain hidden until widespread outbreaks occur.

**OneHealth Nexus** addresses this gap by engineering an integrated, large-scale analytical framework that unifies distributed Big Data processing, natural language processing (NLP), temporal knowledge graphs, and geospatial biodiversity analytics. Using **Apache Spark 4.0.1** and **Scala 2.13.16**, raw heterogeneous textual records are cleaned, deduplicated, and transformed into 592 standardized documents. An NLP pipeline powered by **spaCy** extracts multi-domain biomedical entities (diseases, pathogens, animal hosts, geographic locations, and dates) and maps their semantic relationships. A directed Knowledge Graph built with **NetworkX** models **1,620 entities and 2,611 semantic relationships**, enabling network topology and centrality analysis. Spatio-temporal intelligence modules analyze longitudinal disease patterns across time (2022–2027) and spatial animal host occurrences across India (GBIF coordinates: Lat 8.48°–31.42° N, Lon 71.68°–94.63° E). An analytical **Emerging Signal Indicator** synthesizes recency, source diversity, and mention volume to rank potential disease threats. The complete intelligence layer is deployed via an interactive, high-performance **Streamlit Dashboard** featuring seven dedicated intelligence modules.

---

## System Architecture

```
                          ┌──────────────────────────────────────────────────────────┐
                          │                HETEROGENEOUS DATA SOURCES                │
                          └──────────────────────────────────────────────────────────┘
                                   │                      │                     │
                     ┌─────────────▼─────────┐ ┌──────────▼─────────┐ ┌─────────▼─────────┐
                     │ WHO Outbreak News API │ │  PubMed NCBI API   │ │  GBIF India API   │
                     │  (50 Outbreak DONs)   │ │  (1000 Articles)   │ │  (300 Occurrences)│
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
                                   │   592 Processed Documents   │              │
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
                                   │    1,620 Nodes | 2,611 Rels │              │
                                   │   Topological Centralities  │              │
                                   └──────────────┬──────────────┘              │
                                                  │                             │
                                 ┌────────────────┴────────────────┐            │
                                 ▼                                 ▼            ▼
                   ┌───────────────────────────┐     ┌────────────────────────────────────┐
                   │    TEMPORAL INTELLIGENCE  │     │   SPATIAL BIODIVERSITY OCCURRENCE  │
                   │ (Yearly/Longitudinal Trend│     │ (GBIF Host Distribution in India)  │
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
| **Data Ingestion** | Python, `requests`, `xml.etree` | 3.12 / Standard | Automated REST harvesting with retry exponential backoff from WHO, PubMed, GBIF |
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
2. **PubMed / NCBI Entrez Biomedical Literature:** 1,000 articles retrieved using targeted domain search queries: `One Health`, `Zoonotic disease`, `Zoonoses`, `Emerging infectious disease`, `Spillover`. Extracted fields: PMID, Title, Abstract, Year, Journal.
3. **GBIF Species Occurrence (Animalia in India):** 300 verified animal occurrences with valid geographic coordinates (latitude, longitude, species, kingdom, state/province, event date).

### Stage 2: Initial Normalization & Colab Pipeline
- Performed HTML/XML tag stripping, HTML entity unescaping, whitespace canonicalization, character filtering, and deduplication.
- Unified WHO and PubMed into a common schema: `document_id`, `source`, `date`, `clean_text`.
- Validated output datasets: `cleaned_documents.csv` (2.34 MB), `cleaned_gbif.csv` (67.5 KB), and `data_summary.csv`.

### Stage 3: Distributed Big Data Processing with Apache Spark + Scala
- Written in **Scala 2.13.16** utilizing **Apache Spark 4.0.1** with SBT project configuration.
- Reads `data/processed/cleaned_documents.csv` via Spark SQL DataFrame API.
- Implements distributed filtering: null elimination, length checks (`length(trim(col("clean_text"))) > 0`), and text deduplication (`dropDuplicates("clean_text")`).
- Output: Exactly **592 verified processed documents** exported as a tab-delimited corpus (`processed_documents.txt`).

### Stage 4: Biomedical Natural Language Processing (spaCy)
- Processes the 592 Spark-cleaned documents through spaCy's `en_core_web_sm` model and domain-specific regular expressions.
- **Entity Extraction Categories:**
  - `Disease`: Influenza, Avian Influenza, COVID-19, Dengue, Malaria, Cholera, Ebola, Mpox, Rabies, Tuberculosis, Typhoid, Measles, Nipah, Hepatitis.
  - `Pathogen`: Virus, Coronavirus, SARS-CoV-2, H5N1, H7N9, Bacteria, Parasite, Fungus.
  - `Animal Host`: Bird, Poultry, Chicken, Duck, Pig, Swine, Bat, Dog, Cat, Cattle, Cow, Livestock, Wildlife.
  - `Location (GPE)`: Extracted via statistical NER (countries, states, outbreak epicenters).
  - `Date (DATE)`: Extracted via statistical NER and temporal expressions.
  - `Document`: Unique identifier node serving as provenance origin.

### Stage 5: Temporal Knowledge Graph Construction (NetworkX)
- Constructed as a directed graph $G = (V, E)$ in NetworkX.
- **Graph Scale:**
  - **Total Nodes ($|V|$):** **1,620**
  - **Total Relationships ($|E|$):** **2,611**
  - **Graph Density:** $0.0009955$
- **Node Breakdown:**
  - Documents: 557
  - Dates: 544
  - Locations: 470
  - Animals: 21
  - Diseases: 17
  - Pathogens: 11
- **Relationship Semantics:**
  - `Document` $\xrightarrow{\text{MENTIONS\_DISEASE}}$ `Disease`
  - `Document` $\xrightarrow{\text{MENTIONS\_PATHOGEN}}$ `Pathogen`
  - `Document` $\xrightarrow{\text{MENTIONS\_ANIMAL}}$ `Animal`
  - `Document` $\xrightarrow{\text{MENTIONS\_LOCATION}}$ `Location`
  - `Document` $\xrightarrow{\text{HAS\_DATE}}$ `Date`
  - Cross-domain inferences: `Animal` $\xrightarrow{\text{ASSOCIATED\_WITH}}$ `Disease`, `Pathogen` $\xrightarrow{\text{FOUND\_IN}}$ `Animal`, `Disease` $\xrightarrow{\text{REPORTED\_IN}}$ `Location`.

### Stage 6: Spatio-Temporal Intelligence & Signal Detection
1. **Temporal Intelligence:** Converts dates to ISO years, tracks publication/outbreak density over time (464 records concentrated in 2026, baseline historical validation 2024–2025). Generates `temporal_summary.csv` and `temporal_trend.png`.
2. **Spatial Biodiversity Intelligence:** Maps 300 GBIF animal occurrences across India. Coordinates bound the subcontinent: Latitude $8.484^\circ\text{ N}$ to $31.420^\circ\text{ N}$, Longitude $71.676^\circ\text{ E}$ to $94.628^\circ\text{ E}$. Generates `spatial_summary.csv` and `spatial_distribution.png`.
3. **Emerging Signal Detection Indicator:**
   A transparent multi-factor analytical scoring heuristic calculated as:
   $$\text{Signal Score} = \left( 0.5 \times \text{Recency Score} + 0.3 \times \text{Source Diversity Score} + 0.2 \times \text{Mention Volume Score} \right) \times 100$$
   - **Recency Score:** Ratio of recent-year mentions ($\ge \text{Year}_{\max} - 1$) to total mentions: $\frac{M_{\text{recent}}}{M_{\text{total}}}$
   - **Source Diversity Score:** Ratio of distinct sources mentioning the disease: $\min\left(\frac{N_{\text{sources}}}{3}, 1.0\right)$
   - **Mention Volume Score:** Activity scale threshold: $\min\left(\frac{M_{\text{total}}}{20}, 1.0\right)$

   **Top Ranked Signals Identified:**
   1. **Influenza:** 17 mentions, 16 recent, 2 sources $\rightarrow$ **Score: 84.06**
   2. **Avian Influenza:** 15 mentions, 14 recent, 2 sources $\rightarrow$ **Score: 81.67**
   3. **Rabies:** 13 mentions, 13 recent, 1 source $\rightarrow$ **Score: 73.00**
   4. **COVID-19:** 8 mentions, 8 recent, 1 source $\rightarrow$ **Score: 68.00**
   5. **Tuberculosis:** 7 mentions, 7 recent, 1 source $\rightarrow$ **Score: 67.00**
   6. **Ebola / Dengue / Coronavirus:** 6 mentions each $\rightarrow$ **Score: 66.00**
   7. **Nipah:** 5 mentions $\rightarrow$ **Score: 65.00**

### Stage 7: Streamlit Interactive Intelligence Dashboard
The interactive application (`dashboard/app.py`) provides 7 synchronized analytical views:
- **Tab 1: 🏠 Intelligence Overview** — Top-level metrics cards (592 documents, 1,620 nodes, 2,611 relationships, 300 GBIF records), top signal banner, and architecture flow diagram.
- **Tab 2: 🚨 Emerging Signals** — Ranked alert cards with composite scores, recency breakdowns, and source diversity tags.
- **Tab 3: 📈 Temporal Intelligence** — Interactive Plotly time-series charts showing outbreak dynamics across years.
- **Tab 4: 🌎 Spatial Intelligence** — Scatter distribution map plotting GBIF wildlife/domestic occurrences across Indian states and latitude/longitude bounds.
- **Tab 5: 🕸️ Knowledge Graph** — Subgraph visualizer and topological metrics table (top in-degree and out-degree central entities).
- **Tab 6: 🧬 Entity Intelligence** — Frequency breakdowns by entity type (Diseases, Pathogens, Animals, Locations, Dates).
- **Tab 7: 🔬 Methodology** — Full algorithmic transparency, formulas, One Health principles, and clinical disclaimer.

---

## Repository Directory Structure

```
OneHealth-Nexus/
├── .gitignore                      # Git exclusion rules (.venv, target, metals, pycache)
├── README.md                       # Comprehensive Project Specification & Report
├── PSEUDO.md                       # Layman-Friendly Implementation Walkthrough & Viva Guide
├── build.sbt                       # Scala / SBT dependencies (Spark 4.0.1, Scala 2.13.16)
├── requirements.txt                # Python dependencies (Streamlit, spaCy, NetworkX, Plotly, etc.)
├── run_all.ps1                     # Complete turnkey PowerShell pipeline orchestrator
├── analysis/                       # Spatio-temporal and signal detection scripts
│   ├── emerging_signals.py         # Signal scoring engine
│   ├── emerging_signals.csv        # Output ranked signal dataset
│   ├── spatial_analysis.py         # GBIF geospatial mapping script
│   ├── spatial_summary.csv         # India bounding coordinates summary
│   ├── spatial_distribution.png    # India animal occurrence scatter plot
│   ├── temporal_analysis.py        # Longitudinal time series script
│   ├── temporal_summary.csv        # Output document counts by year
│   ├── temporal_trend.png          # Longitudinal trend line chart
│   └── run_analysis.py             # Unified analysis module coordinator
├── dashboard/                      # Web dashboard tier
│   └── app.py                      # 7-page interactive Streamlit intelligence application
├── data/                           # Data storage tier
│   ├── raw/                        # Raw API datasets (who_outbreaks.csv, pubmed.csv, gbif.csv)
│   ├── processed/                  # Normalized datasets (cleaned_documents.csv, cleaned_gbif.csv)
│   └── processed/spark_output/     # Spark output corpus (processed_documents.txt - 592 docs)
├── docs/                           # Documentation, presentations, and design specifications
│   ├── TA AND BDA.pptx             # Official project slide presentation
│   ├── architecture_stack.jpeg     # Tech stack mapping diagram
│   ├── spark_scala_plan.txt        # Spark + Scala data processing plan
│   └── data_collection_plan.txt    # Data collection & schema architecture specification
├── knowledge_graph/                # Graph modeling tier
│   ├── build_graph.py              # NetworkX graph generator & centrality analyzer
│   ├── load_neo4j.py               # Neo4j property graph ingestion utility
│   ├── nodes.csv                   # Graph nodes (1,620 entities)
│   ├── relationships.csv           # Graph edges (2,611 relationships)
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
You can execute the entire pipeline with a single command via the PowerShell runner:
```powershell
.\run_all.ps1
```
This orchestrates:
1. Scala + Apache Spark distributed preprocessing (`sbt run`) $\rightarrow$ generates `processed_documents.txt` (592 documents).
2. spaCy NLP Entity Extraction (`nlp/entity_extraction.py`) $\rightarrow$ extracts entities and relationships into `nodes.csv` and `relationships.csv`.
3. NetworkX Knowledge Graph Construction (`knowledge_graph/build_graph.py`) $\rightarrow$ builds graph, computes centralities, exports `important_entities.csv` and `onehealth_subgraph.png`.
4. Analytical Modules (`analysis/run_analysis.py`) $\rightarrow$ generates temporal trends, spatial distributions, and emerging signal scores.

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
| **Raw PubMed Scientific Articles** | 1,000 articles | `data/raw/pubmed.csv` |
| **Raw GBIF Species Occurrences** | 300 records | `data/raw/gbif.csv` |
| **Cleaned Document Corpus Size** | 2.34 MB | `data/processed/cleaned_documents.csv` |
| **Spark Preprocessed Documents** | **592 documents** | `data/processed/spark_output/processed_documents.txt` |
| **Knowledge Graph Nodes** | **1,620 nodes** | `knowledge_graph/nodes.csv` |
| **Knowledge Graph Relationships** | **2,611 relationships** | `knowledge_graph/relationships.csv` |
| **Graph Density** | $9.955 \times 10^{-4}$ | `knowledge_graph/graph_summary.csv` |
| **Document Nodes** | 557 nodes | `knowledge_graph/graph_summary.csv` |
| **Temporal Date Nodes** | 544 nodes | `knowledge_graph/graph_summary.csv` |
| **Geographic Location Nodes** | 470 nodes | `knowledge_graph/graph_summary.csv` |
| **Animal Host Nodes** | 21 nodes | `knowledge_graph/graph_summary.csv` |
| **Disease Target Nodes** | 17 nodes | `knowledge_graph/graph_summary.csv` |
| **Pathogen Nodes** | 11 nodes | `knowledge_graph/graph_summary.csv` |
| **GBIF Valid Geographic Occurrences**| 300 coordinates (India) | `analysis/spatial_summary.csv` |
| **Geographic Coverage (India)** | Lat: $8.48^\circ - 31.42^\circ\text{ N}$, Lon: $71.68^\circ - 94.63^\circ\text{ E}$ | `analysis/spatial_distribution.png` |
| **Top Detected Emerging Signal** | Influenza / Avian Influenza (Score: 84.06 / 81.67) | `analysis/emerging_signals.csv` |

---

## References

1. **One Health High-Level Expert Panel (OHHLEP)** et al., *"Developing One Health surveillance systems,"* *One Health*, vol. 17, Art. no. 100617, 2023. DOI: `10.1016/j.onehlt.2023.100617`.
2. **J. Wu**, *"Construct a Knowledge Graph for China Coronavirus (COVID-19) Patient Information Tracking,"* *Risk Management and Healthcare Policy*, vol. 14, pp. 4321–4337, 2021. DOI: `10.2147/RMHP.S309732`.
3. **S. Consoli, P. Coletti, P. V. Markov, L. Orfei, I. Biazzo, L. Schuh, N. Stefanovitch, L. Bertolini, M. Ceresa, and N. I. Stilianakis**, *"An epidemiological knowledge graph extracted from the World Health Organization’s Disease Outbreak News,"* *Scientific Data*, vol. 12, Art. no. 970, 2025. DOI: `10.1038/s41597-025-05276-2`.
4. **W. J. Chen, S.-Y. Yang, J.-C. Chang, W.-C. Cheng, T.-P. Lu, Y.-N. Wang, M.-H. Juan, R.-T. Hsu, S.-R. Huang, J.-J. Tu, P.-C. Wang, V. W.-S. Feng, and P.-Z. Chang**, *"Development of a semi-structured, multifaceted, computer-aided questionnaire for outbreak investigation: e-Outbreak Platform,"* *Biomedical Journal*, vol. 43, no. 4, pp. 318–324, 2020. DOI: `10.1016/j.bj.2020.06.007`.

---

## Disclaimer
The **OneHealth Nexus** platform and its Emerging Signal Detection indicator are analytical research and decision-support heuristics designed for academic evaluation in Big Data Analytics and Text Analytics. They do not constitute official epidemiological diagnostic software or certified clinical outbreak prediction tools.
