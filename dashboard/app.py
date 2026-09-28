import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OneHealth Nexus | Intelligence Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b172a;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #0b172a;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #64748b;
        margin-bottom: 25px;
    }

    /* Hero section */
    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #0b172a 0%,
            #123b5d 55%,
            #087f8c 100%
        );
        color: white;
        margin-bottom: 25px;
        box-shadow: 0px 8px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
    }

    .hero-text {
        font-size: 16px;
        opacity: 0.9;
        margin-top: 8px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 4px 18px rgba(15,23,42,0.06);
        min-height: 120px;
    }

    .kpi-title {
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 32px;
        font-weight: 800;
        color: #0b172a;
        margin-top: 8px;
    }

    .kpi-description {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 5px;
    }

    /* Section titles */
    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #0b172a;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* Signal card */
    .signal-card {
        background: white;
        border-left: 5px solid #ef4444;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    }

    .signal-name {
        font-size: 20px;
        font-weight: 750;
        color: #0b172a;
    }

    .signal-score {
        font-size: 28px;
        font-weight: 800;
        color: #ef4444;
    }

    /* Pipeline */
    .pipeline-step {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        min-height: 120px;
    }

    .pipeline-number {
        font-size: 13px;
        color: #0891b2;
        font-weight: 700;
    }

    .pipeline-name {
        font-size: 16px;
        font-weight: 700;
        color: #0b172a;
        margin-top: 8px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 30px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

summary_file = "knowledge_graph/graph_summary.csv"
entities_file = "knowledge_graph/important_entities.csv"
temporal_file = "analysis/temporal_summary.csv"
signal_file = "analysis/emerging_signals.csv"
nodes_file = "knowledge_graph/nodes.csv"
relationships_file = "knowledge_graph/relationships.csv"
gbif_file = "data/processed/cleaned_gbif.csv"

summary = pd.read_csv(summary_file)
entities = pd.read_csv(entities_file)
temporal = pd.read_csv(temporal_file)
signals = pd.read_csv(signal_file)
nodes = pd.read_csv(nodes_file)
relationships = pd.read_csv(relationships_file)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_value(metric):
    row = summary[summary["metric"] == metric]

    if len(row) > 0:
        return row.iloc[0]["value"]

    return 0


def fmt_number(value):
    try:
        return f"{int(float(value)):,}"
    except:
        return str(value)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌍 OneHealth")
    st.markdown("### NEXUS")

    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠 Intelligence Overview",
            "🚨 Emerging Signals",
            "📈 Temporal Intelligence",
            "🌎 Spatial Intelligence",
            "🕸️ Knowledge Graph",
            "🧬 Entity Intelligence",
            "🔬 Methodology"
        ]
    )

    st.markdown("---")

    st.markdown(
        """
        **Data Sources**

        🏥 WHO Disease Outbreak News

        📚 PubMed

        🐾 GBIF
        """
    )

    st.markdown("---")

    st.caption("OneHealth Nexus")
    st.caption("TA + BDA Project")


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🌍 OneHealth Nexus
</div>

<div class="hero-text">
Large-Scale NLP and Temporal Knowledge Graphs
for Emerging Disease Intelligence
</div>

<div class="hero-text">
Connecting human health, animal occurrence and
environmental signals across time and space.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PAGE 1 — INTELLIGENCE OVERVIEW
# ============================================================

