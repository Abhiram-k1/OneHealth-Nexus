# PSEUDO.md — Capstone Plain-Language Guide & Viva Cheatsheet

**Project Title:** OneHealth Nexus: Large-Scale NLP and Temporal Knowledge Graphs for Emerging Disease Intelligence  
**Course:** Text Analytics (TA) & Big Data Analytics (BDA) — B.Tech AI & Data Science (Sem-5 / UG-III)  
**Institution:** Amrita Vishwa Vidyapeetham, Delhi NCR Campus, Faridabad  
**Department:** Department of Artificial Intelligence and Data Science  
**Faculty Coordinators:** Dr. Ranjit Panigrahi (Associate Professor) & Dr. Barkha Singh (Assistant Professor)  
**Team Members:** Anagha Manoj (`DL.AI.U4AID24105`), Mimansha Goyal (`DL.AI.U4AID24123`), Tanvi Bhardwaj (`DL.AI.U4AID24136`), Kundurthi Abhiram (`DL.AI.U4AID24144`)  
**Purpose:** This document explains the entire implemented system in simple, layman-friendly language. It allows you to explain every concept, pipeline stage, design decision, mathematical formula, and empirical result clearly in an exam, presentation, or viva without needing to read raw code.

---

# PART 1: THE BIG PICTURE

### What is this project about?
**OneHealth Nexus** is an intelligent disease surveillance system that bridges the gap between **human health**, **animal biology**, and **environmental geography**. 
- Over **70% of emerging infectious diseases** in humans (such as COVID-19, Avian Influenza / Bird Flu, Nipah, Ebola, and Mpox) are **zoonotic** — meaning they jump from animals (wildlife or livestock) to human beings.
- When an outbreak happens, signs and clues are published in different places:
  1. Doctors and public health agencies report human clinical symptoms in text bulletins (like the **World Health Organization Disease Outbreak News**).
  2. Biomedical researchers publish findings about viruses, mutations, and animal hosts in scientific journals (like **PubMed / NCBI**).
  3. Wildlife ecologists track where animal species, birds, and bats live in biodiversity databases (like the **Global Biodiversity Information Facility — GBIF**).
- In the real world, these three data streams exist in completely isolated "silos". Medical researchers don't look at biodiversity maps every day, and ecologists don't monitor clinical hospital admissions.
- By the time anyone realizes that a sick bat in a forest is carrying a virus that matches a patient in a nearby hospital, weeks have passed and an epidemic has already begun.

### What is our solution?
We built **OneHealth Nexus** — an end-to-end Big Data and Text Analytics pipeline that:
1. Automatically collects data from **WHO**, **PubMed**, and **GBIF**.
2. Cleans and deduplicates the massive text corpus using **Apache Spark 4.0.1** and **Scala 2.13.16** to demonstrate industrial big data scalability.
3. Uses Natural Language Processing (**spaCy**) to read the medical texts like a human doctor would, automatically identifying diseases, viruses, animal hosts, locations, and dates.
4. Constructs an interconnected **Temporal Knowledge Graph** using **NetworkX** containing **1,620 nodes** and **2,611 semantic relationships**.
5. Performs **Temporal Analysis** (tracking how disease mentions surge over the years) and **Spatial Analysis** (mapping animal occurrences across India).
6. Calculates a transparent, multi-factor **Emerging Signal Indicator** that ranks which diseases are showing abnormal recent surges across diverse sources.
7. Presents all intelligence inside an interactive, publication-grade **Streamlit Dashboard** with 7 synchronized modules.

### Key Numbers at a Glance (Memorize for Viva!)
- **Raw Data Ingested:** 50 WHO Outbreak Reports + 1,000 PubMed Research Articles + 300 GBIF Animal Occurrences in India.
- **Spark Preprocessed Corpus:** Exactly **592 verified unique documents** (1,003,729 bytes).
- **Knowledge Graph Scale:** Exactly **1,620 nodes** and **2,611 directed relationships**.
- **Graph Breakdown:** 557 Documents, 544 Dates, 470 Locations, 21 Animals, 17 Diseases, 11 Pathogens.
- **Geographic Bounds (India):** Latitude $8.48^\circ\text{ N}$ to $31.42^\circ\text{ N}$, Longitude $71.68^\circ\text{ E}$ to $94.63^\circ\text{ E}$.
- **Top Detected Signal:** **Influenza** (Score: 84.06) and **Avian Influenza / Bird Flu** (Score: 81.67).

---

# PART 2: STEP-BY-STEP IMPLEMENTATION PIPELINE

---

## STEP 1 — MULTI-SOURCE HETEROGENEOUS DATA COLLECTION

### What are we doing?
We harvest data from three completely different external APIs, representing the three sides of the One Health triangle:
1. **WHO Disease Outbreak News (DONs):** Captures real-world clinical outbreak reports.
2. **PubMed (NCBI Entrez E-Utilities):** Captures peer-reviewed biomedical literature on zoonoses and spillover.
3. **GBIF (Global Biodiversity Information Facility):** Captures animal occurrence records with exact GPS coordinates.

