# OneHealth Nexus — Mid-Semester Progress & 10-Week Implementation Plan

**Project Title**: OneHealth Nexus: Large-Scale NLP and Temporal Knowledge Graphs for Emerging Disease Intelligence  
**Evaluation Milestone**: Mid-Semester Progress Review (Phase 1 & Phase 2 Gate)  
**Overall Completion Status**: **60% Completed** (On Schedule for 10-Week Timeline)  
**Repository**: [https://github.com/Abhiram-k1/OneHealth-Nexus](https://github.com/Abhiram-k1/OneHealth-Nexus)  

---

## 1. Executive Summary

The **OneHealth Nexus** project addresses the critical fragmentation between human clinical disease reporting, peer-reviewed biomedical literature, and wildlife vector biodiversity data. By combining **Apache Spark big data distributed processing**, **biomedical Named Entity Recognition (NER)**, and **heterogeneous knowledge graph modeling**, the platform surfaces early-warning signals for zoonotic transmission risks.

At the **Mid-Semester Review Gate (Week 6)**, the project has achieved **60% overall technical completion**, exceeding the minimum semester requirements by establishing a fully functional end-to-end prototype ingesting **5,550 verified data points** across three heterogeneous domains, modeling **4,796 knowledge nodes** and **12,471 transmission relationships**, and serving an **operational 7-screen decision support dashboard**.

---

## 2. Three-Phase Project Architecture

To transition from raw multi-source data ingestion to a fully operational, predictive artificial intelligence system, the project is structured into **three distinct phases**:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ONEHEALTH NEXUS — 3-PHASE ROADMAP                                │
├──────────────────────────────────┬─────────────────────────────────┬─────────────────────────────┤
│  PHASE 1: FOUNDATION & INGESTION │  PHASE 2: ANALYTICS & PROTOTYPE │ PHASE 3: PREDICTIVE AI      │
│  Weeks 1–4 (Status: 100% DONE)   │  Weeks 5–7 (Status: 85% DONE)   │ Weeks 8–10 (Status: PLANNED)│
├──────────────────────────────────┼─────────────────────────────────┼─────────────────────────────┤
│ • Tri-domain data harvesting     │ • Heterogeneous Knowledge Graph │ • Data scale expansion      │
│   (WHO, PubMed, GBIF: 5,550 pts) │   (4,796 nodes, 12,471 edges)   │   to 10,000+ points         │
│ • Apache Spark distributed ETL   │ • 53-year longitudinal trends   │ • BioLinkBERT transformer   │
│   (Scala 4.0.1 + PySpark)        │   (1965–2027 surveillance)      │   relation extraction       │
│ • Schema harmonization & null    │ • Spatial hotspot density map   │ • Graph Neural Network (GNN)│
│   reconciliation                 │   (3,000 GPS vector records)    │   spillover link prediction │
│ • Fast-path biomedical NER       │ • Composite 4-factor risk score │ • Neo4j persistent graph    │
│   (Disease, Host, Pathogen)      │ • 7-Screen Streamlit Dashboard  │ • Cloud cluster deployment  │
│                                  │   [★ CURRENT REVIEW GATEWAY ★]  │   & automated alerts        │
└──────────────────────────────────┴─────────────────────────────────┴─────────────────────────────┘
```

### Phase 1: Foundation, Ingestion & Batch Architecture (Weeks 1–4)
* **Status**: **100% Completed** (Weightage: 35% of total project)
* **Primary Goal**: Establish scalable multi-source data collection, distributed batch cleaning, and baseline entity extraction.
* **Key Deliverables Achieved**:
  1. **Multi-Source Data Lake**: Ingested 5,550 raw data points across 3 domains:
     - Human Clinical: 50 WHO Disease Outbreak News (DONs)
     - Biomedical Literature: 2,500 PubMed research articles
     - Animal Vectors: 3,000 georeferenced GBIF wildlife occurrences in India
  2. **Distributed Apache Spark Pipeline**: Configured Scala Spark 4.0.1 (via `sbt`) with PySpark fallback for text normalization, deduplication, and coordinate bounding ($6.94^\circ\text{–}33.82^\circ\text{ N}$, $68.97^\circ\text{–}95.95^\circ\text{ E}$).
  3. **Biomedical NLP Engine**: Implemented spaCy `en_core_web_sm` and compiled regular expression tokenization extracting 5 core entity classes (*Disease*, *Pathogen*, *Animal Host*, *Location*, *Date*).

### Phase 2: Knowledge Graph Engineering, Spatio-Temporal Analytics & Operational Dashboard (Weeks 5–7)
* **Status**: **85% Completed** (Weightage: 25% of total project; **Overall Project Progress: ~60%**)
* **Primary Goal**: Construct heterogeneous multi-relational network, quantify emerging zoonotic risk signals, and deliver an interactive operational command center for the mid-semester evaluation.
* **Key Deliverables Achieved**:
  1. **Heterogeneous Knowledge Graph**: Assembled NetworkX graph with **4,796 nodes and 12,471 directed edges** across 6 entity classes, identifying key transmission hub entities (Dengue, Monkeypox, Ebola, H5N1, bats, livestock).
  2. **Longitudinal Temporal Analysis**: Profiled surveillance volume over 53 calendar years (1965–2027), validating pandemic inflection points (2009 H1N1, 2014 Ebola, 2020 COVID-19, and 2024 post-pandemic acceleration).
  3. **Geospatial Intelligence**: Geocoded 3,000 vector occurrences across India, identifying high-risk wildlife-human contact zones in the Western Ghats, Indo-Gangetic Basin, and Himalayan corridor.
  4. **Quantitative Early Warning Indicator**: Implemented multi-factor composite risk scoring formula:
     $$\text{Risk Score} = 0.40 \cdot v_{\text{recent}} + 0.25 \cdot a_{\text{growth}} + 0.20 \cdot d_{\text{sources}} + 0.15 \cdot c_{\text{centrality}}$$
  5. **Operational 7-Page Surveillance UI**: Built production Streamlit command center (`dashboard/app.py`) with high-contrast institutional styling.

### Phase 3: Advanced Predictive Modeling (GNNs), Scale to 10k+, & Cloud Production Hardening (Weeks 8–10)
* **Status**: **Planned Scope** (Weightage: 40% of total project; End-Semester Focus)
* **Primary Goal**: Integrate deep learning link prediction, expand dataset past 10,000 points, deploy persistent graph database, and package for cloud execution.
* **Target Deliverables**:
  1. **Dataset Scaling to 10,000+ Records**: Harvest from ProMED-mail, FAO EMPRES-i animal disease tracking, and GISAID viral genomics.
  2. **BioLinkBERT Transformer NLP**: Replace regex rules with fine-tuned BioLinkBERT for nuanced relation extraction (`TRANSMITS_TO`, `RESERVOIR_OF`).
  3. **Graph Neural Network (GNN) Link Prediction**: Train Relational Graph Convolutional Networks (R-GCN) or Node2Vec to forecast unobserved host-pathogen spillovers.
  4. **Neo4j Graph Database**: Migrate from NetworkX memory graph to Neo4j with Cypher query endpoints.
  5. **Cloud Deployment & REST API**: Deploy on Google Cloud (Dataproc Serverless + Cloud Run) with automated email/webhook alert notifications.

---

## 3. Ten-Week Project Schedule & Gantt Timeline

```
Week  1   Week 2   Week 3   Week 4   Week 5   Week 6   Week 7   Week 8   Week 9   Week 10
[=========== PHASE 1: FOUNDATION ===========]
[==== Task 1: Multi-Source Data Harvesting (WHO, PubMed, GBIF: 5,550 pts) ====] (100% DONE)
         [==== Task 2: Apache Spark Ingestion & Deduplication (Scala/PySpark) ====] (100% DONE)
                  [==== Task 3: Biomedical NLP Entity Extraction (spaCy) ====] (100% DONE)
                                   [======= PHASE 2: ANALYTICS & PROTOTYPE ======]
                                   [==== Task 4: Knowledge Graph Construction (4,796 N / 12,471 E) ====] (100% DONE)
                                            [==== Task 5: 53-Yr Temporal & Spatial Hotspot Engine ====] (90% DONE)
                                            [==== Task 6: Mathematical Compound Risk Metric ====] (90% DONE)
                                                     [==== Task 7: 7-Screen Streamlit Dashboard ====] (95% DONE)
                                                     |
                                            ★ MID-SEM GATE (W6) ★
                                            CURRENT PROGRESS: 60%
                                                     |
                                                     [======== PHASE 3: ADVANCED PREDICTIVE AI =======]
                                                     [==== Task 8: Ingestion Scale to 10k+ (ProMED/FAO) ====]
                                                              [==== Task 9: BioLinkBERT Relation Mining ====]
                                                              [==== Task 10: GNN Spillover Link Prediction ==]
                                                                       [==== Task 11: Neo4j Cypher DB =======]
                                                                                [== Task 12: Cloud / Viva ==]
```

### Schedule Breakdown Table

| Week | Phase | Planned Objectives & Engineering Milestones | Primary Outputs | Status |
| :--- | :---: | :--- | :--- | :---: |
| **Week 1** | Phase 1 | Project scoping, API exploration (WHO DONs, PubMed E-Utilities, GBIF Occurrence API). | Raw ingestion scripts, schema definitions | **Completed** |
| **Week 2** | Phase 1 | Initial harvesting, text cleaning, character encoding, null-value reconciliation. | `data/raw/` initial multi-source corpus | **Completed** |
| **Week 3** | Phase 1 | Apache Spark pipeline development in Scala 4.0.1, distributed batch partitioning. | `src/main/scala/OneHealthPreprocessing.scala` | **Completed** |
| **Week 4** | Phase 1 | Biomedical NLP NER pipeline implementation, fast-path regex and spaCy model setup. | `nlp/entity_extraction.py`, entity annotations | **Completed** |
| **Week 5** | Phase 2 | NetworkX Knowledge Graph construction, typed relationships, degree calculations. | `knowledge_graph/build_graph.py`, 4,796 nodes | **Completed** |
| **Week 6** | Phase 2 | **Mid-Semester Review Gate**: Spatio-temporal analysis, risk formula, 7-page dashboard. | `dashboard/app.py`, 5,550 data points | **Active (60%)** |
| **Week 7** | Phase 2 | Post-review feedback integration, dataset validation audit, pipeline optimization. | `DATA_STUDY.md`, performance benchmarks | **In Progress** |
| **Week 8** | Phase 3 | Ingestion scaling to 10,000+ records (ProMED, FAO EMPRES-i), schema mapping. | 10k clean data lake records | **Planned** |
| **Week 9** | Phase 3 | BioLinkBERT relation extraction fine-tuning, Graph Neural Network (GNN) link prediction. | PyTorch Geometric GNN models, ROC-AUC metrics | **Planned** |
| **Week 10** | Phase 3 | Neo4j persistent database migration, cloud containerization, final documentation & viva. | Neo4j Cypher API, final technical report | **Planned** |

---

## 4. Current Status: Where Exactly We Are (60%) vs What Else Is Left (40%)

```
  ┌─────────────────────────────────────────────────────────────┐
  │              MID-SEMESTER STATUS BREAKDOWN                  │
  │   [██████████████████████████████░░░░░░░░░░░░░░░░░░░░] 60%  │
  │   • Completed & Operational: 60%                            │
  │   • Remaining End-Semester Scope: 40%                       │
  └─────────────────────────────────────────────────────────────┘
```

### Component-by-Component Progress Audit

| Architectural Layer | Mid-Semester Status (Delivered: 60%) | End-Semester Scope (Remaining: 40%) | Completion % |
| :--- | :--- | :--- | :---: |
| **Data Lake & Volume** | **5,550 records** harvested, cleaned, and geocoded (3,000 GBIF + 2,500 PubMed + 50 WHO). Validated across India bounding box. | Scale to **10,000+ records** by integrating ProMED-mail, FAO EMPRES-i, and GISAID. | **55.5%** |
| **Big Data Batch Engine** | Scala Apache Spark 4.0.1 (via `sbt run`) and PySpark fallback; batch deduplication and schema harmonization. | Cloud cluster deployment on GCP Dataproc Serverless for multi-node parallel execution. | **90.0%** |
| **NLP & Entity Extraction** | Hybrid biomedical NER using spaCy `en_core_web_sm` and compiled regex fast-path for 5 entity classes. | Fine-tune **BioLinkBERT** transformer model to classify complex multi-token relations and event semantics. | **75.0%** |
| **Knowledge Graph** | NetworkX multi-relational graph with **4,796 nodes and 12,471 relationships** across 6 entity classes; in-degree hub rankings. | Migrate to **Neo4j Enterprise Graph Database** with persistent storage, indexation, and Cypher query endpoints. | **70.0%** |
| **Spatio-Temporal Analytics** | 53-year longitudinal surveillance trajectory (1965–2027) + spatial density hotspot map of 3,000 vector coordinates. | Spatio-temporal cluster detection algorithms (Kulldorff spatial scan statistic / DBSCAN). | **85.0%** |
| **Risk Prioritization Engine** | Mathematical 4-factor compound risk formula combining velocity, growth rate, source diversity, and degree centrality. | **Graph Neural Network (GNN)** link prediction (R-GCN / Node2Vec) to forecast novel unobserved spillover links. | **40.0%** |
| **Interactive Dashboard** | 7-screen operational Streamlit surveillance center with institutional high-contrast styling and Plotly visuals. | Real-time automated alert dispatch (Email/Webhook/Telegram) and external REST API endpoint. | **90.0%** |
| **System Orchestration** | Fully automated local pipeline (`run_all.ps1`, `run_dashboard.ps1`) with environment self-healing. | Docker containerization, CI/CD pipeline, and Cloud Run production hosting. | **70.0%** |

---

## 5. Visual Artifacts for Mid-Semester Presentation

Two publication-grade (300 DPI) visualization diagrams have been generated and committed to the repository for inclusion in your presentation slides:

1. **Project Timeline & 3-Phase Roadmap**:
   - **Path**: [`analysis/midsem_timeline_roadmap.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/midsem_timeline_roadmap.png)
   - **Description**: Gantt chart illustrating all 12 tasks across Weeks 1 to 10, highlighting the current **Week 6 Mid-Semester Review Gateway** with progress color coding (Green: Done, Orange: Gateway, Blue: Planned).
