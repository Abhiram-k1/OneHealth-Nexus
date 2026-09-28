# OneHealth Nexus — Academic Coursework Explanation
## Text Analytics (TA) & Big Data Analytics (BDA) Curriculum Alignment

**Course Context**: SEM-5 | Text Analytics (TA) & Big Data Analytics (BDA)  
**Project**: OneHealth Nexus: Large-Scale NLP and Temporal Knowledge Graphs for Emerging Disease Intelligence  
**Repository**: [https://github.com/Abhiram-k1/OneHealth-Nexus](https://github.com/Abhiram-k1/OneHealth-Nexus)  

---

## 1. Overview & Pedagogical Objective

The **OneHealth Nexus** project sits at the direct convergence of **Big Data Analytics (BDA)** and **Text Analytics (TA)**. In modern epidemiological surveillance, neither discipline alone is sufficient:
* **Text Analytics alone** can extract entities and sentiments from biomedical research or clinical bulletins, but struggles to process unstructured corpora across millions of documents without scalable distributed infrastructure.
* **Big Data Analytics alone** provides high-throughput distributed computation (e.g., Apache Spark), but lacks the semantic comprehension needed to disambiguate medical terminology, link zoonotic reservoirs, or extract typed biological relationships from natural language.

By unifying both paradigms, **OneHealth Nexus** ingests heterogeneous, high-volume, multi-source data, leverages **Apache Spark** for distributed data harmonization and cleaning, applies **Biomedical NLP (NER and Information Extraction)** to parse unstructured clinical and research texts, and constructs a **heterogeneous multi-relational Knowledge Graph** for predictive early warning signals.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     ONEHEALTH NEXUS — TA & BDA SYNERGY ARCHITECTURE                    │
├──────────────────────────────────────────┬─────────────────────────────────────────────┤
│      BIG DATA ANALYTICS (BDA) DOMAIN     │        TEXT ANALYTICS (TA) DOMAIN           │
├──────────────────────────────────────────┼─────────────────────────────────────────────┤
│ • 5 V's of Big Data Management           │ • Unstructured Biomedical Corpus Processing │
│ • Distributed Apache Spark (Scala 4.0.1) │ • Multi-stage Lexical Normalization         │
│ • Resilient Distributed Datasets (RDDs)  │ • Biomedical Named Entity Recognition (NER) │
│ • Catalyst Optimizer & DataFrame API     │ • Entity Disambiguation & Taxonomic Linking │
│ • In-Memory Shuffling & Partitioning     │ • Subject-Predicate-Object (SPO) Extraction │
│ • Fault-Tolerant Batch Preprocessing     │ • Semantic Knowledge Graph Construction     │
│ • Scalable Data Lake Architecture        │ • Longitudinal Trend & Frequency Mining     │
└──────────────────────────────────────────┴─────────────────────────────────────────────┘
```

---

## 2. Big Data Analytics (BDA) Curriculum Mapping

### 2.1 The 5 V's of Big Data in OneHealth Nexus

| Dimension | Textbook Concept | Concrete OneHealth Nexus Implementation |
| :--- | :--- | :--- |
| **Volume** | Ingestion and management of massive data scales beyond single-machine memory capacity. | Ingested **5,550 multi-source data points** in Phase 1 (3,000 GBIF vector records, 2,500 PubMed research articles, 50 WHO Outbreak Reports), engineered with an architecture designed to scale seamlessly past **10,000+ points** in Phase 3. |
| **Velocity** | Speed of data generation, streaming ingestion, and batch processing cycles. | Batch-processed 53 years of surveillance records (1965–2027) via Apache Spark in 60 seconds; structured for recurring automated pipeline triggers. |
| **Variety** | Heterogeneous data formats spanning unstructured text, semi-structured JSON, and structured tabular GIS coordinates. | Unifies unstructured biomedical abstracts (PubMed), semi-structured HTML/JSON outbreak reports (WHO DONs), and structured georeferenced spatial tuples (GBIF CSV). |
| **Veracity** | Data quality, completeness, noise filtering, and deduplication of noisy web-scraped data. | Automated Spark cleaning filters out null texts, enforces India bounding-box coordinates ($6.94^\circ\text{–}33.82^\circ\text{ N}$, $68.97^\circ\text{–}95.95^\circ\text{ E}$), reconciles partial date strings, and achieves a **99.7% data hygiene score**. |
| **Value** | Extracting actionable predictive intelligence and early-warning decision support from raw data. | Synthesizes 4-factor composite risk scores to surface high-priority zoonotic pathogen risks (Dengue: 57.83, Malaria: 56.08, Mpox: 53.79, Avian Flu: 53.16). |

---

### 2.2 Apache Spark Architecture & Internal Execution

The distributed computing backbone of OneHealth Nexus is built on **Apache Spark 4.0.1** using **Scala 2.13** (compiled via `sbt`) with a dual Python Spark fallback.

```
                      ┌─────────────────────────────────────────┐
                      │              Driver Program             │
                      │  • SparkSession ("OneHealth Nexus")     │
                      │  • DAGScheduler (Builds Task Stages)    │
                      │  • TaskScheduler (Dispatches Tasks)     │
                      └────────────────────┬────────────────────┘
                                           │
                    Cluster Manager / Local Master Mode (local[*])
                                           │
                 ┌─────────────────────────┴─────────────────────────┐
                 ▼                                                   ▼
     ┌───────────────────────┐                           ┌───────────────────────┐
     │    Executor Core 1    │                           │    Executor Core 2    │
     │ • BlockManager        │                           │ • BlockManager        │
     │ • In-Memory Cache     │                           │ • In-Memory Cache     │
     │ • Tasks: Filter/Clean │                           │ • Tasks: Deduplicate  │
     └───────────────────────┘                           └───────────────────────┘
```

#### Core Spark Concepts Implemented in Code:

1. **SparkSession Initialization**:
   Implemented in [`src/main/scala/OneHealthPreprocessing.scala`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/src/main/scala/OneHealthPreprocessing.scala):
   ```scala
   val spark = SparkSession.builder()
     .appName("OneHealth Nexus Preprocessing")
     .master("local[*]")
     .getOrCreate()
   spark.sparkContext.setLogLevel("ERROR")
   ```
   * *Curriculum Concept*: The `SparkSession` acts as the unified entry point for DataFrame operations. Setting `master("local[*]")` utilizes all available CPU cores on the host machine to achieve multi-threaded task parallelization.

2. **Lazy Evaluation & Directed Acyclic Graph (DAG)**:
   * *Curriculum Concept*: Spark does not execute transformations immediately upon declaration. Instead, it constructs a DAG of logical execution stages. Execution is triggered only when an **Action** (such as `.count()`, `.show()`, or `.collect()`) is called.
   * *In Our Code*: The `.filter()` and `.dropDuplicates()` transformations are compiled into an optimized physical plan by the **Catalyst Optimizer** before the terminal `.collect()` action executes.

3. **Narrow vs. Wide Transformations**:
   * **Narrow Transformation** (`filter`):
     ```scala
     val filteredDF = df.filter(col("clean_text").isNotNull && length(trim(col("clean_text"))) > 0)
     ```
     *Concept*: Operates on individual partitions in memory without network data movement (no shuffle). Each partition produces exactly one output partition.
   * **Wide Transformation** (`dropDuplicates`):
     ```scala
     val cleanedDF = filteredDF.dropDuplicates("clean_text")
     ```
     *Concept*: Requires a **Shuffle** operation across worker threads. Spark hashes the `clean_text` column and redistributes matching records to identical partitions across executor boundaries to identify duplicates.

4. **Schema Harmonization & Type Safety**:
   * In raw data, date fields contain heterogeneous strings (e.g., `"2024"`, `"2024-03"`, `"2024-03-15"`).
   * By setting `.option("inferSchema", "false")`, Spark treats all inputs as robust `StringType`, preventing JVM runtime casting exceptions (`EXPRESSION_DECODING_FAILED`) before downstream NLP ingestion.

---

## 3. Text Analytics (TA) Curriculum Mapping

Text Analytics transforms unstructured natural language from scientific papers and clinical bulletins into structured machine-readable knowledge.

### 3.1 Text Processing Pipeline Stages

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Raw Documents   │ ──> │ Lexical Cleaning │ ──> │ Tokenization &   │ ──> │ Named Entity     │
│ (PubMed / WHO)   │     │ & Normalization  │     │ Sentence Bounds  │     │ Recognition(NER) │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
                                                                                     │
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐               │
│ Knowledge Graph  │ <── │ Relation & Link  │ <── │ Entity Linking & │ <─────────────┘
│ (Nodes & Edges)  │     │ Extraction (SPO) │     │ Disambiguation   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

---

### 3.2 Lexical & Morphological Processing

1. **Noise Removal & Unicode Sanitization**:
   Implemented in [`nlp/entity_extraction.py`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/nlp/entity_extraction.py):
   * Stripping HTML tags (`<p>`, `<div>`, `<b>`), carriage returns (`\r\n` $\rightarrow$ space), and URLs.
   * Removing non-ASCII corruptions, trailing scientific journal citation artifacts, and publisher boilerplates (e.g., `UNLABELLED:`, `Copyright 2024 Elsevier`).
2. **Case Normalization & Whitespace Folding**:
   * Text is lowercased for token-level dictionary matching while preserving original sentence tokens for dependency parsing.
   * Multiple consecutive spaces and tabs are collapsed into single space delimiters.

---

### 3.3 Biomedical Named Entity Recognition (NER)

A central pillar of Text Analytics is **Named Entity Recognition (NER)**—identifying mentions of rigid designators in text and classifying them into predefined categories.

OneHealth Nexus employs a **Hybrid NER Architecture**:
1. **Statistical NER (spaCy `en_core_web_sm`)**:
   * Uses a transition-based neural network trained on OntoNotes 5 to recognize `GPE` / `LOC` (Geographic entities) and `DATE` (Temporal markers).
2. **Domain-Specific Biomedical Regex & Dictionary Matching**:
   * Standard pre-trained models frequently misclassify specialized biomedical terms (e.g., identifying *"Mpox"* or *"H5N1"* as miscellaneous nouns).
   * We designed high-performance compiled regular expression gazetteers mapped to standardized biomedical taxonomies:

```python
# Biomedical Entity Taxonomy Gazetteer Patterns
DISEASE_PATTERNS = [
    r"\b(dengue|malaria|mpox|monkeypox|avian influenza|influenza|ebola|nipah|covid(?:-19)?|cholera|rabies|tuberculosis|typhoid|zika|chikungunya|anthrax|kyasanur)\b"
]

PATHOGEN_PATTERNS = [
    r"\b(virus|bacteria|pathogen|h5n1|h1n1|sars-cov-2|plasmodium|flavivirus|filovirus|lyssavirus|henipavirus|bacillus anthracis)\b"
]

ANIMAL_PATTERNS = [
    r"\b(bat|bats|monkey|monkeys|primate|primates|poultry|bird|birds|chicken|duck|swine|pig|pigs|cattle|cow|livestock|wildlife|rodent|rodents|mosquito|mosquitoes|vector)\b"
]
```

#### Entity Classification Matrix:

| Entity Class | Semantic Definition | Examples in Corpus | Extraction Method |
| :--- | :--- | :--- | :--- |
| **Disease** | Clinical pathological condition diagnosed in hosts | *Dengue, Nipah virus infection, Mpox, Rabies* | Domain Regex Gazetteer |
| **Pathogen** | Biological agent causing the infection | *H5N1, SARS-CoV-2, Plasmodium falciparum, Lyssavirus* | Domain Regex Gazetteer |
| **Animal Host** | Wildlife reservoir or domestic transmission vector | *Fruit bats (Pteropus), Aedes aegypti, Poultry, Swine* | Taxonomic Gazetteer |
| **Location** | Geographic region of detection or outbreak | *Kerala, India, Wuhan, Guangdong, West Africa* | spaCy `GPE` / `LOC` NER |
| **Date** | Timestamp of epidemiological occurrence | *2024, 2020-03-11, 2009* | spaCy `DATE` + Regex Year |

---

### 3.4 Entity Linking & Disambiguation

* **Curriculum Concept**: Words in natural language exhibit synonymy (different terms for the same concept) and polysemy (one term with multiple meanings).
* **Implementation**:
  * Synonym reconciliation: Resolving `["monkeypox", "mpox"]` $\rightarrow$ canonical entity `Mpox`.
  * Normalizing `["covid", "covid-19", "sars-cov-2"]` $\rightarrow$ linking clinical disease concept to viral pathogen.
  * Resolving generic avian terms: `["bird flu", "avian influenza"]` $\rightarrow$ `Avian Influenza (H5N1)`.

---

### 3.5 Information Extraction (IE) & Semantic Triples

* **Curriculum Concept**: Information Extraction goes beyond finding words to discover the semantic *relationships* connecting entities.
* In OneHealth Nexus, extracted entities are mapped into **Subject-Predicate-Object (SPO) Triples**:

$$\langle \text{Subject} \rangle \xrightarrow{\quad \text{Predicate (Relationship)} \quad} \langle \text{Object} \rangle$$

Examples extracted from the corpus:
* $\langle \text{Document: PUBMED\_38910} \rangle \xrightarrow{\text{DETECTED\_IN}} \langle \text{Location: India} \rangle$
* $\langle \text{Pathogen: Nipah Virus} \rangle \xrightarrow{\text{CARRIED\_BY}} \langle \text{Animal: Fruit Bat} \rangle$
* $\langle \text{Disease: Dengue} \rangle \xrightarrow{\text{CAUSED\_BY}} \langle \text{Pathogen: Flavivirus} \rangle$
* $\langle \text{Disease: Avian Influenza} \rangle \xrightarrow{\text{AFFECTS}} \langle \text{Animal: Poultry} \rangle$
* $\langle \text{Document: WHO\_DON\_2024} \rangle \xrightarrow{\text{OCCURRED\_IN}} \langle \text{Date: 2024} \rangle$

---

## 4. Graph Analytics & Network Science (Intersection of TA & BDA)

The extracted triples are loaded into a **Heterogeneous Multi-Relational Knowledge Graph** constructed via NetworkX (and designed for Neo4j in Phase 3).

```
          ┌────────────────┐
          │  Date: 2024    │
          └───────▲────────┘
                  │ OCCURRED_IN
                  │
┌─────────────────┴─────────────────┐
│     Document: PUBMED_38910        │
└────────┬──────────────┬───────────┘
         │              │
         │ DETECTED_IN  │ MENTIONS
         ▼              ▼
┌─────────────────┐   ┌─────────────────┐
│ Location: Kerala│   │ Disease: Nipah  │
└─────────────────┘   └────────┬────────┘
                               │ CAUSED_BY
                               ▼
                      ┌─────────────────┐
                      │ Pathogen: Henipa│
                      └────────┬────────┘
                               │ CARRIED_BY
                               ▼
                      ┌─────────────────┐
                      │  Animal: Bat    │
                      └─────────────────┘
```

### 4.1 Formal Mathematical Graph Metrics

1. **Graph Density ($D$)**:
   Measures the proportion of potential edges that actually exist in the network:
   $$D = \frac{|E|}{|V|(|V| - 1)}$$
   *For OneHealth Nexus*:
   * $|V| = 4,796$ nodes
   * $|E| = 12,471$ relationships
   * Density: $D = 0.000542$ (characteristic of sparse, highly modular real-world biomedical knowledge networks).

2. **Degree Centrality ($C_D$)**:
   Quantifies the biological transmission importance of an entity based on the number of incident edges:
   $$C_D(v) = \frac{\text{deg}(v)}{|V| - 1}$$
   * **In-Degree Centrality**: Measures how many independent documents and outbreaks reference a specific disease or host (e.g., `virus`: 1,488 connections; `cat`/`livestock`/`wildlife`: 350+ connections; `dengue`/`mpox`/`ebola`: 310+ connections).
   * **Transmission Hubs**: Entities with high in-degree centrality represent **super-spreader transmission hubs** connecting disparate host species to human outbreaks.

3. **Multi-Hop Path Traversal**:
   Enables discovery of indirect transmission routes:
   $$\text{Path} = (v_{\text{animal}}, e_{\text{carried\_by}}, v_{\text{pathogen}}, e_{\text{causes}}, v_{\text{disease}}, e_{\text{detected\_in}}, v_{\text{location}})$$
   Allows public health officials to answer: *"Which wildlife species observed in the Western Ghats carry pathogens linked to acute respiratory syndromes in human literature?"*

---

## 5. Quantitative Analytics & Modeling Formulations

### 5.1 Multi-Factor Early-Warning Compound Risk Score

Rather than relying purely on keyword counts, OneHealth Nexus designs a balanced mathematical indicator:

$$S(d) = w_1 \cdot v_{\text{recent}}(d) + w_2 \cdot a_{\text{growth}}(d) + w_3 \cdot d_{\text{sources}}(d) + w_4 \cdot c_{\text{centrality}}(d)$$

Where:
* $v_{\text{recent}}(d)$: Normalized mention velocity over the last 3 calendar years (2024–2026). Weight $w_1 = 0.40$.
* $a_{\text{growth}}(d)$: Acceleration ratio ($\frac{\text{Recent Mentions}}{\text{Historical Mentions}}$). Weight $w_2 = 0.25$.
* $d_{\text{sources}}(d)$: Cross-source corroboration score (WHO + PubMed + GBIF multi-domain confirmation). Weight $w_3 = 0.20$.
* $c_{\text{centrality}}(d)$: Normalized graph degree centrality in the knowledge network. Weight $w_4 = 0.15$.

#### Current Mid-Semester Prioritization Leaderboard:
1. **Dengue Virus**: **57.83** (High velocity in recent literature + vector presence in South Asia)
2. **Malaria (*Plasmodium*)**: **56.08** (Sustained cross-source documentation)
3. **Mpox**: **53.79** (Rapid acceleration following global re-emergence)
4. **Monkeypox**: **53.40** (Corroborated historical surveillance)
5. **Avian Influenza (H5N1)**: **53.16** (Wildlife-to-domestic poultry cross-transmission risk)
6. **Ebola**: **50.10** (High clinical fatality with localized African reservoirs)
7. **Nipah**: **45.38** (Bat-borne zoonotic spillover risk in Southern India)

---

### 5.2 53-Year Longitudinal Trend Surveillance

* Time series aggregation:
  $$N(t) = \sum_{i=1}^{M} \mathbb{I}(\text{year}(\text{doc}_i) = t), \quad t \in [1965, 2027]$$
* Captures historical pandemic inflection peaks:
  * **2009**: H1N1 Pandemic influenza surge ($N = 10$)
  * **2014**: West Africa Ebola outbreak ($N = 25$)
  * **2020**: COVID-19 pandemic inflection ($N = 49 \rightarrow 100$)
  * **2024–2026**: Post-pandemic surveillance acceleration ($N = 641 \rightarrow 744$)

---

### 5.3 Spatial Density & Coordinate Validation

* Bounding Box Constraint:
  $$\text{Valid}(\text{point}_i) \iff (6.94^\circ \le \text{lat}_i \le 33.82^\circ) \land (68.97^\circ \le \text{lon}_i \le 95.95^\circ)$$
* Filters out corrupted GPS entries (e.g., $(0.0, 0.0)$ null island or inverted latitudes) to guarantee authentic geospatial distribution across the Indian subcontinent.

---

## 6. Academic Viva Cheatsheet (15 High-Yield Questions)

### Q1: What makes OneHealth Nexus a "Big Data" project and not just a standard web application?
> **Answer**: OneHealth Nexus unifies multi-source data across the 5 V's of Big Data. It ingests 5,550 data points spanning unstructured biomedical text (PubMed), semi-structured clinical outbreak news (WHO), and geospatial wildlife occurrences (GBIF). It uses Apache Spark for distributed memory-partitioned data cleaning, deduplication, and schema reconciliation, building a data lake designed to scale past 10,000+ points and millions of records in cloud deployment.

### Q2: Explain the internal architecture of Apache Spark and how it is used in your project.
> **Answer**: Apache Spark uses a master-slave architecture where the Driver program runs the `SparkSession`, creates a Directed Acyclic Graph (DAG) of execution, and coordinates executor worker threads. In our file `OneHealthPreprocessing.scala`, Spark runs in `local[*]` mode. It applies narrow transformations (`filter` on non-null text) and wide transformations (`dropDuplicates` requiring cross-partition shuffling) before executing the action `.collect()` to write out standardized tab-delimited partitions.

### Q3: What is the difference between an RDD and a DataFrame in Spark, and why did you use DataFrames?
> **Answer**: An RDD (Resilient Distributed Dataset) is a low-level, type-safe collection of JVM objects partitioned across nodes. A DataFrame is an RDD organized into named columns, conceptually equivalent to a relational table. We chose DataFrames because they leverage the **Catalyst Optimizer** and the **Tungsten execution engine**, which optimize query plans, generate efficient bytecode, and avoid JVM object serialization overhead.

### Q4: What is Lazy Evaluation, and why is it beneficial in Spark?
> **Answer**: Lazy evaluation means Spark records transformations (like `.filter()` and `.select()`) into a logical execution plan rather than executing them immediately. Execution occurs only when an action (like `.count()` or `.collect()`) is called. This allows the Catalyst Optimizer to optimize the entire processing chain—for example, by pushing down filter predicates to read only relevant data and minimizing expensive data shuffles.

### Q5: How do you handle schema heterogeneity when ingesting multi-source datasets?
> **Answer**: In our Scala Spark script, we disabled `inferSchema` (`option("inferSchema", "false")`). This prevents Spark from misinterpreting partial or heterogeneous date strings (e.g., `"2024"` vs `"2024-03-15"`) as strict SQL Date types, which would throw runtime decoding exceptions. We enforce a harmonized schema (`document_id: String`, `source: String`, `date: String`, `clean_text: String`) across all text sources.

### Q6: What text pre-processing steps are applied before entity extraction?
> **Answer**: We perform Unicode sanitization, URL and HTML tag stripping via compiled regular expressions, whitespace folding, carriage return neutralization, and stop-phrase removal (such as publisher boilerplates like `UNLABELLED:` and copyright lines). We preserve sentence capitalization for spaCy's dependency parser while utilizing lowercased normalization for dictionary matching.

### Q7: Why did you use a Hybrid NER approach instead of relying purely on spaCy's pre-trained model?
> **Answer**: Pre-trained statistical models like spaCy's `en_core_web_sm` are trained on general news corpora (OntoNotes 5). While they excel at detecting `GPE`/`LOC` (Locations) and `DATE` (Timestamps), they frequently miss specialized biomedical terms like *"Mpox"*, *"H5N1"*, or *"Kyasanur Forest Disease"*. Our hybrid approach pairs spaCy for spatial/temporal extraction with compiled biomedical regex gazetteers that capture domain-specific disease, pathogen, and vector entities with 100% precision.

### Q8: What is the difference between Rule-Based NER and Statistical NER?
> **Answer**: Rule-based NER uses deterministic pattern matching, regular expressions, and gazetteers. It offers 100% precision on known vocabularies and requires zero training data, but cannot generalize to unseen terms. Statistical NER uses probabilistic sequential models (e.g., Conditional Random Fields, BiLSTM-CRF, or Transformers) that predict entity boundaries based on contextual word embeddings, allowing them to detect novel entities at the cost of requiring annotated training data.

### Q9: What is Entity Disambiguation and how is it implemented?
> **Answer**: Entity disambiguation resolves different textual surface forms that refer to the same real-world entity. In our pipeline, mentions such as `"monkeypox"` and `"mpox"` are mapped to the canonical concept `Mpox`, while `"bird flu"` and `"avian influenza"` are unified into `Avian Influenza (H5N1)` to prevent duplicate or fragmented nodes in our knowledge graph.

### Q10: How are relationships extracted to form the Knowledge Graph?
> **Answer**: We use sentence-level co-occurrence and grammatical dependency patterns to extract Subject-Predicate-Object (SPO) triples. When a disease entity and a location entity co-occur within the same validated document context, a `DETECTED_IN` directed edge is established. Similarly, associations between pathogens and animal vectors create `CARRIED_BY` relationships, and pathogen-disease links create `CAUSED_BY` edges.

### Q11: What graph metrics do you calculate, and what do they signify biologically?
> **Answer**: We calculate Graph Density ($D = 0.000542$, indicating a sparse, highly specific biological network) and In-Degree Centrality. In our knowledge graph, nodes with exceptionally high in-degree centrality (such as the pathogen `virus`, animal hosts like `bats` and `livestock`, and diseases like `Dengue` and `Mpox`) act as transmission hubs that bridge multiple independent host reservoirs with human clinical infection events.

### Q12: How does your Emerging Signal Score work mathematically?
> **Answer**: It is a 4-factor composite weighted index:
> $$S(d) = 0.40 \cdot v_{\text{recent}} + 0.25 \cdot a_{\text{growth}} + 0.20 \cdot d_{\text{sources}} + 0.15 \cdot c_{\text{centrality}}$$
> It balances recent 3-year mention velocity (40%), growth rate acceleration over historical baselines (25%), cross-source corroboration across multiple independent datasets (20%), and network degree centrality (15%). This prevents a disease with high historical mentions but zero recent cases from overshadowing an accelerating emerging threat.

### Q13: Why did you restrict GBIF animal occurrences to the India geographic bounding box?
> **Answer**: Public health interventions are geographically specific. To model realistic zoonotic spillovers for regional surveillance, we bounded GBIF coordinates to $6.94^\circ\text{–}33.82^\circ\text{ N}$ and $68.97^\circ\text{–}95.95^\circ\text{ E}$. This filters out corrupted entries (such as $(0,0)$ null coordinates) and highlights critical ecological corridors like the Western Ghats (a known hotspot for Kyasanur Forest Disease and bat-borne Nipah virus).

### Q14: What is the current project progress at the Mid-Semester review?
> **Answer**: We stand at **60% technical completion**. Phase 1 (Data Lake Ingestion, Spark Batch Cleaning, Baseline NER) is 100% completed. Phase 2 (Knowledge Graph Construction, 53-Year Temporal Modeling, Spatial Density Heatmaps, and the 7-Screen Streamlit Dashboard) is 85% completed. The remaining 40% represents Phase 3, which focuses on advanced predictive modeling (GNN link prediction), scaling past 10,000 points, fine-tuning BioLinkBERT, and cloud containerization.

### Q15: How will Phase 3 improve upon your current rule-based extraction and scoring?
> **Answer**: In Phase 3, we will replace regex relation extraction with a fine-tuned **BioLinkBERT** transformer to classify nuanced grammatical relations (`TRANSMITS_TO`, `ASYMPTOMATIC_RESERVOIR`). Furthermore, we will train a **Graph Neural Network (R-GCN / Node2Vec)** on the knowledge graph to perform link prediction, forecasting previously unobserved animal-pathogen interactions before clinical outbreaks occur in the human population.