### Why are we doing it?
If you only look at hospital data, you only see the disease *after* humans get sick. If you look at PubMed, you understand *how* the pathogen behaves in a lab. If you look at GBIF, you see *where* the animal hosts live. Bringing all three together is the fundamental definition of the **One Health** surveillance paradigm endorsed by the WHO, FAO, UNEP, and WOAH.

### How does it work?
- In Python / Google Colab (`notebooks/TA_AND_BDA_PROJECT.ipynb`), we created robust API wrappers with exponential backoff retries (`request_with_retry`) to handle network timeouts and rate limits.
- **WHO Ingestion:** Queries the WHO API endpoint, extracts title, publication date, overview, epidemiology, public health assessment, and response measures. Retained 50 diverse outbreak records.
- **PubMed Ingestion:** Queries NCBI E-Utilities (`esearch` and `efetch`) using boolean keyword queries: `"One Health" OR "Zoonotic disease" OR "Zoonoses" OR "Emerging infectious disease" OR "Spillover"`. Fetches batches via XML parsing, extracting PMID, title, abstract, publication year, and journal.
- **GBIF Ingestion:** Queries GBIF API (`v1/occurrence/search`) filtered to `country=IN` (India), `kingdom=Animalia`, and `hasCoordinate=true`. Retained 300 verified species occurrences with coordinates, species taxonomy, and locality.

### What comes out?
Three raw CSV files saved in `data/raw/`:
- `who_outbreaks.csv` (235 KB, 50 outbreak bulletins)
- `pubmed.csv` (993 KB, 1,000 biomedical articles)
- `gbif.csv` (67.5 KB, 300 animal coordinate records)

---

## STEP 2 — INITIAL NORMALIZATION & DATA CLEANING

### What are we doing?
We clean messy web texts (removing HTML tags, XML entities, corrupted encodings, newline characters) and merge WHO reports and PubMed abstracts into a single, unified document schema.

### Why is this critical?
Scientific abstracts and WHO bulletins come from different web services with disparate formats. PubMed has XML tags like `<i>`, `<b>`, `<abstracttext>`, while WHO has HTML formatting like `&amp;`, `&nbsp;`, `<p>`. If you feed dirty text into NLP or Spark, your entity extraction will pick up garbage tokens (like "nbsp" as a disease name!).

### How does it work?
- Implemented a custom sanitization pipeline `clean_text(text)`:
  1. Strips HTML/XML markup using regular expressions `re.sub(r"<[^>]+>", " ", text)`.
  2. Decodes HTML entities (e.g., `&amp;` becomes `&`, `&lt;` becomes `<`) using `html.unescape`.
  3. Replaces carriage returns, line breaks, and tabs with single spaces.
  4. Removes non-ASCII junk while retaining essential punctuation (periods, hyphens, commas).
  5. Drops records where the cleaned text length is zero.
- Merges the datasets into a 4-column canonical schema:
  $$\text{Schema} = \left[ \text{document\_id}, \text{source}, \text{date}, \text{clean\_text} \right]$$

### What comes out?
- `data/processed/cleaned_documents.csv` (2.34 MB, unified document corpus)
- `data/processed/cleaned_gbif.csv` (67.5 KB, validated geospatial records)
- `data/processed/data_summary.csv` (Audit log of record counts)

---

## STEP 3 — DISTRIBUTED BIG DATA PROCESSING (APACHE SPARK + SCALA)

### What are we doing?
We execute large-scale, resilient text processing using **Apache Spark 4.0.1** and **Scala 2.13.16**, compiled via the Scala Build Tool (**sbt**).

### Why do we use Spark and Scala instead of just Python Pandas?
- In real-world epidemiological surveillance (e.g., monitoring millions of electronic health records, Twitter/X feeds, and millions of PubMed papers), single-machine Pandas crashes with `OutOfMemoryError`.
- Apache Spark is the industry standard for distributed computing. It breaks data into resilient partitions across a cluster and executes operations in parallel using Directed Acyclic Graphs (DAGs).
- Scala is Spark's native JVM language, offering static type safety, high execution speed, and zero serialization overhead compared to PySpark wrappers.
- In this academic project, we use Spark to demonstrate that our pipeline is enterprise-ready and capable of scaling to gigabytes or terabytes of streaming data.

### How does the Scala code work?
- File: `src/main/scala/OneHealthPreprocessing.scala`
- Build definition: `build.sbt` pulling dependencies:
  ```scala
  "org.apache.spark" %% "spark-core" % "4.0.1",
  "org.apache.spark" %% "spark-sql"  % "4.0.1"
  ```
