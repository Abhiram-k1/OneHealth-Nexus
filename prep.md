# ONEHEALTH NEXUS: MASTER PREPARATION & PRESENTATION GUIDE
### An Evidence-Grounded Knowledge Graph for Integrated Human, Animal, and Environmental Disease Intelligence

> **Welcome to the Project!**  
> If you are new to this project, reading this document from top to bottom will take you from zero knowledge to being able to explain, defend, and present the entire system with authority.
>
> 💡 **How to use this guide:**
> - **Section 1–3**: Core concepts, problem statement, and 5-layer system architecture.
> - **Section 4**: The **Deep-Dive NLP Model Comparison** (Rule-Based/spaCy vs. Fine-Tuned PubMedBERT).
> - **Section 5**: Data pipeline, Knowledge Graph, and Environmental Intelligence.
> - **Section 6**: Dashboard walkthrough and live demo script.
> - **Section 7**: **Viva / Evaluation Q&A Defense Guide** with active recall drills.
> - **Section 8**: Complete codebase file directory with clickable links.
>
> Throughout this guide, you will encounter **⚡ Active Recall Checkpoints**. Stop and answer them mentally before expanding the solution!

---

## 1. Executive Summary & The "One Health" Paradigm

### What is OneHealth Nexus?
**OneHealth Nexus** is an end-to-end Big Data Analytics and Biomedical NLP surveillance platform. It bridges the gap between three traditionally isolated domains of epidemiological intelligence:
1. **Human Health**: Clinical outbreak bulletins and surveillance reports from the **World Health Organization (WHO)**.
2. **Animal Health & Vector Biodiversity**: Scientific research literature from **NCBI PubMed/MEDLINE**, biodiversity vector records from **GBIF** (Global Biodiversity Information Facility), and veterinary disease alerts from **WOAH WAHIS** / **FAO EMPRES-i**.
3. **Environmental & Climate Drivers**: Historical and real-time meteorological observations (temperature, precipitation, humidity) from the **Open-Meteo Historical Archive**.

```
                         ┌────────────────────────┐
                         │   HUMAN SURVEILLANCE   │
                         │    (WHO DONs: 50)      │
                         └───────────┬────────────┘
                                     │
                                     ▼
┌────────────────────────┐       ┌───────┐       ┌────────────────────────┐
│  ANIMAL & VECTOR DATA  │◄─────►│ ONE   │◄─────►│ ENVIRONMENTAL CLIMATE  │
│ (GBIF: 5,500 | WOAH:10)│       │HEALTH │       │ (Open-Meteo: 3,650)    │
└────────────────────────┘       │ NEXUS │       └────────────────────────┘
                                 └───┬───┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │ BIOMEDICAL LITERATURE  │
                         │ (NCBI PubMed: 5,000)   │
                         └────────────────────────┘
```

### Why Does This Project Matter? (The Real-World Problem)
- **75% of emerging infectious diseases (EIDs) are zoonotic**—meaning they jump from animals to humans (e.g., Nipah virus, Avian Influenza H5N1, Mpox, COVID-19, Kyasanur Forest Disease).
- **The surveillance bottleneck**: Human health agencies (like WHO), wildlife biologists (GBIF), and climate researchers operate in silos. An outbreak is often only noticed after human hospitals fill up, even though wildlife mortality or extreme weather anomalies preceded it weeks earlier.
- **Our solution**: OneHealth Nexus automatically harmonizes **14,210 multi-source records**, extracts entities using both high-throughput NLP and deep transformer models, stores relationships in a **5,208-node Knowledge Graph**, and generates **explainable, multi-source alerts** backed by exact sentence-level provenance.

---

> ⚡ **Active Recall Checkpoint 1 (The Pitch)**
> 1. *In 30 seconds, explain what the "One Health" paradigm is and why siloing human, animal, and environmental data is dangerous.*
> 2. *Name the 5 data streams integrated into OneHealth Nexus and what surveillance modality each represents.*
>
> <details>
> <summary>👉 Click to Reveal Model Answer & Viva Talking Points</summary>
>
> 1. **Model Pitch**: "One Health recognizes that human health is inextricably linked to animal health and our shared environment. Over 70% of emerging infectious diseases are zoonotic. Siloing this data is dangerous because zoonotic spillover signals—such as bat vector migrations or unseasonal rainfall—occur weeks before clinical human outbreaks. OneHealth Nexus connects these streams to detect early warnings before human epidemics escalate."
> 2. **5 Data Streams**:
>    - **WHO DONs**: Human clinical outbreaks (50 bulletins).
>    - **NCBI PubMed**: Scientific literature and experimental discoveries (5,000 papers).
>    - **GBIF**: Animal vector and wildlife occurrence coordinates (5,500 points).
>    - **Open-Meteo**: Environmental meteorological records (3,650 daily observations).
>    - **WOAH / FAO**: Official veterinary disease reports (10 records).
> </details>

