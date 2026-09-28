from pathlib import Path
import re
import pandas as pd
from dateutil import parser as date_parser

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT = ROOT / "knowledge_graph"
OUT.mkdir(parents=True, exist_ok=True)

DOC_PATH = DATA / "spark_output" / "processed_documents.txt"
if not DOC_PATH.exists():
    DOC_PATH = DATA / "cleaned_documents.csv"

GBIF_PATH = DATA / "cleaned_gbif.csv"

def read_spark_csv(path: Path) -> pd.DataFrame:
    if path.is_file():
        sep = "\t" if path.suffix == ".txt" else ","
        return pd.read_csv(path, sep=sep, dtype=str).fillna("")
    if path.is_dir():
        parts = sorted(path.glob("part-*.csv"))
        if not parts:
            parts = sorted(path.glob("*.txt"))
        if not parts:
            raise FileNotFoundError(f"No Spark data files found in {path}")
        return pd.concat(
            [pd.read_csv(p, sep="\t" if p.suffix == ".txt" else ",", dtype=str).fillna("") for p in parts],
            ignore_index=True
        )
    raise FileNotFoundError(f"Missing: {path}")

def normalize(s: str) -> str:
    s = "" if pd.isna(s) else str(s)
    s = re.sub(r"\s+", " ", s.strip().lower())
    return s

def split_sentences(text: str):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]

def find_entities(text: str):
    t = str(text)
    entities = []

    disease_patterns = [
        r"\bavian influenza\b", r"\binfluenza\b", r"\bcovid[- ]?19\b",
        r"\bcoronavirus\b", r"\bmers\b", r"\bhiv\b", r"\btuberculosis\b",
        r"\bdengue\b", r"\bmalaria\b", r"\bcholera\b", r"\bmpox\b",
        r"\bmonkeypox\b", r"\bebola\b", r"\brabies\b", r"\bzoonotic disease\b"
    ]
    pathogen_patterns = [
        r"\b(?:influenza|coronavirus|mers|sars[- ]?cov[- ]?2|h5n1|h7n9|ebola)\b"
    ]
    animal_patterns = [
        r"\bbat(?:s)?\b", r"\bpoultry\b", r"\bchicken(?:s)?\b",
        r"\bbird(?:s)?\b", r"\bcattle\b", r"\bcow(?:s)?\b",
        r"\bpig(?:s)?\b", r"\bswine\b", r"\bdog(?:s)?\b",
        r"\bcat(?:s)?\b", r"\bcamel(?:s)?\b", r"\bhorse(?:s)?\b",
        r"\bmonkey(?:s)?\b", r"\bprimate(?:s)?\b", r"\blivestock\b"
    ]
    location_patterns = [
        r"\b(?:India|China|Pakistan|Egypt|Saudi Arabia|United States|USA|Brazil|Bangladesh|Nepal|Thailand|Indonesia|Vietnam|France|Germany|Italy|Spain|United Kingdom|UK)\b"
    ]

    groups = [
        ("Disease", disease_patterns),
        ("Pathogen", pathogen_patterns),
        ("Animal", animal_patterns),
        ("Location", location_patterns),
    ]

    seen = set()
    for label, patterns in groups:
        for pattern in patterns:
            for m in re.finditer(pattern, t, flags=re.I):
                value = m.group(0).strip()
                key = (label, normalize(value))
                if key not in seen:
                    seen.add(key)
                    entities.append({
                        "entity": value,
                        "entity_type": label,
                        "start": m.start(),
                        "end": m.end()
                    })
    return entities

def extract_dates(text: str):
    t = str(text)
    found = []
    patterns = [
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    ]
    for p in patterns:
        found.extend(m.group(0) for m in re.finditer(p, t, flags=re.I))
    return list(dict.fromkeys(found))