- Execution flow:
  1. Initializes `SparkSession.builder().appName("OneHealth Nexus Preprocessing").master("local[*]").getOrCreate()`.
  2. Loads `cleaned_documents.csv` using Spark's distributed DataFrame reader.
  3. Applies distributed DataFrame transformations:
     ```scala
     val cleanedDF = df
       .filter(col("clean_text").isNotNull)
       .filter(length(trim(col("clean_text"))) > 0)
       .dropDuplicates("clean_text")
     ```
  4. Formats each record into a tab-separated text representation (`\t` delimiter prevents comma-splitting bugs inside text sentences).
  5. Writes the final corpus to disk.

### What comes out?
- Exactly **592 verified unique documents** saved in `data/processed/spark_output/processed_documents.txt` (1,003,729 bytes).
- All duplicates and malformed entries are completely eliminated.

---

## STEP 4 — BIOMEDICAL NATURAL LANGUAGE PROCESSING (spaCy)

### What are we doing?
We run an NLP information extraction engine (`nlp/entity_extraction.py`) on each of the 592 Spark-processed documents to identify real-world medical and ecological entities.

### What entities are extracted?
1. **Diseases:** Influenza, Avian Influenza (Bird Flu), COVID-19, Coronavirus, Dengue, Malaria, Cholera, Ebola, Mpox (Monkeypox), Rabies, Tuberculosis, Typhoid, Measles, Nipah, Hepatitis.
2. **Pathogens:** Virus, Influenza virus, Coronavirus, SARS-CoV-2, H5N1, H7N9, Bacteria, Parasite, Fungus.
3. **Animal Hosts:** Bird, Poultry, Chicken, Duck, Pig, Swine, Bat, Dog, Cat, Cattle, Cow, Livestock, Horse, Goat, Sheep, Wildlife.
4. **Geographic Locations (GPE):** Countries, regions, and cities extracted via spaCy NER (e.g., India, China, Egypt, Indonesia, Vietnam, Kerala).
5. **Dates:** Temporal references (e.g., "2024", "February 2026", "2024-03-12").
6. **Documents:** The root source document ID (e.g., `WHO_12`, `PUBMED_42714421`).

### How does it work?
- We combine statistical machine learning NER with curated biomedical lexicons:
  - **spaCy's `en_core_web_sm` pipeline** uses a Convolutional Neural Network (CNN) with transition-based parsing to identify geopolitical entities (`GPE` $\rightarrow$ `Location`) and temporal mentions (`DATE` $\rightarrow$ `Date`).
  - **Domain Lexicon Matcher** scans the text for specialized disease names, pathogen strains, and animal species to ensure 100% precision on critical epidemiological vocabulary.
- For every detected entity, the script assigns a stable integer `node_id` and records the relationship between the document and the entity:
  - `(Document) —[ MENTIONS_DISEASE ]—> (Disease)`
  - `(Document) —[ MENTIONS_PATHOGEN ]—> (Pathogen)`
  - `(Document) —[ MENTIONS_ANIMAL ]—> (Animal)`
  - `(Document) —[ MENTIONS_LOCATION ]—> (Location)`
  - `(Document) —[ HAS_DATE ]—> (Date)`

### What comes out?
- `knowledge_graph/nodes.csv` (1,620 rows, columns: `node_id, name, type, source`)
- `knowledge_graph/relationships.csv` (2,611 rows, columns: `source, target, relationship`)

---

## STEP 5 — KNOWLEDGE GRAPH MODELING (NetworkX)

### What are we doing?
We transform the isolated entity lists into a connected, multi-relational **Directed Knowledge Graph** ($G = (V, E)$) using the **NetworkX** graph computing library (`knowledge_graph/build_graph.py`).

### Why do we need a Knowledge Graph instead of a regular SQL database?
- In a SQL relational database, finding a connection between an animal in Kerala and a virus reported by the WHO requires 4 or 5 expensive table `JOIN` operations.
- In a Knowledge Graph, relationships are first-class citizens. You can traverse paths in $O(1)$ time per edge.
- You can ask questions like: *"Which animal hosts are connected to diseases that are also reported in India?"*
  $$\text{India} \xleftarrow{\text{LOCATION}} \text{Document} \xrightarrow{\text{DISEASE}} \text{Avian Influenza} \xleftarrow{\text{ANIMAL}} \text{Poultry}$$
- This directly reveals zoonotic spillover bridges that are impossible to spot in flat spreadsheets.

### How does it work?
- Creates a directed graph: `G = nx.DiGraph()`.
- Loops through all 1,620 nodes and inserts them with metadata attributes (`name`, `type`, `source`).
- Loops through all 2,611 relationships, validates that both source and target exist, and adds directed edges with relationship labels.
- Calculates network topological properties:
  - **In-Degree ($k_{in}$):** How many documents point to this entity (e.g., an entity with high in-degree like "Influenza" is a major disease hub).
  - **Out-Degree ($k_{out}$):** How many entities a document mentions.
  - **Degree Centrality ($C_D(v)$):** Fraction of all nodes connected to node $v$:
    $$C_D(v) = \frac{\text{degree}(v)}{|V| - 1} = \frac{\text{degree}(v)}{1619}$$
  - **Graph Density ($D$):** Ratio of actual edges to maximum possible edges:
    $$D = \frac{|E|}{|V|(|V| - 1)} = \frac{2611}{1620 \times 1619} \approx 0.0009955$$
