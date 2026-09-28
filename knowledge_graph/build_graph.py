import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# ============================================================
# ONEHEALTH NEXUS - KNOWLEDGE GRAPH
# ============================================================

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------

nodes_file = "knowledge_graph/nodes.csv"
relationships_file = "knowledge_graph/relationships.csv"

graph_image = "knowledge_graph/onehealth_graph.png"
subgraph_image = "knowledge_graph/onehealth_subgraph.png"
summary_file = "knowledge_graph/graph_summary.csv"
important_nodes_file = "knowledge_graph/important_entities.csv"

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

print("======================================")
print("   ONEHEALTH NEXUS - KNOWLEDGE GRAPH")
print("======================================")

print("\nLoading nodes...")

nodes = pd.read_csv(
    nodes_file,
    dtype=str
).fillna("")

print("Loading relationships...")

relationships = pd.read_csv(
    relationships_file,
    dtype=str
).fillna("")

print("\nInput data loaded successfully.")

print("Total nodes:", len(nodes))
print("Total relationships:", len(relationships))


# ============================================================
# CREATE DIRECTED GRAPH
# ============================================================

G = nx.DiGraph()

print("\nCreating graph nodes...")

# ------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------

for _, row in nodes.iterrows():

    node_id = str(row["node_id"])

    G.add_node(
        node_id,
        name=row["name"],
        type=row["type"],
        source=row["source"]
    )


# ============================================================
# ADD RELATIONSHIPS
# ============================================================

print("Creating graph relationships...")

valid_relationships = 0

for _, row in relationships.iterrows():

    source = str(row["source"])
    target = str(row["target"])
    relationship = str(row["relationship"])

    # Only add relationship if both nodes exist
    if source in G.nodes and target in G.nodes:

        G.add_edge(
            source,
            target,
            relationship=relationship
        )

        valid_relationships += 1


# ============================================================
# BASIC GRAPH STATISTICS
# ============================================================

print("\n======================================")
print("GRAPH STATISTICS")
print("======================================")

number_nodes = G.number_of_nodes()
number_edges = G.number_of_edges()

print("\nTotal nodes:", number_nodes)
print("Total relationships:", number_edges)

print("Valid relationships:", valid_relationships)

# Density
density = nx.density(G)

print("Graph density:", round(density, 6))


# ============================================================
# NODE TYPE ANALYSIS
# ============================================================

print("\n======================================")
print("NODE TYPE DISTRIBUTION")
print("======================================")

node_type_counts = nodes["type"].value_counts()

print(node_type_counts)


# ============================================================
# DEGREE ANALYSIS
# ============================================================

print("\n======================================")
print("IMPORTANT ENTITIES")
print("======================================")

# Calculate degree
degree_data = []

for node in G.nodes():

    degree = G.degree(node)
    in_degree = G.in_degree(node)
    out_degree = G.out_degree(node)

    name = G.nodes[node].get("name", "")
    node_type = G.nodes[node].get("type", "")
    source = G.nodes[node].get("source", "")

    degree_data.append({
        "node_id": node,
        "name": name,
        "type": node_type,
        "source": source,
        "degree": degree,
        "in_degree": in_degree,
        "out_degree": out_degree
    })


degree_df = pd.DataFrame(degree_data)

# Sort by degree
degree_df = degree_df.sort_values(
    by="degree",
    ascending=False
)

print("\nTop 20 important entities:")

print(
    degree_df[
        [
            "name",
            "type",
            "degree",
            "in_degree",
            "out_degree"
        ]
    ].head(20).to_string(index=False)
)


# ============================================================
# SAVE IMPORTANT ENTITIES
# ============================================================

degree_df.to_csv(
    important_nodes_file,
    index=False
)

print(
    "\nImportant entities saved to:",
    important_nodes_file
)


# ============================================================
# GRAPH SUMMARY
# ============================================================

summary = pd.DataFrame({
    "metric": [
        "Total Nodes",
        "Total Relationships",
        "Graph Density",
        "Documents",
        "Dates",
        "Locations",
        "Animals",
        "Diseases",
        "Pathogens"
    ],

    "value": [
        number_nodes,
        number_edges,
        density,
        node_type_counts.get("Document", 0),
        node_type_counts.get("Date", 0),
        node_type_counts.get("Location", 0),
        node_type_counts.get("Animal", 0),
        node_type_counts.get("Disease", 0),
        node_type_counts.get("Pathogen", 0)
    ]
})


summary.to_csv(
    summary_file,
    index=False
)

print(
    "\nGraph summary saved to:",
    summary_file
)


# ============================================================
# CREATE READABLE SUBGRAPH
# ============================================================

print("\nCreating graph visualization...")

# Take top important nodes
top_nodes = degree_df.head(40)["node_id"].tolist()

# Create subgraph
subgraph = G.subgraph(top_nodes).copy()

print(
    "Nodes used for visualization:",
    subgraph.number_of_nodes()
)

print(
    "Relationships used for visualization:",
    subgraph.number_of_edges()
)


# ============================================================
# DRAW SUBGRAPH
# ============================================================

if subgraph.number_of_nodes() > 0:

    plt.figure(figsize=(18, 12))

    # Layout
    pos = nx.spring_layout(
        subgraph,
        seed=42,
        k=1.5
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        subgraph,
        pos,
        node_size=900,
        alpha=0.8
    )

    # Draw edges
    nx.draw_networkx_edges(
        subgraph,
        pos,
        arrows=True,
        arrowsize=15,
        alpha=0.5
    )

    # Labels
    labels = {}

    for node in subgraph.nodes():

        name = subgraph.nodes[node].get(
            "name",
            ""
        )

        node_type = subgraph.nodes[node].get(
            "type",
            ""
        )

        # Short label for readability
        if len(name) > 25:
            name = name[:25] + "..."

        labels[node] = f"{name}\n[{node_type}]"

    nx.draw_networkx_labels(
        subgraph,
        pos,
        labels,
        font_size=7
    )

    plt.title(
        "OneHealth Nexus Knowledge Graph",
        fontsize=18
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        subgraph_image,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "Readable graph saved to:",
        subgraph_image
    )


# ============================================================
# CREATE FULL GRAPH IMAGE
# ============================================================

# Only create full graph if manageable
# The graph can contain many nodes, so we use a smaller
# representation for the full structure.

print("\nCreating full graph overview...")

if False:

    plt.figure(figsize=(20, 15))

    pos_full = nx.spring_layout(
        G,
        seed=42,
        k=0.3
    )

    nx.draw_networkx_nodes(
        G,
        pos_full,
        node_size=20,
        alpha=0.5
    )

    nx.draw_networkx_edges(
        G,
        pos_full,
        arrows=False,
        alpha=0.15
    )

    plt.title(
        "OneHealth Nexus - Full Knowledge Graph",
        fontsize=18
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        graph_image,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "Full graph saved to:",
        graph_image
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n======================================")
print("KNOWLEDGE GRAPH COMPLETED")
print("======================================")

print("\nFinal graph statistics:")

print(
    "Nodes:",
    number_nodes
)

print(
    "Relationships:",
    number_edges
)

print(
    "Density:",
    round(density, 6)
)

print("\nGenerated files:")

print(
    "1.",
    graph_image
)

print(
    "2.",
    subgraph_image
)

print(
    "3.",
    summary_file
)

print(
    "4.",
    important_nodes_file
)

print("\n======================================")
print("       PROJECT STAGE COMPLETED")
print("======================================")