---

## 2. High-Level System Architecture (The 5 Layers)

The platform is designed around 5 distinct architectural layers, ensuring high throughput, rigorous evidence grounding, and interactive decision support:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ONEHEALTH NEXUS — 5-TIER ARCHITECTURE                           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Layer 1] Ingestion & Big Data Tier                                                    │
│  • Apache Spark 4.0.1 / Scala / PySpark batch processing                               │
│  • Incremental ingestion with SHA-256 state tracking (ingestion_manifest.json)         │
│  • 14,210 raw & processed records (WHO, PubMed, GBIF, Open-Meteo, WOAH)               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Layer 2] Dual Biomedical Information Extraction Tier                                  │
│  • Pipeline A: Rule-Based / spaCy / Regex Lexicon (4.04 ms/sent, 62x faster)           │
│  • Pipeline B: Fine-Tuned PubMedBERT Transformer (110M params, 11 BIO tags)            │
│  • Canonical concept normalization (e.g., "bird flu" -> "Avian Influenza")            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Layer 3] Provenance & Cross-Source Verification Tier                                  │
│  • 26,024 sentence-level context records (knowledge_graph/entity_provenance.csv)       │
│  • Multi-source cross-referencing (Human + Animal + Climate + Literature)              │
│  • Automated data integrity assertions (tests/test_end_to_end.py)                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Layer 4] Multi-Hop Knowledge Graph Tier                                               │
│  • 5,208 Nodes (Documents, Diseases, Animals, Pathogens, Locations, Dates)            │
│  • 16,031 Directed Semantic Edges (CAUSES_DISEASE, HOST_RESERVOIR_OF, REPORTED_IN)    │
│  • NetworkX topological engine with Graphviz / Matplotlib rendering                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Layer 5] Intelligence & Operational Decision Support Tier                             │
│  • Streamlit Surveillance Dashboard (dashboard/app.py) — 8 interactive modules         │
│  • Explainable Outbreak Alerts (SUPPORTED, NEEDS_REVIEW, LIMITED_EVIDENCE)             │
│  • Dual-model interactive text extraction sandbox with confidence metrics              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Processing & Incremental Pipeline

### Ingestion Statistics (Verified 14,210 Records)
| Stream | Source File / Endpoint | Record Count | Role in System |
|---|---|:---:|---|
| **Human Outbreaks** | `data/raw/who_scraped_data.csv` | 50 | Ground truth human outbreak events |
| **Biomedical Literature** | `data/processed/spark_output/processed_documents.txt` | 5,000 | Deep peer-reviewed textual context |
| **Animal Vectors** | `data/processed/cleaned_gbif.csv` | 5,500 | Geocoded vector occurrences in India |
| **Weather Archive** | `data/processed/weather_data.csv` | 3,650 | 10-year daily weather for 10 outbreak hotspots |
| **Veterinary Health** | `data/processed/cleaned_animal_health.csv` | 10 | Official WOAH/FAO animal disease reports |
| **Total** | Harmonized Data Lake | **14,210** | Integrated One Health multi-stream data |

### How the Incremental Pipeline Works (`src/incremental_pipeline.py`)
In real-world surveillance, reprocessing 14,000+ historical records every morning wastes compute and introduces race conditions.
1. Each incoming document or text record is hashed using **SHA-256** based on its raw content.
2. The hash is checked against [`data/processed/ingestion_manifest.json`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/data/processed/ingestion_manifest.json).
3. If the hash exists, the pipeline immediately skips extraction for that record.
4. If the record is new or updated, it flows through the NLP pipelines and updates the Knowledge Graph incrementally.
- **Verification**: In `tests/test_end_to_end.py`, running an incremental pass over the existing 5,050 documents processes **exactly 0 duplicate records**.