- Renders and exports a high-resolution subgraph visual (`onehealth_subgraph.png`) highlighting the core One Health hubs.

### What comes out?
- `knowledge_graph/graph_summary.csv` (Global topological metrics: 1,620 nodes, 2,611 edges, density 0.0009955)
- `knowledge_graph/important_entities.csv` (Ranked list of top hub entities by degree)
- `knowledge_graph/onehealth_subgraph.png` (Visual network diagram)
- `knowledge_graph/load_neo4j.py` (Script to load the graph into a production Neo4j database if desired)

---

## STEP 6 — TEMPORAL INTELLIGENCE & LONGITUDINAL TRENDS

### What are we doing?
We analyze how disease mentions and outbreak records evolve across time (`analysis/temporal_analysis.py`).

### Why is this important?
Diseases are not static. A disease mentioned 10 times in 2022 might be under control, but a disease mentioned 10 times in the last 30 days is a potential outbreak emergency. By extracting the time dimension, we can distinguish historical background noise from sudden emerging surges.

### How does it work?
- Parses document publication dates using `pd.to_datetime(df["date"], errors="coerce", utc=True)`.
- Filters out records with unparseable dates.
- Extracts calendar years and aggregates document counts:
  $$\text{Count}(y) = \sum_{d \in \text{Docs}} \mathbb{I}(\text{Year}(d) = y)$$
- Generates a temporal distribution across the corpus:
  - The collected corpus spans from 2024 through 2027, with the largest concentration of contemporary documents in 2026 (464 documents).
- Plots a longitudinal curve showing document density over time.

### What comes out?
- `analysis/temporal_summary.csv` (Year vs document count)
- `analysis/temporal_trend.png` (Publication trend graph)

---

## STEP 7 — SPATIAL BIODIVERSITY INTELLIGENCE (GBIF INDIA)

### What are we doing?
We analyze and map the geographic distribution of animal hosts and wildlife vectors across India using GBIF biodiversity occurrence data (`analysis/spatial_analysis.py`).

### Why is this important?
A pathogen cannot cause a zoonotic spillover unless its animal reservoir actually lives in that geographic area. For example, if Kyasanur Forest Disease (KFD) is carried by monkeys and ticks, knowing the spatial density of primates in Karnataka and Goa helps public health officials anticipate risk zones before cases appear in humans.

### How does it work?
- Ingests `data/processed/cleaned_gbif.csv`.
- Validates latitude and longitude columns using numerical coercion.
- Verifies that all 300 records have valid geographic coordinates located within India:
  - Minimum Latitude: **$8.484364^\circ\text{ N}$** (near Kanyakumari, Tamil Nadu)
  - Maximum Latitude: **$31.420114^\circ\text{ N}$** (Punjab / Himachal Pradesh border)
  - Minimum Longitude: **$71.676322^\circ\text{ E}$** (Gujarat / western border)
  - Maximum Longitude: **$94.628057^\circ\text{ E}$** (Assam / Arunachal Pradesh)
- Generates a geographic scatter visualization plotting animal species occurrences across the Indian subcontinent.

### What comes out?
- `analysis/spatial_summary.csv` (Geographic coordinate bounds and valid counts)
- `analysis/spatial_distribution.png` (Spatial distribution scatter plot)

---

## STEP 8 — EMERGING SIGNAL DETECTION HEURISTIC

### What are we doing?
We compute an analytical **Emerging Signal Indicator** (`analysis/emerging_signals.py`) that scans the processed corpus for 17 major infectious diseases and ranks which ones pose the highest potential risk.

### Why do we need this indicator?
Public health officials receive thousands of papers and news alerts every month. They cannot read everything. They need a prioritization score that highlights: *"Which disease is showing sudden recent spikes, appears across multiple independent sources, and has significant mention volume?"*

### How does the formula work?
For each disease $i$, we compute three sub-scores and combine them with weighted linear combination:

$$\text{Signal Score}_i = \left( 0.5 \times \text{Recency}_i + 0.3 \times \text{Diversity}_i + 0.2 \times \text{Volume}_i \right) \times 100$$

1. **Recency Score ($R_i$, Weight = 0.5):**
   What fraction of the disease's total mentions occurred recently (defined as $\ge \text{Year}_{\max} - 1$)?
   $$R_i = \frac{M_{i, \text{recent}}}{M_{i, \text{total}}}$$
   *(If all mentions are brand new, $R_i = 1.0$. If mentions are from years ago, $R_i \to 0$.)*

2. **Source Diversity Score ($D_i$, Weight = 0.3):**
   How many distinct sources (WHO, PubMed, etc.) report this disease?
   $$D_i = \min\left(\frac{S_i}{3}, 1.0\right)$$
   *(If a disease is only reported in one blog, diversity is low. If both WHO and PubMed confirm it, diversity is high!)*

