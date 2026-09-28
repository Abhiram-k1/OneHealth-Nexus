"""
OneHealth Nexus — Epidemiological Intelligence & Zoonotic Surveillance Center
Mid-Semester Evaluation Release (Phase 1 Prototype)
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OneHealth Nexus | Surveillance Dashboard",
    page_icon="none",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# INSTITUTIONAL STYLING & CSS
# ============================================================

st.markdown("""
<style>
    /* Base typography */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #cbd5e1 !important;
        font-size: 14px;
        padding: 4px 0;
    }

    /* Top banner */
    .status-banner {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .badge-midterm {
        background: #dbeafe;
        color: #1e40af;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .banner-text {
        font-size: 13px;
        color: #475569;
        font-weight: 500;
    }

    /* Header component */
    .header-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .header-title {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }

    .header-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* Section titles */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 6px;
        letter-spacing: -0.2px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 16px;
    }

    /* KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        height: 100%;
    }

    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 6px;
        margin-bottom: 4px;
    }

    .kpi-sub {
        font-size: 12px;
        color: #94a3b8;
    }

    /* Signal Card */
    .signal-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #ef4444;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    .signal-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
    }

    .signal-meta {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    .signal-score-badge {
        font-size: 22px;
        font-weight: 700;
        color: #dc2626;
    }

    /* Pipeline stage box */
    .stage-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }

    .stage-num {
        font-size: 11px;
        font-weight: 700;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stage-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 2px;
    }

    .stage-desc {
        font-size: 13px;
        color: #64748b;
        margin-top: 4px;
    }

    /* Footer */
    .dash-footer {
        border-top: 1px solid #e2e8f0;
        padding: 24px 0 12px 0;
        margin-top: 40px;
        color: #94a3b8;
        font-size: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA INGESTION
# ============================================================

summary_file = "knowledge_graph/graph_summary.csv"
entities_file = "knowledge_graph/important_entities.csv"
temporal_file = "analysis/temporal_summary.csv"
signal_file = "analysis/emerging_signals.csv"
nodes_file = "knowledge_graph/nodes.csv"
relationships_file = "knowledge_graph/relationships.csv"
gbif_file = "data/processed/cleaned_gbif.csv"
docs_file = "data/processed/cleaned_documents.csv"

summary = pd.read_csv(summary_file) if os.path.exists(summary_file) else pd.DataFrame(columns=["metric", "value"])
entities = pd.read_csv(entities_file) if os.path.exists(entities_file) else pd.DataFrame()
temporal = pd.read_csv(temporal_file) if os.path.exists(temporal_file) else pd.DataFrame()
signals = pd.read_csv(signal_file) if os.path.exists(signal_file) else pd.DataFrame()
nodes = pd.read_csv(nodes_file) if os.path.exists(nodes_file) else pd.DataFrame()
relationships = pd.read_csv(relationships_file) if os.path.exists(relationships_file) else pd.DataFrame()
gbif = pd.read_csv(gbif_file) if os.path.exists(gbif_file) else pd.DataFrame()
docs = pd.read_csv(docs_file) if os.path.exists(docs_file) else pd.DataFrame()

def get_metric(name):
    if len(summary) > 0 and "metric" in summary.columns:
        row = summary[summary["metric"] == name]
        if len(row) > 0:
            return row.iloc[0]["value"]
    return 0

def fmt_num(val):
    try:
        return f"{int(float(val)):,}"
    except (ValueError, TypeError):
        return str(val)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 16px 0;">
        <div style="font-size: 19px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px;">ONEHEALTH NEXUS</div>
        <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; margin-top: 3px;">Surveillance Platform</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Emerging Risk Signals",
            "Temporal Surveillance",
            "Geospatial Intelligence",
            "Knowledge Graph Network",
            "Biomedical Entity Profiler",
            "Methodology & Evaluation"
        ]
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #334155; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
        Data Ingestion Status
    </div>
    """, unsafe_allow_html=True)

    total_points = len(docs) + len(gbif)
    progress_pct = min(1.0, total_points / 10000.0)
    st.progress(progress_pct)

    st.markdown(f"""
    <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 14px;">
        <b>{total_points:,}</b> / 10,000 Records ({progress_pct*100:.1f}%)
    </div>
    <div style="font-size: 12px; color: #94a3b8; line-height: 1.8;">
        • WHO Clinical Outbreaks: <b>50</b><br>
        • PubMed Research Corpus: <b>2,500</b><br>
        • GBIF Wildlife Vectors: <b>3,000</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #334155; margin: 20px 0;'>", unsafe_allow_html=True)
    st.caption("Phase 1 — Mid-Semester Release")
    st.caption("Big Data & Text Analytics Lab")