2. **Subsystem Progress & Completion Matrix**:
   - **Path**: [`analysis/midsem_progress_breakdown.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/midsem_progress_breakdown.png)
   - **Description**: Dual-panel chart featuring an **Overall 60% Completion Donut** on the left and **8 subsystem completion progress bars** on the right.

---

## 6. Slide-by-Slide Mid-Semester Presentation Guide

Use this structured guide when presenting the project slides tomorrow:

### Slide 1: Title & Overview
* **Say**: *"Good morning respected evaluators. Today we present OneHealth Nexus, a Big Data and Text Analytics platform that breaks traditional epidemiological silos by unifying human clinical outbreaks, biomedical literature, and wildlife vector observations into an early-warning surveillance system."*
* **Highlight**: Phase 1 Prototype status, 60% overall completion.

### Slide 2: Problem Statement & Motivation
* **Say**: *"Traditional public health surveillance is reactive. Human outbreaks are tracked separately from veterinary disease records and academic publications. By the time human clinical cases appear, wildlife reservoir spillovers have already occurred. OneHealth Nexus bridges these three domains."*
* **Highlight**: Tri-domain integration (WHO + PubMed + GBIF).

### Slide 3: 3-Phase Architecture & 10-Week Roadmap
* **Say**: *"We have designed a structured 10-week implementation plan divided into three phases. Phase 1 established the foundation and data lake. Phase 2 delivered the knowledge graph and surveillance prototype, putting us at 60% completion today at Week 6. Phase 3 will introduce advanced predictive GNN modeling to achieve the fully developed platform by Week 10."*
* **Display Visual**: Show [`analysis/midsem_timeline_roadmap.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/midsem_timeline_roadmap.png).