3. **Mention Volume Score ($V_i$, Weight = 0.2):**
   What is the absolute volume of activity (normalized against an activity threshold of 20 mentions)?
   $$V_i = \min\left(\frac{M_{i, \text{total}}}{20}, 1.0\right)$$

### What are the actual results?
| Rank | Disease Name | Total Mentions | Recent Mentions | Sources | Score | Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **1** | **Influenza** | 17 | 16 | 2 | **84.06** | 🔴 HIGH ALERT |
| **2** | **Avian Influenza** | 15 | 14 | 2 | **81.67** | 🔴 HIGH ALERT |
| **3** | **Rabies** | 13 | 13 | 1 | **73.00** | 🟠 ELEVATED |
| **4** | **COVID-19** | 8 | 8 | 1 | **68.00** | 🟡 MODERATE |
| **5** | **Tuberculosis** | 7 | 7 | 1 | **67.00** | 🟡 MODERATE |
| **6** | **Ebola** | 6 | 6 | 1 | **66.00** | 🟡 MODERATE |
| **7** | **Dengue** | 6 | 6 | 1 | **66.00** | 🟡 MODERATE |
| **8** | **Nipah** | 5 | 5 | 1 | **65.00** | 🟡 MODERATE |
| **9** | **Mpox** | 4 | 4 | 1 | **64.00** | 🟢 MONITORED |
| **10** | **Cholera / Measles** | 1 | 1 | 1 | **61.00** | 🟢 BASELINE |

> **Important Viva Note:** Always explain that this is a **transparent project heuristic** designed for prioritization and triage, NOT a clinical diagnosis or official epidemiological outbreak forecast.

### What comes out?
- `analysis/emerging_signals.csv` (Ranked table of signals, sub-scores, and metadata)

---

## STEP 9 — INTERACTIVE STREAMLIT DASHBOARD (UI)

### What are we doing?
We bring all the outputs from Spark, spaCy, NetworkX, and Pandas into an interactive web dashboard (`dashboard/app.py`).

### What does the dashboard contain?
The application is structured into **7 interactive pages**:
1. **🏠 Intelligence Overview:**
   - Dark-navy hero header with glassmorphism effects.
   - 4 main KPI metric cards: **592 Processed Documents**, **1,620 Knowledge Nodes**, **2,611 Relationships**, **300 GBIF Biodiversity Records**.
   - Red banner highlighting the Top Emerging Signal: **Influenza / Avian Influenza (Score: 84.06)**.
   - Interactive 4-step architecture overview.
2. **🚨 Emerging Signals:**
   - Ranked alert cards for all 17 analyzed diseases.
   - Colored visual indicator bars showing recency vs diversity vs volume contributions.
3. **📈 Temporal Intelligence:**
   - Interactive Plotly line charts displaying longitudinal trends.
   - Tabular view of document frequency grouped by calendar year.
4. **🌎 Spatial Intelligence:**
   - Interactive Plotly scatter plot mapping 300 animal species occurrences across India.
   - Geographic summary table showing minimum/maximum latitude and longitude.
5. **🕸️ Knowledge Graph:**
   - Display of the NetworkX knowledge graph visualization (`onehealth_subgraph.png`).
   - Interactive data table of top entities ranked by connectivity (Degree Centrality).
6. **🧬 Entity Intelligence:**
   - Interactive entity breakdown tabs: Diseases, Pathogens, Animal Hosts, Locations, and Dates.
7. **🔬 Methodology:**
   - Plain-language explanation of the One Health framework, data collection parameters, Spark Big Data processing steps, NLP extraction rules, and legal/epidemiological disclaimers.

---

# PART 3: ARCHITECTURE & DATA LINEAGE DIAGRAMS

### Complete Data Flow Diagram
```
[WHO API (50 Outbreaks)]   [PubMed API (1,000 Papers)]   [GBIF API (300 Animal Records)]
            │                            │                               │
            └─────────────┬──────────────┘                               │
                          ▼                                              │
              [ Colab Data Ingestion ]                                   │
              [ & Regex Text Cleaning ]                                  │
                          │                                              │
                          ▼                                              │
             cleaned_documents.csv (2.34 MB)                    cleaned_gbif.csv (67.5 KB)
                          │                                              │
                          ▼                                              │
          ┌───────────────────────────────┐                              │
          │     APACHE SPARK + SCALA      │                              │
          │   OneHealthPreprocessing.scala│                              │
          │ Distributed Filter & Deduplicate                              │
          └───────────────┬───────────────┘                              │
                          ▼                                              │
           processed_documents.txt (592 docs)                            │
                          │                                              │
                          ▼                                              │
          ┌───────────────────────────────┐                              │
          │      PYTHON + spaCy (NLP)     │                              │
          │     entity_extraction.py      │                              │
          │  Extract: Disease, Pathogen,  │                              │
          │  Animal, Location, Date       │                              │
          └───────────────┬───────────────┘                              │
                          ▼                                              │
               nodes.csv & relationships.csv                             │
                          │                                              │
                          ▼                                              │
          ┌───────────────────────────────┐                              │
          │    NETWORKX KNOWLEDGE GRAPH   │                              │
          │        build_graph.py         │                              │
          │   1,620 Nodes | 2,611 Edges   │                              │
          └───────────────┬───────────────┘                              │
                          │                                              │
             ┌────────────┴────────────┐                                 │
             ▼                         ▼                                 ▼
   [ Temporal Analysis ]    [ Emerging Signals ]              [ Spatial Analysis ]
   (temporal_analysis.py)   (emerging_signals.py)             (spatial_analysis.py)
   temporal_trend.png       emerging_signals.csv              spatial_distribution.png
             │                         │                                 │
             └─────────────────────────┼─────────────────────────────────┘
                                       ▼
                       ┌───────────────────────────────┐
                       │      STREAMLIT DASHBOARD      │
                       │        dashboard/app.py       │
                       │  7-Page Live Intelligence App │
                       └───────────────────────────────┘
```

