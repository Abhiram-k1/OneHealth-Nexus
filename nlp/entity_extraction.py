import pandas as pd
import os
import re

# -----------------------------------------
# Load NLP model or robust regex fallback
# -----------------------------------------
nlp = None
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
    print("Loaded spaCy model: en_core_web_sm (optimized for high-throughput NER)")
except Exception:
    print("spaCy model not loaded; operating in high-performance biomedical regex extraction mode.")

# -----------------------------------------
# Paths
# -----------------------------------------
input_file = "data/processed/spark_output/processed_documents.txt"
output_dir = "knowledge_graph"

os.makedirs(output_dir, exist_ok=True)

# -----------------------------------------
# Read Spark output
# -----------------------------------------
df = pd.read_csv(
    input_file,
    sep="\t",
    encoding="utf-8",
    dtype=str
).fillna("")

print("======================================")
print("       ONEHEALTH NEXUS - NLP")
print("======================================")

print("\nInput records to process:", len(df))

# -----------------------------------------
# Curated Domain Lexicons
# -----------------------------------------
disease_keywords = [
    "influenza", "avian influenza", "bird flu",
    "covid", "covid-19", "coronavirus",
    "dengue", "malaria", "cholera", "ebola",
    "mpox", "monkeypox", "rabies",
    "tuberculosis", "typhoid", "measles",
    "nipah", "hepatitis", "leptospirosis",
    "kyasanur forest disease", "scrub typhus",
    "brucellosis", "anthrax"
]

pathogen_keywords = [
    "virus", "influenza virus",
    "coronavirus", "sars-cov-2",
    "h5n1", "h7n9", "ebolavirus",
    "bacteria", "bacterium", "bacillus anthracis",
    "orientia tsutsugamushi", "leptospira",
    "parasite", "fungus", "fungi"
]

animal_keywords = [
    "bird", "birds", "poultry",
    "chicken", "duck", "pig", "swine",
    "bat", "bats", "dog", "dogs",
    "cat", "cats", "cattle", "cow",
    "livestock", "horse", "goat",
    "sheep", "wildlife", "mammal",
    "rodent", "rodents", "monkey", "primate"
]

location_patterns = [
    "India", "Kerala", "Tamil Nadu", "Karnataka", "Maharashtra", "Gujarat",
    "Delhi", "West Bengal", "Uttar Pradesh", "Assam", "Punjab", "Rajasthan",
    "China", "Egypt", "Indonesia", "Vietnam", "Bangladesh", "Pakistan",
    "Nepal", "Thailand", "Brazil", "United States", "USA", "Africa", "Europe"
]

date_regex = re.compile(r"\b(19\d\d|20\d\d)\b")

# -----------------------------------------
# Stable node storage
# -----------------------------------------
node_lookup = {}
nodes = []
relationships = []

next_node_id = 1


def get_or_create_node(name, entity_type, source):
    global next_node_id

    name = str(name).strip()

    if not name or len(name) < 2:
        return None

    key = (
        name.lower(),
        entity_type
    )

    if key in node_lookup:
        return node_lookup[key]

    node_id = next_node_id
    next_node_id += 1

    node_lookup[key] = node_id

    nodes.append({
        "node_id": node_id,
        "name": name,
        "type": entity_type,
        "source": source
    })

    return node_id


# -----------------------------------------
# Process documents
# -----------------------------------------
print("\nExtracting entities across documents...")
for idx, row in df.iterrows():
    if (idx + 1) % 500 == 0 or idx == len(df) - 1:
        print(f"  Processed {idx + 1}/{len(df)} documents...")

    document_id = str(row.get("document_id", f"DOC_{idx+1}"))
    source = str(row.get("source", "Unknown"))
    text = str(row.get("clean_text", ""))

    if not text or text == "nan":
        continue

    text_lower = text.lower()

    # Document node
    document_node = get_or_create_node(
        document_id,
        "Document",
        source
    )

    # Locations and Dates
    if nlp is not None:
        doc = nlp(text[:10000])
        for ent in doc.ents:
            if ent.label_ == "GPE":
                entity_node = get_or_create_node(ent.text, "Location", source)
                if entity_node:
                    relationships.append({
                        "source": document_node,
                        "target": entity_node,
                        "relationship": "MENTIONS_LOCATION"
                    })
            elif ent.label_ == "DATE":
                entity_node = get_or_create_node(ent.text, "Date", source)
                if entity_node:
                    relationships.append({
                        "source": document_node,
                        "target": entity_node,
                        "relationship": "HAS_DATE"
                    })
    else:
        # Regex extraction for locations
        for loc in location_patterns:
            if re.search(r"\b" + re.escape(loc) + r"\b", text, re.IGNORECASE):
                entity_node = get_or_create_node(loc, "Location", source)
                if entity_node:
                    relationships.append({
                        "source": document_node,
                        "target": entity_node,
                        "relationship": "MENTIONS_LOCATION"
                    })
        # Regex extraction for dates
        for dm in date_regex.finditer(text):
            d_val = dm.group(1)
            entity_node = get_or_create_node(d_val, "Date", source)
            if entity_node:
                relationships.append({
                    "source": document_node,
                    "target": entity_node,
                    "relationship": "HAS_DATE"
                })

    # Diseases
    for keyword in disease_keywords:
        if keyword in text_lower:
            entity_node = get_or_create_node(keyword, "Disease", source)
            if entity_node:
                relationships.append({
                    "source": document_node,
                    "target": entity_node,
                    "relationship": "MENTIONS_DISEASE"
                })

    # Pathogens
    for keyword in pathogen_keywords:
        if keyword in text_lower:
            entity_node = get_or_create_node(keyword, "Pathogen", source)
            if entity_node:
                relationships.append({
                    "source": document_node,
                    "target": entity_node,
                    "relationship": "MENTIONS_PATHOGEN"
                })

    # Animals
    for keyword in animal_keywords:
        if keyword in text_lower:
            entity_node = get_or_create_node(keyword, "Animal", source)
            if entity_node:
                relationships.append({
                    "source": document_node,
                    "target": entity_node,
                    "relationship": "MENTIONS_ANIMAL"
                })

# -----------------------------------------
# DataFrames
# -----------------------------------------
nodes_df = pd.DataFrame(nodes)
relationships_df = pd.DataFrame(relationships)

# Remove duplicate relationships
relationships_df = relationships_df.drop_duplicates()

# -----------------------------------------
# Save
# -----------------------------------------
nodes_file = os.path.join(output_dir, "nodes.csv")
relationships_file = os.path.join(output_dir, "relationships.csv")

nodes_df.to_csv(nodes_file, index=False)
relationships_df.to_csv(relationships_file, index=False)

# -----------------------------------------
# Results
# -----------------------------------------
print("\n======================================")
print("NLP EXTRACTION COMPLETED")
print("======================================")
print("\nNodes created:", len(nodes_df))
print("Relationships created:", len(relationships_df))
print("\nNode types breakdown:")
print(nodes_df["type"].value_counts())
print("\nOutput files:")
print(" ", nodes_file)
print(" ", relationships_file)
print("======================================")