def infer_relations(entities, sentence):
    rels = []
    low = sentence.lower()
    for a in entities:
        for b in entities:
            if a is b:
                continue
            pair = (a["entity"], b["entity"])
            if a["entity_type"] == "Animal" and b["entity_type"] in {"Disease", "Pathogen"}:
                if re.search(r"\b(infected|infection|host|reservoir|exposure|transmission|virus|disease|cases?)\b", low):
                    rels.append((a, b, "ASSOCIATED_WITH"))
            elif a["entity_type"] == "Disease" and b["entity_type"] == "Location":
                if re.search(r"\b(cases?|outbreak|reported|detected|occurred|in|from|among)\b", low):
                    rels.append((a, b, "REPORTED_IN"))
            elif a["entity_type"] == "Pathogen" and b["entity_type"] == "Animal":
                if re.search(r"\b(host|infected|infection|detected|found|virus)\b", low):
                    rels.append((a, b, "FOUND_IN"))
            elif a["entity_type"] == "Pathogen" and b["entity_type"] == "Location":
                if re.search(r"\b(detected|reported|identified|outbreak|cases?|in)\b", low):
                    rels.append((a, b, "DETECTED_IN"))
    # deduplicate
    unique = []
    seen = set()
    for a, b, r in rels:
        k = (normalize(a["entity"]), normalize(b["entity"]), r)
        if k not in seen:
            seen.add(k)
            unique.append((a, b, r))
    return unique

def main():
    docs = read_spark_csv(DOC_PATH)
    gbif = read_spark_csv(GBIF_PATH)

    docs["text"] = docs.get("clean_text", docs.get("text", "")).fillna("")
    docs["document_id"] = docs["document_id"].astype(str)

    entity_rows = []
    relation_rows = []
    temporal_rows = []

    for _, row in docs.iterrows():
        doc_id = row["document_id"]
        text = str(row["text"])
        doc_date = str(row.get("date", ""))

        for ent in find_entities(text):
            entity_rows.append({
                "document_id": doc_id,
                "entity": ent["entity"],
                "entity_normalized": normalize(ent["entity"]),
                "entity_type": ent["entity_type"],
                "date": doc_date,
                "source": str(row.get("source", "")),
            })

        for sent in split_sentences(text):
            ents = find_entities(sent)
            for a, b, rel in infer_relations(ents, sent):
                relation_rows.append({
                    "document_id": doc_id,
                    "source_entity": a["entity"],
                    "source_type": a["entity_type"],
                    "relation": rel,
                    "target_entity": b["entity"],
                    "target_type": b["entity_type"],
                    "evidence": sent[:1000],
                    "date": doc_date,
                    "source": str(row.get("source", "")),
                })

        dates = extract_dates(text)
        for d in dates:
            temporal_rows.append({
                "document_id": doc_id,
                "date_mention": d,
                "document_date": doc_date,
                "source": str(row.get("source", "")),
            })

    entities_df = pd.DataFrame(entity_rows).drop_duplicates()
    relations_df = pd.DataFrame(relation_rows).drop_duplicates()
    temporal_df = pd.DataFrame(temporal_rows).drop_duplicates()

    if entities_df.empty:
        entities_df = pd.DataFrame(columns=[
            "document_id","entity","entity_normalized","entity_type","date","source"
        ])
    if relations_df.empty:
        relations_df = pd.DataFrame(columns=[
            "document_id","source_entity","source_type","relation",
            "target_entity","target_type","evidence","date","source"
        ])
    if temporal_df.empty:
        temporal_df = pd.DataFrame(columns=[
            "document_id","date_mention","document_date","source"
        ])

    entities_df.to_csv(OUT / "entities.csv", index=False)
    relations_df.to_csv(OUT / "relations.csv", index=False)
    temporal_df.to_csv(OUT / "temporal_mentions.csv", index=False)

    gbif["species"] = gbif.get("species", "").fillna("")
    gbif["scientific_name"] = gbif.get("scientific_name", "").fillna("")
    gbif["state"] = gbif.get("state", "").fillna("")
    gbif["country"] = gbif.get("country", "").fillna("")

    gbif_entities = gbif[
        ["gbif_id","species","scientific_name","state","country","latitude","longitude","year","event_date"]
    ].copy()
    gbif_entities.to_csv(OUT / "gbif_entities.csv", index=False)

    print("=" * 55)
    print("ONEHEALTH NEXUS - NLP PIPELINE COMPLETE")
    print("=" * 55)
    print(f"Documents:          {len(docs)}")
    print(f"GBIF records:       {len(gbif)}")
    print(f"Entity mentions:    {len(entities_df)}")
    print(f"Relations:          {len(relations_df)}")
    print(f"Date mentions:      {len(temporal_df)}")
    print("\nCreated:")
    print("  knowledge_graph/entities.csv")
    print("  knowledge_graph/relations.csv")
    print("  knowledge_graph/temporal_mentions.csv")
    print("  knowledge_graph/gbif_entities.csv")

if __name__ == "__main__":
    main()