---

> ⚡ **Active Recall Checkpoint 2 (Data & Pipelines)**
> 1. *Why did we build an incremental ingestion pipeline using SHA-256 manifests instead of simply running a batch script daily?*
> 2. *What is stored in `entity_provenance.csv` and why is it essential for explainability?*
>
> <details>
> <summary>👉 Click to Reveal Model Answer & Viva Talking Points</summary>
>
> 1. **Incremental Ingestion**: "Batch re-processing 14,000+ records every time new data arrives causes $O(N)$ redundant computation, wastes transformer GPU/CPU cycles, and risks duplicating nodes in the Knowledge Graph. SHA-256 hashing creates a deterministic fingerprint for each document; only truly novel articles trigger NLP extraction."
> 2. **Entity Provenance**: "In clinical and public health intelligence, a black-box node link is untrustworthy. `entity_provenance.csv` stores 26,024 exact sentence-level citations containing the document ID, publication year, extracted entity, and surrounding sentence context (up to 300 characters), enabling epidemiologists to audit the evidence behind any graph edge."
> </details>

---

## 4. Deep-Dive NLP Model Comparison: spaCy / Lexicon vs. PubMedBERT

This is one of the most critical experimental components of the project. We built, trained, and benchmarked two parallel extraction engines on the exact same held-out test split.

### The Two Competing Pipelines

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ PIPELINE A: High-Throughput Lexicon + spaCy  │ PIPELINE B: Fine-Tuned PubMedBERT Classifier │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ • File: nlp/entity_extraction.py             │ • Files: nlp/pubmedbert_ner.py, models/      │
│ • Architecture: Compiled regex gazetteer +   │ • Architecture: 12-layer Transformer, 768    │
│   word boundary enforcement (\b) + spaCy     │   hidden size, 12 heads (110M parameters)    │
│   tokenization (en_core_web_sm)              │ • Head: Linear classifier with 11 BIO tags   │
│ • Canonical Concept Dictionary Normalization │ • Tokenizer: WordPiece subword alignment     │
│ • Latency: 4.04 ms / sentence                │ • Latency: 251.76 ms / sentence              │
│ • Throughput: ~247 sentences / sec           │ • Throughput: ~3.97 sentences / sec          │
│ • Hardware: Single CPU thread, <2 MB disk    │ • Hardware: PyTorch neural backend, 440 MB   │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

### The BIO Tagging Scheme in PubMedBERT
PubMedBERT was fine-tuned to classify every token into 11 discrete BIO tags:
- `O`: Outside any entity
- `B-DISEASE`, `I-DISEASE`: Beginning / Inside of a disease entity
- `B-ANIMAL`, `I-ANIMAL`: Animal species or host reservoir
- `B-PATHOGEN`, `I-PATHOGEN`: Biological virus, bacterium, or parasite
- `B-LOCATION`: Geographic state, country, or region
- `B-DATE`: Temporal year, month, or surveillance date

---

### Quantitative Head-to-Head Benchmark Table

Evaluated on held-out test split (`data/evaluation/biomedical_ner_dataset.json` — 8 sentences, 132 evaluation tokens):

| Evaluation Metric | Pipeline A (Existing NLP Engine) | Pipeline B (Fine-Tuned PubMedBERT) | Winner & Scientific Explanation |
|:---|:---:|:---:|---|
| **Overall Token Accuracy** | **0.8939** (89.4%) | 0.8636 (86.4%) | **Pipeline A (+3.0%)** |
| **Weighted Precision** | **0.8920** (89.2%) | 0.8247 (82.5%) | **Pipeline A (+6.7%)** |
| **Weighted Recall** | **0.8939** (89.4%) | 0.8636 (86.4%) | **Pipeline A (+3.0%)** |
| **Weighted F1-Score** | **0.8754** (87.5%) | 0.8384 (83.8%) | **Pipeline A (+3.7%)** |
| **Inference Latency** | **4.04 ms / sentence** | 251.76 ms / sentence | **Pipeline A is 62x faster** |
| **Inference Throughput** | **~247 sentences/sec** | ~3.97 sentences/sec | **Pipeline A is 62x higher throughput** |
| **Model Size on Disk** | **< 2 MB** | 440 MB | **Pipeline A is 220x smaller** |
| **RAM Footprint** | **~65 MB** | ~750 MB | **Pipeline A is 11.5x more lightweight** |

