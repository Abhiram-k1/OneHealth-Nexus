"""
OneHealth Nexus — Improved NLP Entity & Relationship Extraction Engine (Pipeline A)
Includes regex word boundaries, domain normalization, sentence-level provenance, and cross-domain relations.
"""
import os
import re
import pandas as pd

# Load spaCy if available
nlp = None
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
    print("Loaded spaCy model: en_core_web_sm (optimized for high-throughput NER)")
except Exception:
    print("spaCy model not loaded; operating in high-performance biomedical regex extraction mode.")

input_file = "data/processed/spark_output/processed_documents.txt"
if not os.path.exists(input_file):
    input_file = "data/processed/cleaned_documents.csv"

output_dir = "knowledge_graph"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(input_file, sep="\t" if input_file.endswith(".txt") else ",", dtype=str).fillna("")
print(f"Loaded {len(df)} input records for entity extraction.")

# Canonical Normalization Dictionaries with regex patterns
DISEASE_LEXICON = {
    "COVID-19": [r"\bcovid(?:-19)?\b", r"\bcoronavirus disease\b", r"\bsars-cov-2 infection\b"],
    "Avian Influenza": [r"\bavian influenza\b", r"\bbird flu\b", r"\bh5n1 influenza\b", r"\bh7n9 influenza\b"],
    "Influenza": [r"\binfluenza\b", r"\bseasonal flu\b", r"\bh1n1\b"],
    "Dengue": [r"\bdengue(?: fever)?\b"],
    "Malaria": [r"\bmalaria\b"],
    "Cholera": [r"\bcholera\b"],
    "Ebola": [r"\bebola(?: virus disease)?\b"],
    "Mpox": [r"\bmpox\b", r"\bmonkeypox\b"],
    "Rabies": [r"\brabies\b"],
    "Tuberculosis": [r"\btuberculosis\b", r"\bmycobacterial infection\b"],
    "Typhoid": [r"\btyphoid(?: fever)?\b", r"\benteric fever\b"],
    "Measles": [r"\bmeasles\b"],
    "Nipah Virus Disease": [r"\bnipah(?: virus)?(?: infection| disease)?\b"],
    "Hepatitis": [r"\bhepatitis(?: [a-e])?\b"],
    "Leptospirosis": [r"\bleptospirosis\b"],
    "Kyasanur Forest Disease": [r"\bkyasanur forest disease\b", r"\bkfd\b"],
    "Scrub Typhus": [r"\bscrub typhus\b"],
    "Brucellosis": [r"\bbrucellosis\b"],
    "Anthrax": [r"\banthrax\b"],
    "Chikungunya": [r"\bchikungunya\b"],
    "Zika": [r"\bzika(?: virus)?\b"],
    "Foot and Mouth Disease": [r"\bfoot and mouth disease\b", r"\bfmd\b"],
    "African Swine Fever": [r"\bafrican swine fever\b", r"\basf\b"]
}

PATHOGEN_LEXICON = {
    "SARS-CoV-2": [r"\bsars-cov-2\b", r"\bcoronavirus\b"],
    "Influenza A / H5N1": [r"\bh5n1\b", r"\binfluenza a virus\b", r"\bavian influenza virus\b"],
    "Influenza A / H7N9": [r"\bh7n9\b"],
    "Ebolavirus": [r"\bebolavirus\b", r"\bebola virus\b"],
    "Nipah Virus": [r"\bnipah virus\b"],
    "Lyssavirus (Rabies)": [r"\blyssavirus\b", r"\brabies virus\b"],
    "Bacillus anthracis": [r"\bbacillus anthracis\b"],
    "Orientia tsutsugamushi": [r"\borientia tsutsugamushi\b"],
    "Leptospira": [r"\bleptospira\b", r"\bleptospira interrogans\b"],
    "Brucella": [r"\bbrucella\b", r"\bbrucella abortus\b"],
    "Plasmodium": [r"\bplasmodium\b", r"\bplasmodium falciparum\b", r"\bplasmodium vivax\b"],
    "Vibrio cholerae": [r"\bvibrio cholerae\b"],
    "Mycobacterium tuberculosis": [r"\bmycobacterium tuberculosis\b"],
    "African Swine Fever Virus": [r"\basfv\b", r"\bafrican swine fever virus\b"],
    "Aphthovirus (FMDV)": [r"\baphthovirus\b"]
}