---

# PART 4: EMPIRICAL ARTIFACTS & METRICS SUMMARY TABLE

| Pipeline Layer | Primary Technology | Exact Metric / Number | Generated Artifact File |
|---|---|---|---|
| **Raw WHO Data** | Python `requests` | **50 Outbreak DONs** | `data/raw/who_outbreaks.csv` |
| **Raw PubMed Data** | NCBI Entrez API | **1,000 Articles** | `data/raw/pubmed.csv` |
| **Raw GBIF Data** | GBIF Occurrence API | **300 Occurrences** | `data/raw/gbif.csv` |
| **Cleaned Documents** | Python RegEx | **2.34 MB Corpus** | `data/processed/cleaned_documents.csv` |
| **Spark Preprocessing** | **Apache Spark 4.0.1 + Scala** | **592 Unique Documents** | `data/processed/spark_output/processed_documents.txt` |
| **Total Graph Nodes** | NetworkX `DiGraph` | **1,620 Nodes** | `knowledge_graph/nodes.csv` |
| **Total Relationships** | NetworkX `DiGraph` | **2,611 Relationships** | `knowledge_graph/relationships.csv` |
| **Document Nodes** | Node Type Breakdown | 557 Nodes | `knowledge_graph/graph_summary.csv` |
| **Date Nodes** | Node Type Breakdown | 544 Nodes | `knowledge_graph/graph_summary.csv` |
| **Location Nodes** | Node Type Breakdown | 470 Nodes | `knowledge_graph/graph_summary.csv` |
| **Animal Nodes** | Node Type Breakdown | 21 Nodes | `knowledge_graph/graph_summary.csv` |
| **Disease Nodes** | Node Type Breakdown | 17 Nodes | `knowledge_graph/graph_summary.csv` |
| **Pathogen Nodes** | Node Type Breakdown | 11 Nodes | `knowledge_graph/graph_summary.csv` |
| **Graph Density** | Topological Metric | **0.0009955** | `knowledge_graph/graph_summary.csv` |
| **Geographic Validation**| India Bounding Box | **300 Coordinates Validated** | `analysis/spatial_summary.csv` |
| **Latitude Range** | Geodetic Coordinates | $8.484^\circ\text{ N} - 31.420^\circ\text{ N}$ | `analysis/spatial_summary.csv` |
| **Longitude Range** | Geodetic Coordinates | $71.676^\circ\text{ E} - 94.628^\circ\text{ E}$ | `analysis/spatial_summary.csv` |
| **Top Signal Detected** | Emerging Signal Heuristic | **Influenza (84.06)** | `analysis/emerging_signals.csv` |
| **Second Top Signal** | Emerging Signal Heuristic | **Avian Influenza (81.67)** | `analysis/emerging_signals.csv` |
| **Dashboard Interface** | Streamlit + Plotly | **7 Integrated Modules** | `dashboard/app.py` |

---

# PART 5: VIVA & PRESENTATION CHEATSHEET (COMMON QUESTIONS & ANSWERS)

### Q1: What is the main objective of this project?
**Answer:** The objective of **OneHealth Nexus** is to break down the information silos between human health, animal biology, and environmental data. By combining Apache Spark for distributed big data processing, spaCy for biomedical NLP, NetworkX for temporal knowledge graph construction, and Streamlit for interactive visualization, our system connects disease reports, animal hosts, and geographic locations to identify emerging infectious disease signals early.

### Q2: Why is the "One Health" approach so important?
**Answer:** More than 70% of emerging infectious diseases in humans are zoonotic — meaning they originate in animals before jumping to humans (e.g., COVID-19, Avian Flu, Nipah, Ebola). Traditional surveillance systems only monitor humans in hospitals after an outbreak has already started. One Health connects clinical outbreak data (WHO), biomedical literature (PubMed), and animal/vector biodiversity records (GBIF) to detect risks before human transmission escalates.