---

### Per-Category F1 Breakdown: The Nuanced Story

Looking only at overall F1 misses the most fascinating scientific insight of this project! When we break down performance by entity category, a striking pattern emerges:

| Entity Category | Pipeline A (Rule/spaCy) F1 | Pipeline B (PubMedBERT) F1 | Category Winner & Analysis |
|:---|:---:|:---:|---|
| **ANIMAL** | **1.0000** | **1.0000** | **Tie (100%)** — Both models flawlessly detect common hosts (swine, bats, poultry, cattle). |
| **LOCATION** | 0.6000 | **1.0000** | **PubMedBERT (+40.0%)** — **BERT completely dominates.** It uses sentence syntax (*"in [Location] during..."*) to identify locations never seen in training. Pipeline A relies on a fixed gazetteer and misses unindexed towns. |
| **DATE** | 0.9231 | **1.0000** | **PubMedBERT (+7.7%)** — BERT correctly groups multi-token calendar dates (*"June 2023"*, *"September 2021"*) while regex occasionally captures only partial numeric tokens. |
| **DISEASE** | **0.8800** | 0.6087 | **Pipeline A (+27.1%)** — Pipeline A's curated medical dictionary and concept normalization prevents false positives. BERT struggled with rare disease name boundaries. |
| **PATHOGEN** | **0.8421** | 0.5263 | **Pipeline A (+31.6%)** — Acronyms like *H5N1*, *SARS-CoV-2*, and *Lyssavirus* match unambiguously in regex, whereas BERT's WordPiece tokenizer fragments them into subwords (*H*, *##5*, *##N*, *##1*), causing boundary penalties. |

---