ANIMAL_LEXICON = {
    "Bat (Chiroptera)": [r"\bbats?\b", r"\bfruit bats?\b", r"\bpteropus\b", r"\bchiroptera\b"],
    "Poultry / Avian Host": [r"\bbirds?\b", r"\bpoultry\b", r"\bchickens?\b", r"\bducks?\b", r"\bgeese\b", r"\bwaterfowl\b"],
    "Swine (Sus scrofa)": [r"\bpigs?\b", r"\bswine\b", r"\bwild boars?\b"],
    "Cattle / Livestock": [r"\bcows?\b", r"\bcattle\b", r"\bbovine\b", r"\bbuffalo(?:es)?\b", r"\blivestock\b"],
    "Canine (Dog)": [r"\bdogs?\b", r"\bcanines?\b"],
    "Feline (Cat)": [r"\bcats?\b", r"\bfelines?\b"],
    "Horse (Equine)": [r"\bhorses?\b", r"\bequines?\b"],
    "Goat / Sheep": [r"\bgoats?\b", r"\bsheep\b", r"\bovine\b", r"\bcaprine\b"],
    "Rodent (Muridae)": [r"\brodents?\b", r"\brats?\b", r"\bmice\b", r"\bmouse\b"],
    "Non-Human Primate": [r"\bmonkeys?\b", r"\bprimates?\b", r"\bmacaques?\b"],
    "Mosquito Vector": [r"\bmosquito(?:es)?\b", r"\baedes\b", r"\banopheles\b"],
    "Tick Vector": [r"\bticks?\b", r"\bhaemaphysalis\b", r"\bixodes\b"]
}

LOCATION_PATTERNS = [
    "India", "Kerala", "Tamil Nadu", "Karnataka", "Maharashtra", "Gujarat",
    "Delhi", "West Bengal", "Uttar Pradesh", "Assam", "Punjab", "Rajasthan",
    "China", "Egypt", "Indonesia", "Vietnam", "Bangladesh", "Pakistan",
    "Nepal", "Thailand", "Brazil", "United States", "USA", "Saudi Arabia",
    "Democratic Republic of the Congo", "Nigeria", "United Kingdom", "France", "Germany"
]

date_regex = re.compile(r"\b(19\d\d|20\d\d)\b")

node_lookup = {}
nodes = []
relationships = []
provenance_records = []
next_node_id = 1

def get_or_create_node(name, entity_type, source):
    global next_node_id
    name = str(name).strip()
    if not name or len(name) < 2:
        return None
    key = (name.lower(), entity_type)
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

def match_lexicon(text, lexicon):
    matched = set()
    for canonical, patterns in lexicon.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                matched.add(canonical)
                break
    return matched

def split_into_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", str(text)) if len(s.strip()) > 10]