### Q3: Why did you use Apache Spark + Scala instead of doing everything in Python Pandas?
**Answer:** While Pandas is convenient for small prototypes, it runs strictly in memory on a single CPU core. In national or global disease surveillance, datasets consist of millions of medical records, genomic sequences, and literature feeds, which would cause an `OutOfMemoryError` in Pandas. Apache Spark distributes the computations across a cluster using resilient distributed datasets (RDDs) and DataFrames. We used **Scala 2.13.16** because it is Spark's native JVM language, offering high performance, static type checking, and zero Python-to-JVM serialization overhead.

### Q4: How did you get from raw records to 592 documents?
**Answer:** We collected 50 WHO Outbreak News reports and 1,000 PubMed scientific abstracts. In Google Colab, we merged them into a common schema. Then, Apache Spark loaded the corpus, filtered out null texts, removed empty whitespace strings, and performed distributed deduplication using `dropDuplicates("clean_text")`. This produced exactly **592 verified, clean, non-duplicate documents**.

### Q5: How does your NLP pipeline extract entities and relationships?
**Answer:** We used **spaCy's `en_core_web_sm`** convolutional model combined with custom biomedical regular expression matchers:
- spaCy's statistical NER extracts **Locations** (`GPE`) and **Dates** (`DATE`).
- Domain-specific lexicons extract **Diseases** (e.g., Influenza, Ebola, Nipah), **Pathogens** (e.g., H5N1, Coronavirus, Bacteria), and **Animal Hosts** (e.g., Poultry, Bats, Cattle).
- The pipeline creates directed relationships connecting each `Document` to the entities it mentions (`MENTIONS_DISEASE`, `MENTIONS_ANIMAL`, `MENTIONS_LOCATION`, `HAS_DATE`).

### Q6: What are the key metrics of your Knowledge Graph?
**Answer:** The knowledge graph contains:
- **1,620 Nodes** and **2,611 Directed Relationships**.
- **Nodes Breakdown:** 557 Documents, 544 Dates, 470 Locations, 21 Animals, 17 Diseases, and 11 Pathogens.
- **Graph Density:** $0.0009955$, indicating a typical real-world sparse information network where specific key nodes (like "Influenza" and "India") act as dense hubs with high degree centrality.

### Q7: Why is a Knowledge Graph better than a relational SQL table for this task?
**Answer:** In SQL, connecting a disease in a clinical report to an animal host species in a biodiversity database requires multiple expensive `JOIN` operations across several tables. In a Knowledge Graph, relationships are stored as direct pointers. We can traverse multi-hop paths like:
$$\text{Location} \longleftarrow \text{Document} \longrightarrow \text{Disease} \longleftarrow \text{Document} \longrightarrow \text{Animal Host}$$
This enables instant discovery of cross-species transmission pathways that are virtually impossible to see in tabular databases.

### Q8: How did you handle the temporal (time) dimension?
**Answer:** We parsed publication and report dates into standardized ISO datetime formats and grouped them by calendar year. Our temporal analysis revealed how disease mentions fluctuate over time, with 464 documents concentrated in 2026 reflecting the most current literature, alongside historical baselines from 2024 and 2025. This temporal tracking allows the system to distinguish between old background research and sudden current surges.

### Q9: What data is used for Spatial Analysis and why?
**Answer:** We used **GBIF (Global Biodiversity Information Facility)** animal occurrence data for India. We validated 300 records with exact latitude and longitude coordinates. The coordinates span Latitude $8.48^\circ\text{ N}$ to $31.42^\circ\text{ N}$ and Longitude $71.68^\circ\text{ E}$ to $94.62^\circ\text{ E}$, confirming complete geographical coverage of the Indian subcontinent. This spatial layer lets us cross-reference where potential disease reservoir animals (like wild birds and bats) actually live.

### Q10: How does the Emerging Signal Detection formula work?
**Answer:** The signal score is a transparent weighted heuristic calculated for each disease:
$$\text{Signal Score} = \left( 0.5 \times \text{Recency} + 0.3 \times \text{Source Diversity} + 0.2 \times \text{Mention Volume} \right) \times 100$$
- **Recency (50% weight):** Ratio of recent mentions ($\ge \text{Year}_{\max} - 1$) to total mentions. High recency indicates a sudden new surge.
- **Source Diversity (30% weight):** Number of distinct reporting sources (WHO vs PubMed). Multi-source confirmation filters out single-source false alarms.
- **Mention Volume (20% weight):** Absolute frequency normalized against an activity threshold of 20 mentions.

### Q11: Which disease scored the highest and why?
**Answer:** **Influenza** scored **84.06** and **Avian Influenza (Bird Flu)** scored **81.67**. They ranked highest because:
1. They appeared across multiple independent data sources (both WHO outbreak bulletins and PubMed scientific literature).
2. Almost all of their mentions occurred in the most recent time window.
3. They had the highest absolute frequency in the corpus (17 and 15 mentions respectively).