### Visual Metrics Comparison Plot
Located at [`analysis/model_comparison_metrics.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/analysis/model_comparison_metrics.png):

```
       OVERALL F1 & SPEED TRADE-OFF             PER-CATEGORY F1 COMPARISON
  1.0 ┌───────────────────────────────┐   1.0 ┌─────────────────────────────────┐
      │  0.8754                       │       │  1.0  1.0   1.0  1.0   1.0      │
  0.8 │  █████    0.8384              │   0.8 │  ███  ███        ███        ███   │
      │  █████    █████               │       │  ███  ███   ███  ███   ███  ███   │
  0.6 │  █████    █████               │   0.6 │  ███  ███   ███  ███   ███  ███   │
      │  █████    █████               │       │  ███  ███   ███  ███   ███  ███   │
  0.4 │  █████    █████               │   0.4 │  ███  ███   ███  ███   ███  ███   │
      │  █████    █████               │       │  ███  ███   ███  ███   ███  ███   │
  0.2 │  █████    █████               │   0.2 │  ███  ███   ███  ███   ███  ███   │
      │  █████    █████               │       │  ███  ███   ███  ███   ███  ███   │
  0.0 └───────────────────────────────┘   0.0 └─────────────────────────────────┘
         Pipe A   Pipe B                         Animal   Location  Date  Disease Pathogen
       (4.04ms)  (251.8ms)                    ■ Pipe A (Rule/spaCy)   ■ Pipe B (PubMedBERT)
```

---

### Qualitative Real-World Examples (Where Each Model Wins & Loses)

#### Case 1: Out-of-Vocabulary Location (PubMedBERT Wins)
> **Sentence:** *"In 2020, veterinarians quarantined swine herds in Mizoram due to African swine fever outbreaks."*
- **Gold Standard:** `Mizoram` [LOCATION]
- **Pipeline A (Rule/spaCy):** **MISSED `Mizoram`** (False Negative) because *"Mizoram"* was not explicitly listed in the curated location gazetteer.
- **Pipeline B (PubMedBERT):** **CORRECTLY DETECTED `Mizoram` [LOCATION]**. The self-attention heads recognized the prepositional context (*"in [X] due to..."*) and grammatical role, predicting `B-LOCATION` even without prior exposure.

#### Case 2: Subword Acronym Boundary (Pipeline A Wins)
> **Sentence:** *"Aedes aegypti mosquitoes collected in Kerala tested positive for Dengue virus in June 2023."*
- **Gold Standard:** `Dengue virus` [PATHOGEN]
- **Pipeline A (Rule/spaCy):** **CORRECT**. The regex pattern `\bdengue virus\b` matched and mapped directly to the canonical pathogen entity.
- **Pipeline B (PubMedBERT):** **PARTIAL ERROR**. BERT classified `Dengue` as `B-DISEASE` and `virus` as `O`, splitting the pathogen term and incurring precision/recall penalties.

---

### The Grand Conclusion: The Two-Tier Hybrid Architecture
In academic presentations, professors love to ask: *"So which model is better?"*  
The mature, engineering answer is: **Neither model is unilaterally superior; they are complementary.**

Our recommendation is a **Two-Tier Production Hybrid Architecture**:
1. **Tier 1 (High-Throughput Streaming Bulk Ingestion)**:
   - Run **Pipeline A** on the 5,000+ daily streaming PubMed articles and GBIF records. It runs in seconds on Spark at 4.04 ms/sentence with zero GPU requirements.
2. **Tier 2 (Contextual Verification on Low-Confidence / Novel Text)**:
   - Route sentences with unindexed geographic patterns, ambiguous syntax, or novel disease alerts to **Pipeline B (PubMedBERT)**. This gives us open-vocabulary spatial discovery (Location F1 = 1.0) without suffering a 62x throughput penalty on the entire corpus.

---

> ⚡ **Active Recall Checkpoint 3 (The NLP Showdown)**
> 1. *Why did Pipeline A beat PubMedBERT in overall F1 and pathogen extraction?*
> 2. *In which specific entity categories did PubMedBERT beat Pipeline A, and what architectural capability made this possible?*
> 3. *If an examiner asks: "Why not just throw away Pipeline A and use BERT for everything?", how will you respond?*
>
> <details>
> <summary>👉 Click to Reveal Model Answer & Viva Talking Points</summary>
>
> 1. **Why Pipeline A Won Overall/Pathogens**: "Pipeline A uses curated medical lexicons with canonical mapping and word-boundary enforcement. Biomedical pathogens (e.g., *H5N1*, *SARS-CoV-2*) have rigid nomenclature that regex matches deterministically. PubMedBERT's WordPiece tokenizer splits acronyms into subwords, and with a small fine-tuning dataset, it suffered boundary misalignment errors on pathogens."
> 2. **Where BERT Won**: "PubMedBERT achieved **1.0000 F1 on Locations (vs. 0.6000 for Pipeline A)** and **1.0000 on Dates (vs. 0.9231)**. It won because transformer multi-head self-attention learns contextual syntax (e.g., prepositional phrases like *'in [X]'*), enabling it to extract out-of-vocabulary locations (like *Mizoram*) that were never hardcoded in Pipeline A's dictionary."
> 3. **The "Why Not Just BERT" Defense**: "Running PubMedBERT on 14,000+ streaming records at 251.76 ms/sentence would take hours and require expensive GPU infrastructure. Pipeline A processes records at 4.04 ms/sentence (62x faster). We propose a **Two-Tier Hybrid Architecture**: Pipeline A handles high-throughput bulk streaming, while PubMedBERT is invoked on active surveillance sentences to catch out-of-vocabulary locations and novel contexts."
> </details>

---

## 5. Knowledge Graph & Environmental Intelligence

### Knowledge Graph Topology (`knowledge_graph/`)
- **Nodes (5,208)**:
  - 5,050 `Document` nodes (PubMed PMIDs + WHO DONs)
  - 83 `Date` nodes
  - 28 `Location` nodes
  - 23 `Disease` nodes
  - 12 `Pathogen` nodes
  - 12 `Animal` nodes
- **Relationships (16,031)**:
  - `MENTIONS_ANIMAL`: 4,790
  - `MENTIONS_DISEASE`: 3,729
  - `HAS_DATE`: 3,471
  - `MENTIONS_LOCATION`: 1,859
  - `MENTIONS_PATHOGEN`: 1,831
  - **Multi-Hop Semantic Edges** (Connecting concepts directly without document intermediaries):
    - `REPORTED_IN` (*Disease $\rightarrow$ Location*): 228
    - `ASSOCIATED_WITH` (*Animal $\rightarrow$ Disease*): 60
    - `HOST_RESERVOIR_OF` (*Animal $\rightarrow$ Pathogen*): 38
    - `CAUSES_DISEASE` (*Pathogen $\rightarrow$ Disease*): 25

```
                  ┌────────────────────────┐
                  │    Document (5,050)    │
                  └───────────┬────────────┘
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Animal (12)    │  │  Pathogen (12)  │  │  Disease (23)   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │ HOST_RESERVOIR_OF  │ CAUSES_DISEASE     │ REPORTED_IN
         └───────────────────►│                    ▼
                              └───────────►┌─────────────────┐
                                           │  Location (28)  │
                                           └─────────────────┘
```

### Environmental Intelligence (`src/weather_collector.py`)
- Sourced from the **Open-Meteo Historical Archive API**.
- Contains **3,650 daily observations** spanning 10 epidemiological hotspots in India (Kerala, Assam, Maharashtra, West Bengal, Tamil Nadu, etc.).
- Attributes collected: Mean Temperature (°C), Precipitation (mm), Relative Humidity (%), Wind Speed (km/h).
- **Epidemiological Correlation**:
  - Dengue & Malaria vectors (*Aedes aegypti*, *Anopheles*) thrive at temperatures between 24°C–32°C combined with precipitation spikes exceeding 50 mm/week.
  - Avian Influenza outbreaks correlate with migratory waterfowl season during winter temperature dips.

### Explainable Outbreak Risk Alerts (`analysis/evidence_alerts.json`)
The system computes multi-factor risk scores and assigns one of three explicit evidence grades:
- `SUPPORTED`: Validated across clinical cases, vector presence, AND matching weather drivers.
- `NEEDS_REVIEW`: High clinical signal, but environmental or vector data is anomalous or incomplete.
- `LIMITED_EVIDENCE`: Isolated report without corroborating multi-stream evidence.

---

> ⚡ **Active Recall Checkpoint 4 (Graph & Climate)**
> 1. *What is the difference between a direct document-entity edge and a multi-hop semantic edge in our Knowledge Graph?*
> 2. *How does weather data contribute to explaining a disease alert in OneHealth Nexus?*
>
> <details>
> <summary>👉 Click to Reveal Model Answer & Viva Talking Points</summary>
>
> 1. **Document-Entity vs. Multi-Hop**: "A document-entity edge (e.g., `Document -> MENTIONS_DISEASE -> Nipah`) simply records co-occurrence in a text. A multi-hop semantic edge (e.g., `Fruit Bat -> HOST_RESERVOIR_OF -> Nipah Virus -> CAUSES_DISEASE -> Nipah Virus Disease -> REPORTED_IN -> Kerala`) forms a biomedical knowledge path that allows the system to trace transmission mechanisms across animal reservoirs and human cases."
> 2. **Weather in Disease Alerts**: "Pathogens and vectors have physiological thermal and moisture limits. For example, in our Kerala Dengue alert, the system checks whether the 14-day rainfall anomaly exceeded historical baselines, providing an environmental explanation for vector breeding rather than just reporting case numbers."
> </details>

---

## 6. Live Dashboard Walkthrough (The 8 Modules)

The interactive dashboard is built in Streamlit ([`dashboard/app.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/dashboard/app.py)). When presenting to examiners or audiences, walk through these 8 modules in this exact order:

```
┌────────────────────────────────────────────────────────────────────────┐
│               STREAMLIT DASHBOARD NAVIGATION SIDEBAR                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 🌐 System Overview & Telemetry                                      │
│    • 14,210 total records, 5,208 nodes, 16,031 relationships           │
│ 2. 🔬 Model Comparison (spaCy vs. PubMedBERT)                          │
│    • Interactive text extraction sandbox, confusion matrix, F1 metrics │
│ 3. 📜 Evidence-Grounded Provenance                                     │
│    • Search any entity to see its exact source sentence and PMID       │
│ 4. 🌦️ Environmental & Weather Intelligence                             │
│    • Longitudinal temperature and precipitation charts across 10 hubs  │
│ 5. 🚨 Explainable Outbreak Alerts                                      │
│    • Live risk cards with SUPPORTED / NEEDS_REVIEW status badges       │
│ 6. 🕸️ Interactive Knowledge Graph Explorer                            │
│    • Subgraph viewer filtering by disease, animal, and location        │
│ 7. 🔍 Entity Verification Engine                                       │
│    • Audit discrepancies between rule-based and neural predictions     │
│ 8. 🏗️ System Architecture & Workflow                                   │
│    • Full system flow diagrams and Big Data pipeline specs             │
└────────────────────────────────────────────────────────────────────────┘
```