# ============================================================
# TOP STATUS BANNER
# ============================================================

st.markdown("""
<div class="status-banner">
    <div>
        <span class="badge-midterm">Phase 1 Prototype</span>
        <span class="banner-text" style="margin-left: 12px;">Mid-Semester Review — Ingestion, Apache Spark Preprocessing & Knowledge Graph Construction</span>
    </div>
    <div style="font-size: 12px; color: #64748b; font-weight: 500;">
        Status: Validated Pipeline (5,550 Data Points)
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">Executive Surveillance Overview</h1>
        <div class="header-subtitle">
            Cross-domain early warning surveillance platform integrating clinical human disease alerts, 
            biomedical peer-reviewed literature, and animal vector reservoir occurrences.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Ingested Records</div>
            <div class="kpi-value">{total_points:,}</div>
            <div class="kpi-sub">55.5% of 10,000 Milestone</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Cleaned Documents</div>
            <div class="kpi-value">{fmt_num(len(docs))}</div>
            <div class="kpi-sub">Spark deduplicated texts</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Vector GPS Points</div>
            <div class="kpi-value">{fmt_num(len(gbif))}</div>
            <div class="kpi-sub">Bounded to India region</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Knowledge Nodes</div>
            <div class="kpi-value">{fmt_num(get_metric("Total Nodes"))}</div>
            <div class="kpi-sub">6 entity classifications</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Relationships</div>
            <div class="kpi-value">{fmt_num(get_metric("Total Relationships"))}</div>
            <div class="kpi-sub">Biological & spatial edges</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Mid-Semester Milestone Progression Chart
    milestone_img = "analysis/data_milestone_target.png"
    if os.path.exists(milestone_img):
        st.markdown('<div class="section-title">Data Ingestion Scaling Milestone</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Mid-semester baseline achieved vs. final submission target across three core data layers.</div>', unsafe_allow_html=True)
        st.image(milestone_img, caption="Figure 1: Current Ingested Points (5,550) vs Project Target (10,000)", use_container_width=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Two-Column Longitudinal & Entity Views
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-title">Longitudinal Surveillance Trajectory</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Temporal distribution of research documents and outbreak reports (1965–2027).</div>', unsafe_allow_html=True)

        if len(temporal) > 0 and "year" in temporal.columns:
            temp_df = temporal.copy()
            temp_df["year"] = pd.to_numeric(temp_df["year"], errors="coerce")
            temp_df["document_count"] = pd.to_numeric(temp_df["document_count"], errors="coerce")
            temp_df = temp_df.dropna().sort_values("year")
            temp_df["year"] = temp_df["year"].astype(int)

            fig_t = px.area(
                temp_df,
                x="year",
                y="document_count",
                color_discrete_sequence=["#2563eb"],
                labels={"year": "Calendar Year", "document_count": "Document Count"}
            )
            fig_t.update_layout(
                height=340,
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
            )
            st.plotly_chart(fig_t, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">Knowledge Graph Entity Composition</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Breakdown of extracted biomedical, temporal, and spatial node types.</div>', unsafe_allow_html=True)

        if len(nodes) > 0 and "type" in nodes.columns:
            counts = nodes["type"].value_counts().reset_index()
            counts.columns = ["Type", "Count"]

            fig_p = px.pie(
                counts,
                names="Type",
                values="Count",
                hole=0.55,
                color_discrete_sequence=["#1e3a8a", "#0284c7", "#0d9488", "#d97706", "#dc2626", "#7c3aed"]
            )
            fig_p.update_layout(
                height=340,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#ffffff"
            )
            st.plotly_chart(fig_p, use_container_width=True)

    # Top Signals Preview
    st.markdown('<div class="section-title">Priority Early-Warning Signals</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Top prioritized pathogen threats ranked by compound velocity, acceleration, and cross-source corroboration.</div>', unsafe_allow_html=True)

    if len(signals) > 0:
        top_sig = signals.head(4)
        s_cols = st.columns(4)
        for idx, (_, row) in enumerate(top_sig.iterrows()):
            with s_cols[idx]:
                st.markdown(f"""
                <div class="signal-item">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <span class="signal-title">{str(row['disease']).title()}</span>
                        <span class="signal-score-badge">{float(row['signal_score']):.1f}</span>
                    </div>
                    <div class="signal-meta">
                        Recent Activity: <b>{row['recent_mentions']}</b><br>
                        Source Breadth: <b>{row['source_count']}</b> source(s)<br>
                        Surveillance Span: <b>{row['year_count']}</b> yr(s)
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# PAGE 2 — EMERGING RISK SIGNALS
# ============================================================

elif page == "Emerging Risk Signals":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">Emerging Pathogen Risk Scoring & Signal Detection</h1>
        <div class="header-subtitle">
            Multi-factor quantitative prioritization evaluating velocity, recent acceleration, cross-source breadth, 
            and graph transmission centrality.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formula Box
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px 20px; margin-bottom:20px;">
        <div style="font-size:12px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px;">Compound Risk Metric Formulation</div>
        <div style="font-size:14px; color:#1e293b; margin-top:6px;">
            <code>Score = 0.40 · Velocity (Recent Mentions) + 0.25 · Acceleration (Growth Rate) + 0.20 · Source Diversity + 0.15 · Centrality (In-Degree)</code>
        </div>
        <div style="font-size:12px; color:#64748b; margin-top:6px;">
            The indicator standardizes publication surge rates against historical baselines to surface emerging zoonotic spillovers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # High-Resolution Ranking Chart
    ranking_img = "analysis/emerging_signals_ranking.png"
    if os.path.exists(ranking_img):
        st.image(ranking_img, caption="Figure 2: Emerging Pathogen Risk Prioritization Ranking (Normalized Compound Score)", use_container_width=True)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if len(signals) > 0 and "signal_score" in signals.columns:
        sig_df = signals.copy()
        sig_df["signal_score"] = pd.to_numeric(sig_df["signal_score"], errors="coerce")
        sig_df = sig_df.dropna(subset=["signal_score"]).sort_values("signal_score", ascending=False)

        min_threshold = st.slider("Filter by Minimum Signal Score", min_value=0.0, max_value=100.0, value=25.0, step=1.0)
        filtered_sig = sig_df[sig_df["signal_score"] >= min_threshold]

        fig_bar = px.bar(
            filtered_sig,
            x="signal_score",
            y="disease",
            orientation="h",
            color="signal_score",
            color_continuous_scale="Blues",
            labels={"signal_score": "Composite Signal Score", "disease": "Pathogen / Condition"},
            text="signal_score"
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_bar.update_layout(
            height=500,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            yaxis=dict(autorange="reversed"),
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown('<div class="section-title">Signal Metric Audit Table</div>', unsafe_allow_html=True)
        st.dataframe(filtered_sig, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 3 — TEMPORAL SURVEILLANCE
# ============================================================

elif page == "Temporal Surveillance":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">Longitudinal Temporal Surveillance (1965–2027)</h1>
        <div class="header-subtitle">
            Historical analysis of epidemic reporting, publication volumes, and inflection peaks across five decades of surveillance records.
        </div>
    </div>
    """, unsafe_allow_html=True)

    surge_img = "analysis/temporal_longitudinal_surge.png"
    if os.path.exists(surge_img):
        st.image(surge_img, caption="Figure 3: 53-Year Longitudinal Outbreak Surveillance Timeline (H1N1, Ebola, COVID-19)", use_container_width=True)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if len(temporal) > 0 and "year" in temporal.columns:
        temp_df = temporal.copy()
        temp_df["year"] = pd.to_numeric(temp_df["year"], errors="coerce")
        temp_df["document_count"] = pd.to_numeric(temp_df["document_count"], errors="coerce")
        temp_df = temp_df.dropna().sort_values("year")
        temp_df["year"] = temp_df["year"].astype(int)

        fig_line = px.line(
            temp_df,
            x="year",
            y="document_count",
            markers=True,
            color_discrete_sequence=["#1e3a8a"],
            labels={"year": "Calendar Year", "document_count": "Processed Documents"}
        )
        fig_line.update_layout(
            height=450,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9", dtick=2),
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown('<div class="section-title">Annual Record Ingestion Counts</div>', unsafe_allow_html=True)
        st.dataframe(temp_df, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 4 — GEOSPATIAL INTELLIGENCE
# ============================================================

elif page == "Geospatial Intelligence":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">Geospatial Wildlife & Vector Intelligence</h1>
        <div class="header-subtitle">
            Georeferenced occurrence observations from the Global Biodiversity Information Facility (GBIF) 
            mapping reservoir vectors across India.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Heatmap visual
    heatmap_img = "analysis/spatial_biodiversity_heatmap.png"
    if os.path.exists(heatmap_img):
        st.image(heatmap_img, caption="Figure 4: Spatial Density & Biodiversity Hotspot Map of 3,000 Animal Records Across India", use_container_width=True)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if len(gbif) > 0:
        lat_col = next((c for c in gbif.columns if "lat" in c.lower()), None)
        lon_col = next((c for c in gbif.columns if "lon" in c.lower() or "lng" in c.lower()), None)

        if lat_col and lon_col:
            map_data = gbif.copy()
            map_data[lat_col] = pd.to_numeric(map_data[lat_col], errors="coerce")
            map_data[lon_col] = pd.to_numeric(map_data[lon_col], errors="coerce")
            map_data = map_data.dropna(subset=[lat_col, lon_col])

            c_map1, c_map2 = st.columns([3, 1])

            with c_map1:
                fig_geo = px.scatter_geo(
                    map_data,
                    lat=lat_col,
                    lon=lon_col,
                    scope="asia",
                    projection="natural earth",
                    color_discrete_sequence=["#0d9488"],
                    title="Interactive Occurrence Coordinates"
                )
                fig_geo.update_traces(marker=dict(size=5, opacity=0.7))
                fig_geo.update_layout(
                    height=500,
                    margin=dict(l=0, r=0, t=30, b=0),
                    paper_bgcolor="#ffffff"
                )
                st.plotly_chart(fig_geo, use_container_width=True)

            with c_map2:
                st.markdown("""
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:18px; height:100%;">
                    <div style="font-size:12px; font-weight:700; color:#64748b; text-transform:uppercase;">Spatial Coverage Specs</div>
                    <div style="font-size:13px; color:#1e293b; margin-top:10px; line-height:1.7;">
                        • <b>Total Coordinates</b>: 3,000 points<br>
                        • <b>Bounding Lat</b>: 6.94° N – 33.82° N<br>
                        • <b>Bounding Lon</b>: 68.97° E – 95.95° E<br>
                        • <b>Hotspot Zones</b>: Western Ghats, Indo-Gangetic Basin, Himalayan Corridor<br>
                        • <b>Target Reservoirs</b>: Chiroptera (bats), Primates, Culicidae (mosquitoes)
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# PAGE 5 — KNOWLEDGE GRAPH NETWORK
# ============================================================

elif page == "Knowledge Graph Network":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">Knowledge Graph Network Topology</h1>
        <div class="header-subtitle">
            Heterogeneous multi-relational network linking documents, diseases, pathogens, reservoir animals, 
            geographic regions, and event timestamps.
        </div>
    </div>
    """, unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Graph Nodes", fmt_num(len(nodes)))
    g2.metric("Relationships", fmt_num(len(relationships)))
    g3.metric("Entity Classes", fmt_num(nodes["type"].nunique()) if len(nodes) > 0 and "type" in nodes.columns else "6")
    g4.metric("Graph Density", f"{float(get_metric('Graph Density')):.6f}")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Subgraph Visual
    subgraph_img = "knowledge_graph/onehealth_subgraph.png"
    if os.path.exists(subgraph_img):
        st.image(subgraph_img, caption="Figure 5: OneHealth Nexus Subgraph — Extracted Transmission Pathways & Cross-Domain Nodes", use_container_width=True)

    # Topology Distribution
    entity_dist_img = "knowledge_graph/entity_distribution.png"
    if os.path.exists(entity_dist_img):
        st.image(entity_dist_img, caption="Figure 6: Entity Distribution & High In-Degree Biomedical Transmission Hubs", use_container_width=True)

    if len(nodes) > 0 and "type" in nodes.columns:
        st.markdown('<div class="section-title">Node Class Frequency Distribution</div>', unsafe_allow_html=True)
        node_freq = nodes["type"].value_counts().reset_index()
        node_freq.columns = ["Entity Class", "Total Nodes"]

        fig_node_bar = px.bar(
            node_freq,
            x="Entity Class",
            y="Total Nodes",
            text="Total Nodes",
            color_discrete_sequence=["#1e40af"]
        )
        fig_node_bar.update_layout(
            height=380,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
        )
        st.plotly_chart(fig_node_bar, use_container_width=True)

# ============================================================
# PAGE 6 — BIOMEDICAL ENTITY PROFILER
# ============================================================

elif page == "Biomedical Entity Profiler":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">Biomedical Entity Profiler</h1>
        <div class="header-subtitle">
            Inspection interface for all discrete concepts extracted via biomedical Named Entity Recognition (NER).
        </div>
    </div>
    """, unsafe_allow_html=True)

    if len(nodes) > 0 and "type" in nodes.columns:
        types = ["All"] + sorted([str(t) for t in nodes["type"].dropna().unique().tolist()])
        selected_type = st.selectbox("Filter by Entity Class", types)

        filtered = nodes.copy() if selected_type == "All" else nodes[nodes["type"] == selected_type]

        query = st.text_input("Search entity name...", "")
        if query:
            filtered = filtered[filtered["name"].astype(str).str.contains(query, case=False, na=False)]

        st.caption(f"Displaying {len(filtered):,} matching entities")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 7 — METHODOLOGY & EVALUATION
# ============================================================

elif page == "Methodology & Evaluation":

    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">System Methodology & Mid-Semester Implementation</h1>
        <div class="header-subtitle">
            Architecture pipeline, data flow specifications, and evaluation criteria for the Phase 1 defense.
        </div>
    </div>
    """, unsafe_allow_html=True)

    pipeline_stages = [
        ("01", "Multi-Source Data Ingestion", "Ingestion from WHO Outbreak News (50), PubMed NCBI (2,500), and GBIF Occurrence API (3,000) totaling 5,550 validated data points."),
        ("02", "Distributed Batch Preprocessing", "Apache Spark (Scala + PySpark) pipeline performing schema harmonization, null-value reconciliation, deduplication, and coordinate bounding."),
        ("03", "Biomedical Information Extraction", "spaCy en_core_web_sm pipeline and regex fallback extracting Disease, Pathogen, Host Animal, Location, and Date entities."),
        ("04", "Knowledge Graph Construction", "NetworkX graph construction generating 4,796 nodes and 12,471 directed transmission relationships across 6 entity classes."),
        ("05", "Spatio-Temporal & Signal Analytics", "Longitudinal 53-year trend modeling (1965–2027) and composite mathematical risk scoring for emerging pathogen alerts."),
        ("06", "Decision Support Intelligence Center", "Interactive Streamlit web application providing epidemiological filtering, GIS mapping, and graph topology inspection.")
    ]

    for num, title, desc in pipeline_stages:
        st.markdown(f"""
        <div class="stage-card">
            <div class="stage-num">Stage {num}</div>
            <div class="stage-title">{title}</div>
            <div class="stage-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Mid-Semester Milestone Evaluation Matrix</div>', unsafe_allow_html=True)

    matrix_data = {
        "Component": [
            "Data Lake Volume",
            "Distributed Processing",
            "Information Extraction",
            "Knowledge Representation",
            "Risk Quantification",
            "Interactive Dashboard"
        ],
        "Phase 1 Delivered (Mid-Semester)": [
            "5,550 records (55.5% achieved; 3,000 GBIF + 2,500 PubMed + 50 WHO)",
            "Local Scala Spark 4.0.1 + PySpark automated batch pipeline",
            "Hybrid spaCy NER + high-speed biomedical regex extraction",
            "4,796 nodes, 12,471 edges, in-degree transmission hubs",
            "Composite 4-factor risk scoring formula across 53 years",
            "7-page operational surveillance intelligence dashboard"
        ],
        "Phase 2 Target (End-Semester)": [
            "10,000+ records (ProMED, FAO EMPRES-i, GISAID integration)",
            "Dataproc Serverless cluster deployment on Google Cloud",
            "Fine-tuned BioLinkBERT transformer embeddings for relation classification",
            "Neo4j persistent graph database with Cypher query endpoints",
            "Graph Neural Network (GNN) link prediction for spillover forecasting",
            "Automated alert notification service and REST API layer"
        ]
    }
    st.table(pd.DataFrame(matrix_data))

# ============================================================
# INSTITUTIONAL FOOTER
# ============================================================

st.markdown("""
<div class="dash-footer">
    <b>OneHealth Nexus</b> — Big Data & Text Analytics Platform for Zoonotic Early Warning<br>
    Mid-Semester Interim Evaluation Release | Version 0.5.0-beta
</div>
""", unsafe_allow_html=True)