### Q12: Is your Emerging Signal Indicator an official outbreak prediction?
**Answer:** No. We explicitly state in our methodology and dashboard disclaimer that this score is an **analytical research heuristic for prioritization and triage**. It is designed to help analysts prioritize which literature to read first, not to replace official clinical diagnosis or certified epidemiological modeling.

### Q13: How is the Streamlit dashboard structured?
**Answer:** The Streamlit dashboard (`dashboard/app.py`) contains 7 synchronized modules:
1. **Intelligence Overview:** KPI cards, top signal banner, and architectural overview.
2. **Emerging Signals:** Ranked risk cards and score factor breakdowns.
3. **Temporal Intelligence:** Interactive Plotly time-series charts.
4. **Spatial Intelligence:** Geographic scatter map of GBIF animal occurrences in India.
5. **Knowledge Graph:** Subgraph visualizer and degree centrality ranking tables.
6. **Entity Intelligence:** Frequency breakdown across diseases, pathogens, animals, and locations.
7. **Methodology:** Plain-language One Health framework explanation and disclaimers.

### Q14: How does this satisfy both Text Analytics (TA) and Big Data Analytics (BDA)?
**Answer:**
- **Text Analytics (TA):** Web scraping unstructured text, regex sanitization, HTML entity decoding, tokenization, spaCy Named Entity Recognition (NER), domain lexicon keyword matching, semantic relationship extraction, and biomedical text categorization.
- **Big Data Analytics (BDA):** Multi-source heterogeneous data lake ingestion (clinical, literature, biodiversity), distributed text processing and deduplication using Apache Spark and Scala on the JVM, graph computing with NetworkX (1,620 nodes, 2,611 edges), spatio-temporal aggregation, and scalable dashboard deployment.

### Q15: What were the biggest technical challenges you faced and how did you resolve them?
**Answer:**
1. **Heterogeneous Schemas:** PubMed abstracts and WHO bulletins had completely different structures and dirty HTML/XML tags. We solved this by writing a custom sanitization pipeline that stripped markup and normalized texts into a common 4-column schema.
2. **Spark In-Memory Text Delimiters:** Standard CSV export from Spark can corrupt multiline biomedical abstracts containing commas and quotes. We resolved this by exporting the Spark corpus using tab-separated (`\t`) formatting.
3. **Graph Density & Visual Clutter:** A 1,620-node graph is too dense to render legibly on a single 2D screen. We resolved this by generating an optimized subgraph focused on high-degree One Health hub nodes and providing interactive tabular filters for entity exploration.

### Q16: Can this system be deployed to a production graph database like Neo4j?
**Answer:** Yes! We have written `knowledge_graph/load_neo4j.py` specifically for this purpose. It connects to a Neo4j instance via the official Python Neo4j driver (`neo4j>=5.20`), defines unique node constraints using Cypher queries, and executes batch edge insertions to support enterprise graph querying.

### Q17: What are the primary limitations of the current implementation?
**Answer:**
1. Our prototype uses 50 WHO reports, 1,000 PubMed articles, and 300 GBIF records as a representative proof-of-concept; a national production deployment would ingest hundreds of thousands of daily records.
2. The current NLP pipeline uses an English-language model (`en_core_web_sm`), meaning non-English veterinary bulletins are not yet ingested.
3. Relationship extraction combines rule-based matching with sentence co-occurrence; deep learning transformer models (like BioBERT) could further refine nuanced relation classification.

### Q18: What is your future scope?
**Answer:**
1. Implementing continuous streaming ingestion using **Apache Kafka** feeding directly into **Spark Structured Streaming**.
2. Upgrading NLP extraction to domain-adapted biomedical transformers such as **BioBERT** or **PubMedBERT**.
3. Integrating real-time weather and climate data (e.g., Copernicus ECMWF) to incorporate environmental vector variables (temperature, precipitation, deforestation).
4. Deploying the Neo4j backend on a cloud Kubernetes cluster with automated alert notifications sent to public health authorities.

### Q19: Which references did you cite in your project and presentation?
**Answer:**
1. **OHHLEP et al. (2023):** *"Developing One Health surveillance systems"* published in *One Health*.
2. **J. Wu (2021):** *"Construct a Knowledge Graph for China Coronavirus (COVID-19) Patient Information Tracking"* in *Risk Management and Healthcare Policy*.
3. **S. Consoli et al. (2025):** *"An epidemiological knowledge graph extracted from the World Health Organization’s Disease Outbreak News"* in *Nature Scientific Data*.
4. **W. J. Chen et al. (2020):** *"Development of a semi-structured, multifaceted, computer-aided questionnaire for outbreak investigation"* in *Biomedical Journal*.

### Q20: If you have to summarize this project in one single sentence, what would you say?
**Answer:** *"OneHealth Nexus is a large-scale Big Data and Text Analytics intelligence platform that processes multi-source medical, scientific, and biodiversity data using Apache Spark and spaCy to construct temporal knowledge graphs that surface emerging zoonotic disease signals before they turn into widespread human epidemics."*