if page == "🏠 Intelligence Overview":

    st.markdown(
        '<div class="section-title">📊 Intelligence Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'A unified view of the OneHealth Nexus knowledge system.'
        '</div>',
        unsafe_allow_html=True
    )

    # KPI ROW
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
        <div class="kpi-title">Knowledge Nodes</div>
        <div class="kpi-value">{fmt_number(get_value("Total Nodes"))}</div>
        <div class="kpi-description">Entities + documents</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
        <div class="kpi-title">Relationships</div>
        <div class="kpi-value">{fmt_number(get_value("Total Relationships"))}</div>
        <div class="kpi-description">Knowledge connections</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
        <div class="kpi-title">Locations</div>
        <div class="kpi-value">{fmt_number(get_value("Locations"))}</div>
        <div class="kpi-description">Geographic entities</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
        <div class="kpi-title">Diseases</div>
        <div class="kpi-value">{fmt_number(get_value("Diseases"))}</div>
        <div class="kpi-description">Detected disease concepts</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="kpi-card">
        <div class="kpi-title">Pathogens</div>
        <div class="kpi-value">{fmt_number(get_value("Pathogens"))}</div>
        <div class="kpi-description">Detected pathogen concepts</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # --------------------------------------------------------
    # TWO COLUMN OVERVIEW
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">📈 Activity Over Time</div>',
            unsafe_allow_html=True
        )

        temporal["year"] = pd.to_numeric(
            temporal["year"],
            errors="coerce"
        )

        temporal["document_count"] = pd.to_numeric(
            temporal["document_count"],
            errors="coerce"
        )

        temporal = temporal.dropna(
            subset=["year", "document_count"]
        )

        temporal["year"] = temporal["year"].astype(int)

        fig = px.area(
            temporal,
            x="year",
            y="document_count",
            markers=True
        )

        fig.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title="Year",
            yaxis_title="Documents",
            plot_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.markdown(
            '<div class="section-title">🧩 Entity Composition</div>',
            unsafe_allow_html=True
        )

        entity_counts = nodes["type"].value_counts().reset_index()

        entity_counts.columns = [
            "type",
            "count"
        ]

        fig_entity = px.pie(
            entity_counts,
            names="type",
            values="count",
            hole=0.55
        )

        fig_entity.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(
            fig_entity,
            use_container_width=True
        )

    # --------------------------------------------------------
    # DATA MILESTONE PROGRESSION
    # --------------------------------------------------------
    if os.path.exists("analysis/data_milestone_target.png"):
        st.markdown('<div class="section-title">📊 Multi-Modal Data Scaling Progression</div>', unsafe_allow_html=True)
        st.image("analysis/data_milestone_target.png", caption="OneHealth Nexus — Data Scaling Progression: Current 5,550 Points vs 10,000 Target", use_container_width=True)

    # --------------------------------------------------------
    # SIGNAL PREVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🚨 Emerging Signal Monitor</div>',
        unsafe_allow_html=True
    )

    preview = signals.head(5)

    for _, row in preview.iterrows():

        st.markdown(f"""
        <div class="signal-card">

        <div class="signal-name">
        {str(row["disease"]).title()}
        </div>

        <div style="color:#64748b;">
        Recent mentions: {row["recent_mentions"]}
        &nbsp;&nbsp; | &nbsp;&nbsp;
        Sources: {row["source_count"]}
        </div>

        <div class="signal-score">
        {float(row["signal_score"]):.1f}
        </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE 2 — EMERGING SIGNALS
# ============================================================

elif page == "🚨 Emerging Signals":

    st.markdown(
        '<div class="section-title">🚨 Emerging Signal Monitor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Disease signals are calculated from recent activity, '
        'source diversity and document frequency.'
        '</div>',
        unsafe_allow_html=True
    )

    if os.path.exists("analysis/emerging_signals_ranking.png"):
        st.image("analysis/emerging_signals_ranking.png", caption="OneHealth Nexus — Emerging Disease Risk Prioritization Ranking", use_container_width=True)

    signals["signal_score"] = pd.to_numeric(
        signals["signal_score"],
        errors="coerce"
    )

    signals = signals.dropna(
        subset=["signal_score"]
    )

    # Filter
    minimum_score = st.slider(
        "Minimum signal score",
        0.0,
        100.0,
        0.0,
        1.0
    )

    filtered = signals[
        signals["signal_score"] >= minimum_score
    ]

    # Main chart
    fig = px.bar(
        filtered.head(15),
        x="signal_score",
        y="disease",
        orientation="h",
        text="signal_score",
        title="Emerging Disease Signal Landscape"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        height=550,
        plot_bgcolor="white",
        xaxis_title="Signal Score",
        yaxis_title="Disease"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Signal Details")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "The signal score is a project-defined analytical indicator, "
        "not a clinical diagnosis or official outbreak prediction."
    )


# ============================================================
# PAGE 3 — TEMPORAL INTELLIGENCE
# ============================================================

elif page == "📈 Temporal Intelligence":

    st.markdown(
        '<div class="section-title">📈 Temporal Intelligence</div>',
        unsafe_allow_html=True
    )

    temporal["year"] = pd.to_numeric(
        temporal["year"],
        errors="coerce"
    )

    temporal["document_count"] = pd.to_numeric(
        temporal["document_count"],
        errors="coerce"
    )

    temporal = temporal.dropna(
        subset=["year", "document_count"]
    )

    temporal["year"] = temporal["year"].astype(int)

    fig = px.line(
        temporal,
        x="year",
        y="document_count",
        markers=True,
        text="document_count"
    )

    fig.update_traces(
        textposition="top center"
    )

    fig.update_xaxes(
        dtick=1,
        title="Year"
    )

    fig.update_yaxes(
        title="Number of Documents"
    )

    fig.update_layout(
        height=500,
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Year-wise Dataset Activity")

    st.dataframe(
        temporal,
        use_container_width=True,
        hide_index=True
    )

    if os.path.exists("analysis/temporal_longitudinal_surge.png"):
        st.markdown("### Longitudinal Historical Outbreak Surge (1990–2027)")
        st.image("analysis/temporal_longitudinal_surge.png", caption="OneHealth Nexus — 53-Year Longitudinal Outbreak Surveillance Activity", use_container_width=True)


# ============================================================
# PAGE 4 — SPATIAL INTELLIGENCE
# ============================================================

elif page == "🌎 Spatial Intelligence":

    st.markdown(
        '<div class="section-title">🌎 Spatial Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Geographic distribution of animal occurrence records from GBIF.'
        '</div>',
        unsafe_allow_html=True
    )

    if os.path.exists(gbif_file):

        gbif = pd.read_csv(
            gbif_file,
            dtype=str
        ).fillna("")

        # Find coordinates automatically
        lat_col = None
        lon_col = None

        for col in gbif.columns:

            name = col.lower()

            if "lat" in name:
                lat_col = col

            if "lon" in name or "lng" in name:
                lon_col = col

        if lat_col and lon_col:

            gbif["latitude"] = pd.to_numeric(
                gbif[lat_col],
                errors="coerce"
            )

            gbif["longitude"] = pd.to_numeric(
                gbif[lon_col],
                errors="coerce"
            )

            gbif = gbif.dropna(
                subset=["latitude", "longitude"]
            )

            st.metric(
                "Mapped GBIF Occurrences",
                f"{len(gbif):,}"
            )

            fig_map = px.scatter_geo(
                gbif,
                lat="latitude",
                lon="longitude",
                projection="natural earth",
                title="Animal Occurrence Distribution"
            )

            fig_map.update_traces(
                marker=dict(
                    size=6,
                    opacity=0.65
                )
            )

            fig_map.update_layout(
                height=600,
                margin=dict(l=0, r=0, t=50, b=0)
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True
            )

        else:

            st.warning(
                "Latitude and longitude columns could not be detected."
            )

    else:

        st.warning(
            "GBIF processed dataset not found."
        )

    st.info(
        "GBIF occurrence records represent geographic animal observations. "
        "They should not be interpreted individually as disease observations."
    )

    spatial_vis = "analysis/spatial_biodiversity_heatmap.png"
    if os.path.exists(spatial_vis):
        st.markdown("#### 🗺️ High-Resolution Spatial Density & Hotspot Map")
        st.image(
            spatial_vis,
            caption="Spatial Distribution of 3,000 Animal Occurrences in India (Western Ghats, Indo-Gangetic, Himalaya)",
            use_container_width=True
        )


# ============================================================
# PAGE 5 — KNOWLEDGE GRAPH
# ============================================================

elif page == "🕸️ Knowledge Graph":

    st.markdown(
        '<div class="section-title">🕸️ Knowledge Graph Explorer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'A network representation connecting documents with '
        'diseases, pathogens, animals, dates and locations.'
        '</div>',
        unsafe_allow_html=True
    )

    # Graph metrics
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Nodes",
        fmt_number(len(nodes))
    )

    c2.metric(
        "Relationships",
        fmt_number(len(relationships))
    )

    c3.metric(
        "Node Types",
        fmt_number(nodes["type"].nunique())
    )

    st.markdown("")

    graph_image = "knowledge_graph/onehealth_subgraph.png"

    if os.path.exists(graph_image):

        st.image(
            graph_image,
            caption="OneHealth Nexus Knowledge Graph",
            width=950
        )

    else:

        st.warning(
            "Knowledge graph visualization not found."
        )

    st.markdown("### Node Type Distribution")

    node_counts = nodes["type"].value_counts().reset_index()

    node_counts.columns = [
        "type",
        "count"
    ]

    fig_nodes = px.bar(
        node_counts,
        x="type",
        y="count",
        text="count"
    )

    fig_nodes.update_layout(
        plot_bgcolor="white",
        xaxis_title="Entity Type",
        yaxis_title="Number of Nodes"
    )

    st.plotly_chart(
        fig_nodes,
        use_container_width=True
    )

    dist_image = "knowledge_graph/entity_distribution.png"
    if os.path.exists(dist_image):
        st.markdown("#### 🔬 Graph Topology & Key Transmission Hubs")
        st.image(
            dist_image,
            caption="Entity Class Distribution & Highest Connected Biomedical Hubs (2,720 Nodes, 10,946 Relationships)",
            use_container_width=True
        )


# ============================================================
# PAGE 6 — ENTITY INTELLIGENCE
# ============================================================

elif page == "🧬 Entity Intelligence":

    st.markdown(
        '<div class="section-title">🧬 Entity Intelligence</div>',
        unsafe_allow_html=True
    )

    entity_type = st.selectbox(
        "Select entity type",
        ["All"] + sorted(
            nodes["type"].dropna().unique().tolist()
        )
    )

    if entity_type == "All":

        filtered_nodes = nodes.copy()

    else:

        filtered_nodes = nodes[
            nodes["type"] == entity_type
        ]

    search = st.text_input(
        "🔎 Search entity"
    )

    if search:

        filtered_nodes = filtered_nodes[
            filtered_nodes["name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.write(
        f"Showing **{len(filtered_nodes):,}** entities"
    )

    st.dataframe(
        filtered_nodes,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 7 — METHODOLOGY
# ============================================================

elif page == "🔬 Methodology":

    st.markdown(
        '<div class="section-title">🔬 OneHealth Nexus Methodology</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'End-to-end architecture of the proposed system.'
        '</div>',
        unsafe_allow_html=True
    )

    # Pipeline
    steps = [
        ("01", "Data Sources", "WHO • PubMed • GBIF"),
        ("02", "Big Data Processing", "Apache Spark + Scala"),
        ("03", "Preprocessing", "Cleaning • Deduplication • Normalization"),
        ("04", "Text Analysis", "Python NLP + Entity Extraction"),
        ("05", "Knowledge Graph", "Entities + Relationships + Provenance"),
        ("06", "Temporal Analysis", "Activity across time"),
        ("07", "Spatial Analysis", "Geographic occurrence patterns"),
        ("08", "Signal Detection", "Emerging signal indicator"),
        ("09", "Dashboard", "Interactive intelligence interface")
    ]

    for number, name, description in steps:

        st.markdown(f"""
        <div class="pipeline-step">

        <div class="pipeline-number">
        STAGE {number}
        </div>

        <div class="pipeline-name">
        {name}
        </div>

        <div style="color:#64748b; margin-top:8px;">
        {description}
        </div>

        </div>

        <div style="text-align:center; font-size:20px; color:#0891b2;">
        ↓
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🎯 Project Objective")

    st.write(
        "OneHealth Nexus integrates heterogeneous health, scientific "
        "and animal-occurrence information into a unified analytical "
        "framework for exploring disease-related signals across "
        "time, geography and interconnected entities."
    )

    st.markdown("### 💡 Project Novelty")

    novelty1, novelty2, novelty3 = st.columns(3)

    with novelty1:
        st.info(
            "**Tri-domain integration**\n\n"
            "Human-health literature, outbreak information "
            "and animal occurrence data."
        )

    with novelty2:
        st.info(
            "**Knowledge representation**\n\n"
            "Entities and relationships are represented "
            "as an interconnected graph."
        )

    with novelty3:
        st.info(
            "**Signal-oriented analysis**\n\n"
            "Temporal activity, source diversity and "
            "frequency are combined into an analytical indicator."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

🌍 <b>OneHealth Nexus</b><br>

Large-Scale NLP and Temporal Knowledge Graphs
for Emerging Disease Intelligence<br><br>

TA + Big Data Analysis Project

</div>
""", unsafe_allow_html=True)