### Slide 4: Data Lake & Big Data Scaling
* **Say**: *"For our mid-term milestone, we set a target to surpass 5,000 records. We have successfully ingested and validated 5,550 data points: 50 WHO outbreak reports, 2,500 PubMed research papers, and 3,000 animal occurrence coordinates across India, already reaching 55.5% of our 10,000 final project goal."*
* **Display Visual**: Show [`analysis/data_milestone_target.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/data_milestone_target.png).

### Slide 5: Apache Spark Distributed Preprocessing
* **Say**: *"Data cleaning is handled through an Apache Spark pipeline written in Scala 4.0.1 with automated fallbacks. Spark deduplicates text documents, enforces schema consistency, and filters geographic coordinates to ensure high data hygiene before knowledge modeling."*
* **Highlight**: Scalable batch execution, 2,550 clean text documents.

### Slide 6: Knowledge Graph Topology (4,796 Nodes, 12,471 Edges)
* **Say**: *"Our biomedical NLP pipeline extracts diseases, pathogens, host animals, locations, and timestamps, assembling them into a heterogeneous knowledge graph of 4,796 nodes and 12,471 relationships. This allows us to trace multi-hop transmission chains—for example, connecting fruit bats to Nipah virus outbreaks in Kerala."*
* **Display Visual**: Show [`knowledge_graph/entity_distribution.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/knowledge_graph/entity_distribution.png).