### Presentation Script (How to Demo Live)
1. **Start on Module 1 (System Overview)**: Point to the telemetry banner: *"Here you can see our 14,210 harmonized records from WHO, PubMed, GBIF, WOAH, and Open-Meteo."*
2. **Move to Module 2 (Model Comparison)**: This is your technical centerpiece.
   - Show Table 1 (F1=0.8754 vs 0.8384).
   - Show Table 2 (Explain the Location 1.0 vs 0.6 win for BERT).
   - Click the **Interactive Sandbox**: Paste an example sentence (e.g., *"In 2021, cattle in Assam contracted Anthrax"*), click extract, and show both models predicting in real time!
3. **Move to Module 3 (Provenance)**: Filter for *"Nipah virus"*. Show the exact PubMed sentence from Kerala with PMID and year.
4. **Move to Module 5 (Explainable Alerts)**: Expand the *Kerala Nipah Virus Outbreak Alert*. Show the 4 evidence criteria: Human Clinical Cases (WHO), Fruit Bat Vectors (GBIF), Literature Evidence (PubMed), and Environmental Drivers (Open-Meteo).

---

## 7. Master Viva / Oral Defense Q&A Cheatsheet

Here are the exact questions professors, project guides, and external examiners will ask, along with the ideal academic responses:

### Q1: "Why did you fine-tune PubMedBERT instead of using general BERT or GPT-4?"
> **Answer**:  
> "General BERT (trained on Wikipedia and BookCorpus) suffers from severe out-of-vocabulary domain shift on biomedical terminology; it splits complex medical terms into arbitrary subwords. Microsoft's PubMedBERT was pretrained *from scratch* on PubMed abstracts and full-text articles, giving it a specialized biomedical vocabulary. We preferred local fine-tuning over closed-source LLMs (like GPT-4) because epidemiological surveillance requires:
> 1. Complete reproducibility without model drift.
> 2. Zero per-token API costs over 14,000+ records.
> 3. Zero latency dependency on external cloud providers.
> 4. Deterministic token classification with exact BIO span boundaries."

### Q2: "Why is Pipeline A's overall F1 higher than PubMedBERT?"
> **Answer**:  
> "Our evaluation dataset contains established zoonotic diseases and pathogens. Pipeline A utilizes curated domain lexicons with canonical concept mapping and word-boundary regex enforcement. When evaluating recognized diseases and pathogens, exact dictionary mapping achieves near-zero false positives. PubMedBERT's subword tokenization occasionally split complex acronyms (*H5N1* -> *H*, *##5*, *##N*, *##1*), resulting in boundary penalties. However, on open-vocabulary concepts like previously unseen geographic locations, PubMedBERT significantly outperformed Pipeline A (1.0000 vs. 0.6000 F1)."

### Q3: "How did you ensure there is no data leakage during model evaluation?"
> **Answer**:  
> "We split our 48 annotated biomedical sentences using strict held-out partitioning: 70% training (33 sentences), 15% validation (7 sentences), and 15% held-out test (8 sentences, 132 tokens). Neither model had seen the test split during training, dictionary curation, or hyperparameter tuning. Both models were evaluated on the exact same token-level test set using standard `seqeval` token and entity classification metrics."

### Q4: "How does your Knowledge Graph handle contradictory information from different sources?"
> **Answer**:  
> "Our verification engine (`src/verification_engine.py`) cross-references statements across three tiers: clinical reports, peer-reviewed literature, and biodiversity occurrence. Instead of blindly merging contradictory nodes, the graph maintains separate provenance links in `entity_provenance.csv`. If a disease-vector connection is mentioned in PubMed but contradicted by WHO, the alert engine classifies it as `NEEDS_REVIEW` rather than `SUPPORTED`, flagging the discrepancy for human epidemiologists."

### Q5: "What makes your alert system 'explainable' compared to traditional ML classifiers?"
> **Answer**:  
> "Traditional ML classifiers output an arbitrary probability score (e.g., 'Risk: 0.87') without reasoning. OneHealth Nexus generates alerts backed by four explicit evidentiary pillars:
> 1. Clinical verification (WHO outbreak report ID).
> 2. Documented host reservoir presence (GBIF geocodes).
> 3. Literature citation (PubMed PMID and exact sentence).
> 4. Meteorological trigger (Open-Meteo precipitation/temperature anomaly).  
> The user can click any alert to inspect the underlying graph subgraph and source sentences."

