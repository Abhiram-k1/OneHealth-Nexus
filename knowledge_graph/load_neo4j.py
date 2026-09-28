import os
from pathlib import Path
import pandas as pd
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[1]
KG = ROOT / "knowledge_graph"

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "")

if not password:
    raise SystemExit(
        "NEO4J_PASSWORD is not set. Set it in PowerShell before running this script."
    )

nodes = pd.read_csv(KG / "nodes.csv", dtype=str).fillna("")
rels = pd.read_csv(KG / "relationships.csv", dtype=str).fillna("")

driver = GraphDatabase.driver(uri, auth=(user, password))

def load(tx):
    tx.run("CREATE CONSTRAINT onehealth_node_id IF NOT EXISTS FOR (n:Entity) REQUIRE n.node_id IS UNIQUE")
    for _, r in nodes.iterrows():
        tx.run(
            "MERGE (n:Entity {node_id:$node_id}) "
            "SET n.label=$label, n.type=$type",
            node_id=r["node_id"], label=r["label"], type=r["type"]
        )
    for _, r in rels.iterrows():
        # Relationship type cannot be a parameter, so validate against generated labels.
        rel_type = r["relation"].strip().upper()
        if not rel_type.isidentifier():
            continue
        query = (
            f"MATCH (a:Entity {{node_id:$source}}), "
            f"(b:Entity {{node_id:$target}}) "
            f"MERGE (a)-[r:{rel_type} {{document_id:$document_id, date:$date}}]->(b) "
            f"SET r.source=$source_dataset"
        )
        tx.run(
            query,
            source=r["source"], target=r["target"],
            document_id=r["document_id"], date=r["date"],
            source_dataset=r["source_dataset"]
        )

with driver.session() as session:
    session.execute_write(load)

driver.close()
print("Neo4j loading completed.")