### Slide 7: Spatio-Temporal Intelligence & Early-Warning Scoring
* **Say**: *"We model disease reporting over a 53-year timeline (1965–2027) capturing historical pandemic surges such as H1N1, Ebola, and COVID-19. Furthermore, our 4-factor mathematical risk score ranks emerging threats. Currently, Dengue, Malaria, Mpox, and Avian Influenza rank highest based on velocity and transmission centrality."*
* **Display Visuals**: Show [`analysis/temporal_longitudinal_surge.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/temporal_longitudinal_surge.png) and [`analysis/emerging_signals_ranking.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/emerging_signals_ranking.png).

### Slide 8: Live Dashboard Demonstration
* **Action**: Switch to browser at `http://localhost:8501`.
* **Demonstrate**:
  1. **Executive Overview**: High-contrast KPI cards, milestone chart, entity donut.
  2. **Emerging Risk Signals**: Slide the threshold filter to show top pathogens.
  3. **Geospatial Intelligence**: Show 3,000 GPS points and spatial density heatmap.
  4. **Knowledge Graph Network**: Show extracted subgraph and node type distribution.

### Slide 9: Mid-Semester Deliverables vs. End-Semester Scope
* **Say**: *"To summarize our standing: our core data lake, Spark processing, knowledge graph, and dashboard are fully delivered and functional at 60%. In Phase 3, we will expand to 10,000+ points, fine-tune BioLinkBERT transformers, train Graph Neural Networks for spillover link prediction, and migrate to Neo4j."*
* **Display Visual**: Show [`analysis/midsem_progress_breakdown.png`](file:///c:/Users/abhi8/OneDrive/Desktop/ACADEMIC%20DOCS/SEM-5/TA&BDA/OneHealth-Nexus/analysis/midsem_progress_breakdown.png).

---

## 7. Anticipated Mid-Semester Viva Questions & Defense Answers

1. **Q: Why did you choose Apache Spark for preprocessing instead of simple Python scripts?**  
   * **A**: *"While Python handles prototyping well, biomedical literature and global biodiversity observations scale into millions of records. Apache Spark provides distributed in-memory fault tolerance, parallel partition processing, and schema enforcement that ensures the pipeline can scale seamlessly to our 10,000+ end-term milestone without architecture changes."*

2. **Q: How is your knowledge graph constructed, and what makes it heterogeneous?**  
   * **A**: *"It is heterogeneous because nodes belong to multiple semantic classes (*Document*, *Disease*, *Pathogen*, *Animal Host*, *Location*, *Date*) and edges represent distinct typed relationships (`DETECTED_IN`, `CARRIED_BY`, `CAUSED_BY`, `AFFECTS`, `OCCURRED_IN`). This multi-relational structure allows path traversals that uncover hidden zoonotic transmission links."*

3. **Q: How does your emerging signal score work? Is it an official prediction?**  
   * **A**: *"It is a quantitative surveillance indicator, not an official clinical diagnosis. It synthesizes four weighted dimensions: 40% recent mention velocity, 25% growth acceleration, 20% cross-source corroboration across multiple independent datasets, and 15% graph transmission centrality."*

4. **Q: What is left to complete for the final semester review?**  
   * **A**: *"The remaining 40% of our scope focuses on advanced predictive modeling: expanding data ingestion to 10,000+ points with ProMED and FAO data, fine-tuning BioLinkBERT for nuanced relation extraction, training Graph Neural Networks for link prediction on unobserved animal-pathogen interactions, and deploying to Neo4j."*