print("Executing upgraded extraction with exact word boundaries and sentence provenance...")
for idx, row in df.iterrows():
    if (idx + 1) % 1000 == 0 or idx == len(df) - 1:
        print(f"  Processed {idx + 1}/{len(df)} documents...")

    document_id = str(row.get("document_id", f"DOC_{idx+1}"))
    source = str(row.get("source", "Unknown"))
    doc_date = str(row.get("date", ""))
    text = str(row.get("clean_text", ""))
    if not text or text == "nan":
        continue

    document_node = get_or_create_node(document_id, "Document", source)
    sentences = split_into_sentences(text)

    # Document-level locations & dates
    doc_locations = set()
    doc_dates = set()

    if nlp is not None:
        doc_spacy = nlp(text[:8000])
        for ent in doc_spacy.ents:
            if ent.label_ == "GPE" and len(ent.text) > 2:
                doc_locations.add(ent.text.strip())
            elif ent.label_ == "DATE":
                doc_dates.add(ent.text.strip())
    else:
        for loc in LOCATION_PATTERNS:
            if re.search(r"\b" + re.escape(loc) + r"\b", text, re.IGNORECASE):
                doc_locations.add(loc)
        for dm in date_regex.finditer(text):
            doc_dates.add(dm.group(1))

    for loc in doc_locations:
        loc_node = get_or_create_node(loc, "Location", source)
        if loc_node:
            relationships.append({"source": document_node, "target": loc_node, "relationship": "MENTIONS_LOCATION"})

    for dt in doc_dates:
        dt_node = get_or_create_node(dt, "Date", source)
        if dt_node:
            relationships.append({"source": document_node, "target": dt_node, "relationship": "HAS_DATE"})

    # Document-level Disease, Pathogen, Animal matching
    doc_diseases = match_lexicon(text, DISEASE_LEXICON)
    doc_pathogens = match_lexicon(text, PATHOGEN_LEXICON)
    doc_animals = match_lexicon(text, ANIMAL_LEXICON)

    for dis in doc_diseases:
        dis_node = get_or_create_node(dis, "Disease", source)
        if dis_node:
            relationships.append({"source": document_node, "target": dis_node, "relationship": "MENTIONS_DISEASE"})

    for pat in doc_pathogens:
        pat_node = get_or_create_node(pat, "Pathogen", source)
        if pat_node:
            relationships.append({"source": document_node, "target": pat_node, "relationship": "MENTIONS_PATHOGEN"})

    for ani in doc_animals:
        ani_node = get_or_create_node(ani, "Animal", source)
        if ani_node:
            relationships.append({"source": document_node, "target": ani_node, "relationship": "MENTIONS_ANIMAL"})

    # Sentence-level cross-domain relations and evidence capture
    for sentence in sentences:
        s_diseases = match_lexicon(sentence, DISEASE_LEXICON)
        s_pathogens = match_lexicon(sentence, PATHOGEN_LEXICON)
        s_animals = match_lexicon(sentence, ANIMAL_LEXICON)
        s_locations = [loc for loc in LOCATION_PATTERNS if re.search(r"\b" + re.escape(loc) + r"\b", sentence, re.IGNORECASE)]

        # Record provenance
        for d in s_diseases:
            provenance_records.append({"document_id": document_id, "entity": d, "type": "Disease", "sentence": sentence[:300], "source": source})
        for p in s_pathogens:
            provenance_records.append({"document_id": document_id, "entity": p, "type": "Pathogen", "sentence": sentence[:300], "source": source})
        for a in s_animals:
            provenance_records.append({"document_id": document_id, "entity": a, "type": "Animal", "sentence": sentence[:300], "source": source})
        for l in s_locations:
            provenance_records.append({"document_id": document_id, "entity": l, "type": "Location", "sentence": sentence[:300], "source": source})

        # Cross-domain semantic edges
        for d in s_diseases:
            d_node = get_or_create_node(d, "Disease", source)
            for p in s_pathogens:
                p_node = get_or_create_node(p, "Pathogen", source)
                if d_node and p_node:
                    relationships.append({"source": p_node, "target": d_node, "relationship": "CAUSES_DISEASE"})
            for a in s_animals:
                a_node = get_or_create_node(a, "Animal", source)
                if a_node and d_node:
                    relationships.append({"source": a_node, "target": d_node, "relationship": "ASSOCIATED_WITH"})
            for l in s_locations:
                l_node = get_or_create_node(l, "Location", source)
                if d_node and l_node:
                    relationships.append({"source": d_node, "target": l_node, "relationship": "REPORTED_IN"})

        for a in s_animals:
            a_node = get_or_create_node(a, "Animal", source)
            for p in s_pathogens:
                p_node = get_or_create_node(p, "Pathogen", source)
                if a_node and p_node:
                    relationships.append({"source": a_node, "target": p_node, "relationship": "HOST_RESERVOIR_OF"})

nodes_df = pd.DataFrame(nodes)
relationships_df = pd.DataFrame(relationships).drop_duplicates()
provenance_df = pd.DataFrame(provenance_records).drop_duplicates()

nodes_file = os.path.join(output_dir, "nodes.csv")
relationships_file = os.path.join(output_dir, "relationships.csv")
provenance_file = os.path.join(output_dir, "entity_provenance.csv")

nodes_df.to_csv(nodes_file, index=False)
relationships_df.to_csv(relationships_file, index=False)
provenance_df.to_csv(provenance_file, index=False)

print("\n" + "=" * 45)
print("UPGRADED NLP EXTRACTION COMPLETE")
print("=" * 45)
print(f"Total Nodes: {len(nodes_df)}")
print(f"Total Relationships: {len(relationships_df)}")
print(f"Total Sentence Provenance Records: {len(provenance_df)}")
print("\nRelationship breakdown:")
print(relationships_df["relationship"].value_counts())
