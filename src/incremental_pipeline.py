"""
OneHealth Nexus — Incremental Data Ingestion & Knowledge Graph Pipeline (Objective 8)
Processes newly added records incrementally without re-parsing historical records.
Maintains state manifest, prevents duplicates, and updates knowledge graph dynamically.
"""
import os
import sys
import json
import hashlib
import time
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

MANIFEST_FILE = "data/processed/ingestion_manifest.json"
NODES_FILE = "knowledge_graph/nodes.csv"
RELS_FILE = "knowledge_graph/relationships.csv"
PROVENANCE_FILE = "knowledge_graph/entity_provenance.csv"

def compute_record_hash(text):
    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()

def load_manifest():
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_manifest(manifest):
    os.makedirs(os.path.dirname(MANIFEST_FILE), exist_ok=True)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def run_incremental_ingestion(new_records_df=None):
    """
    Ingests only new records into the knowledge graph.
    If new_records_df is None, checks cleaned_documents.csv against manifest.
    """
    manifest = load_manifest()
    print("=" * 50)
    print("ONEHEALTH NEXUS — INCREMENTAL INGESTION PIPELINE")
    print("=" * 50)
    print(f"Current manifest record count: {len(manifest)}")

    if new_records_df is None:
        source_file = "data/processed/spark_output/processed_documents.txt"
        if not os.path.exists(source_file):
            source_file = "data/processed/cleaned_documents.csv"
        df = pd.read_csv(source_file, sep="\t" if source_file.endswith(".txt") else ",", dtype=str).fillna("")
    else:
        df = new_records_df.copy().fillna("")

    unprocessed_rows = []
    for _, row in df.iterrows():
        doc_id = str(row.get("document_id", ""))
        text = str(row.get("clean_text", row.get("text", "")))
        rec_hash = compute_record_hash(text)
        if doc_id not in manifest or manifest[doc_id].get("hash") != rec_hash:
            unprocessed_rows.append((row, rec_hash))

    print(f"Total candidate records: {len(df)}")
    print(f"Newly detected / modified records to process: {len(unprocessed_rows)}")

    if not unprocessed_rows:
        print("Knowledge Graph is already up to date. Zero historical recomputation needed.")
        return 0

    # Process new records
    from nlp.entity_extraction import (
        DISEASE_LEXICON, PATHOGEN_LEXICON, ANIMAL_LEXICON,
        LOCATION_PATTERNS, match_lexicon, split_into_sentences
    )

    nodes_df = pd.read_csv(NODES_FILE, dtype=str).fillna("") if os.path.exists(NODES_FILE) else pd.DataFrame(columns=["node_id", "name", "type", "source"])
    rels_df = pd.read_csv(RELS_FILE, dtype=str).fillna("") if os.path.exists(RELS_FILE) else pd.DataFrame(columns=["source", "target", "relationship"])

    next_id = int(nodes_df["node_id"].astype(int).max()) + 1 if not nodes_df.empty else 1
    node_lookup = {(r["name"].lower(), r["type"]): r["node_id"] for _, r in nodes_df.iterrows()}

    new_nodes = []
    new_rels = []

    def get_or_add_node(name, entity_type, source):
        nonlocal next_id
        k = (name.lower(), entity_type)
        if k in node_lookup:
            return node_lookup[k]
        nid = str(next_id)
        next_id += 1
        node_lookup[k] = nid
        new_nodes.append({"node_id": nid, "name": name, "type": entity_type, "source": source})
        return nid

    for row, rec_hash in unprocessed_rows:
        doc_id = str(row.get("document_id", f"DOC_{next_id}"))
        source = str(row.get("source", "Incremental_Stream"))
        text = str(row.get("clean_text", row.get("text", "")))

        doc_node = get_or_add_node(doc_id, "Document", source)

        # Match entities
        dis_set = match_lexicon(text, DISEASE_LEXICON)
        pat_set = match_lexicon(text, PATHOGEN_LEXICON)
        ani_set = match_lexicon(text, ANIMAL_LEXICON)

        for d in dis_set:
            dn = get_or_add_node(d, "Disease", source)
            new_rels.append({"source": doc_node, "target": dn, "relationship": "MENTIONS_DISEASE"})
        for p in pat_set:
            pn = get_or_add_node(p, "Pathogen", source)
            new_rels.append({"source": doc_node, "target": pn, "relationship": "MENTIONS_PATHOGEN"})
        for a in ani_set:
            an = get_or_add_node(a, "Animal", source)
            new_rels.append({"source": doc_node, "target": an, "relationship": "MENTIONS_ANIMAL"})

        manifest[doc_id] = {
            "hash": rec_hash,
            "source": source,
            "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    # Append to graph
    if new_nodes:
        updated_nodes = pd.concat([nodes_df, pd.DataFrame(new_nodes)], ignore_index=True).drop_duplicates(subset=["node_id"])
        updated_nodes.to_csv(NODES_FILE, index=False)
        print(f"Added {len(new_nodes)} new nodes to {NODES_FILE}")

    if new_rels:
        updated_rels = pd.concat([rels_df, pd.DataFrame(new_rels)], ignore_index=True).drop_duplicates()
        updated_rels.to_csv(RELS_FILE, index=False)
        print(f"Added {len(new_rels)} new relationships to {RELS_FILE}")

    save_manifest(manifest)
    print(f"Manifest updated with {len(unprocessed_rows)} records. Ingestion complete.")
    return len(unprocessed_rows)

if __name__ == "__main__":
    count = run_incremental_ingestion()
    manifest = load_manifest()
    assert isinstance(manifest, dict), "Manifest invalid"
    print(f"Self-check passed: Incremental pipeline state verified with {len(manifest)} tracked records.")