---

## 8. Complete Project File Map & Code References

Use this index to quickly locate and open any file in the repository:

| Module / Component | File Path | Description & Role |
|---|---|---|
| **Streamlit Dashboard** | [`dashboard/app.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/dashboard/app.py) | Full 8-module interactive surveillance dashboard |
| **Streamlit Entrypoint** | [`app.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/app.py) | Root entrypoint for Streamlit Community Cloud |
| **Comparative Report** | [`COMPARATIVE_ANALYSIS_REPORT.md`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/COMPARATIVE_ANALYSIS_REPORT.md) | Formal academic evaluation report of NLP models |
| **End-Term Tracker** | [`END_TERM_DEVELOPMENT_PLAN.md`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/END_TERM_DEVELOPMENT_PLAN.md) | Milestone tracker verifying 10 end-term objectives |
| **Automated Test Suite** | [`tests/test_end_to_end.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/tests/test_end_to_end.py) | 6-tier validation suite (14,210 records, KG, NLP) |
| **Existing NLP Engine** | [`nlp/entity_extraction.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/nlp/entity_extraction.py) | Pipeline A: Regex, word-boundary, concept mapping |
| **PubMedBERT Engine** | [`nlp/pubmedbert_ner.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/nlp/pubmedbert_ner.py) | Pipeline B: Fine-tuned transformer token classifier |
| **Benchmark Runner** | [`nlp/model_comparison.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/nlp/model_comparison.py) | Executes head-to-head evaluation & saves metrics |
| **Evaluation Dataset** | [`data/evaluation/biomedical_ner_dataset.json`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/data/evaluation/biomedical_ner_dataset.json) | 48 annotated sentences with 11 BIO tags |
| **Benchmark Results** | [`data/evaluation/model_comparison_results.json`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/data/evaluation/model_comparison_results.json) | Precision, recall, F1, latency, confusion matrices |
| **PubMedBERT Weights** | [`models/pubmedbert_ner/`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/models/pubmedbert_ner/) | Fine-tuned `model.safetensors` (via Git LFS), tokenizer, config |
| **Alert Engine** | [`src/alert_engine.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/src/alert_engine.py) | Generates explainable multi-source outbreak alerts |
| **Verification Engine**| [`src/verification_engine.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/src/verification_engine.py) | Cross-references human, animal, and climate streams |
| **Incremental Engine** | [`src/incremental_pipeline.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/src/incremental_pipeline.py) | SHA-256 state tracking preventing duplicate runs |
| **Weather Collector**  | [`src/weather_collector.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/src/weather_collector.py) | Open-Meteo API ingestion for 10 surveillance zones |
| **Animal Collector**   | [`src/animal_health_collector.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/src/animal_health_collector.py) | Standardizes WOAH WAHIS & FAO veterinary reports |
| **KG Nodes**           | [`knowledge_graph/nodes.csv`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/knowledge_graph/nodes.csv) | 5,208 graph nodes with labels and metadata |
| **KG Relationships**   | [`knowledge_graph/relationships.csv`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/knowledge_graph/relationships.csv) | 16,031 directed semantic and provenance edges |
| **KG Provenance**      | [`knowledge_graph/entity_provenance.csv`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/knowledge_graph/entity_provenance.csv) | 26,024 sentence-level context records |
| **Visual Comparison**  | [`analysis/model_comparison_metrics.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/analysis/model_comparison_metrics.png) | High-resolution comparative bar charts |
| **Active Alerts**      | [`analysis/evidence_alerts.json`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/analysis/evidence_alerts.json) | 6 generated explainable surveillance alerts |
| **PowerShell Orchestration** | [`run_all.ps1`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus-2/run_all.ps1) | Single-click end-to-end execution script |

---

### Quick Commands for Live Demonstration

```powershell
# 1. Run the entire automated test suite (takes ~5 seconds)
.\.venv\Scripts\python.exe tests/test_end_to_end.py

# 2. Run the head-to-head NLP evaluation benchmark
.\.venv\Scripts\python.exe nlp/model_comparison.py

# 3. Launch the 8-module Streamlit Surveillance Dashboard
.\.venv\Scripts\streamlit.exe run dashboard/app.py
```
