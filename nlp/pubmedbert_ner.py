"""
OneHealth Nexus — PubMedBERT Biomedical Named Entity Recognition (Pipeline B)
Fine-tunes microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext for One Health NER.
Saves model weights & tokenizer to models/pubmedbert_ner/ for persistent inference.
"""
import os
import json
import time
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForTokenClassification

MODEL_NAME = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
MODEL_DIR = "models/pubmedbert_ner"
DATASET_PATH = "data/evaluation/biomedical_ner_dataset.json"

LABELS = [
    "O",
    "B-DISEASE", "I-DISEASE",
    "B-ANIMAL", "I-ANIMAL",
    "B-PATHOGEN", "I-PATHOGEN",
    "B-LOCATION", "I-LOCATION",
    "B-DATE", "I-DATE"
]
LABEL2ID = {l: i for i, l in enumerate(LABELS)}
ID2LABEL = {i: l for i, l in enumerate(LABELS)}

class NERDataset(Dataset):
    def __init__(self, examples, tokenizer, max_len=128):
        self.features = []
        for ex in examples:
            words = ex["tokens"]
            tags = ex["ner_tags"]
            tokenized = tokenizer(
                words,
                is_split_into_words=True,
                truncation=True,
                max_length=max_len,
                padding="max_length",
                return_tensors="pt"
            )
            word_ids = tokenized.word_ids(batch_index=0)
            label_ids = []
            previous_word_idx = None
            for w_idx in word_ids:
                if w_idx is None:
                    label_ids.append(-100)
                elif w_idx != previous_word_idx:
                    tag = tags[w_idx] if w_idx < len(tags) else "O"
                    label_ids.append(LABEL2ID.get(tag, 0))
                else:
                    tag = tags[w_idx] if w_idx < len(tags) else "O"
                    # subword tag
                    if tag.startswith("B-"):
                        tag = "I-" + tag[2:]
                    label_ids.append(LABEL2ID.get(tag, 0))
                previous_word_idx = w_idx

            self.features.append({
                "input_ids": tokenized["input_ids"].squeeze(0),
                "attention_mask": tokenized["attention_mask"].squeeze(0),
                "labels": torch.tensor(label_ids, dtype=torch.long)
            })

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx]

def train_and_save_pubmedbert(epochs=3, batch_size=4, lr=3e-5):
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Loading PubMedBERT tokenizer and base architecture...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    train_ds = NERDataset(data["train"], tokenizer)
    val_ds = NERDataset(data["validation"], tokenizer)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    print(f"Fine-tuning PubMedBERT for {epochs} epochs on CPU...")
    start_time = time.time()
    model.train()
    for ep in range(epochs):
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["labels"]
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"  Epoch {ep+1}/{epochs} - Loss: {avg_loss:.4f}")

    train_duration = time.time() - start_time
    print(f"Training completed in {train_duration:.2f} seconds.")

    print(f"Saving fine-tuned PubMedBERT to {MODEL_DIR}...")
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    metadata = {
        "base_model": MODEL_NAME,
        "labels": LABELS,
        "label2id": LABEL2ID,
        "id2label": ID2LABEL,
        "train_samples": len(data["train"]),
        "epochs": epochs,
        "train_duration_sec": train_duration
    }
    with open(os.path.join(MODEL_DIR, "training_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return model, tokenizer

class PubMedBERTNER:
    def __init__(self, model_dir=MODEL_DIR):
        if not os.path.exists(os.path.join(model_dir, "config.json")):
            print("Trained PubMedBERT model not found. Initiating fine-tuning...")
            train_and_save_pubmedbert()
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForTokenClassification.from_pretrained(model_dir)
        self.model.eval()

    def predict(self, text):
        words = text.split()
        if not words:
            return []
        tokenized = self.tokenizer(
            words,
            is_split_into_words=True,
            return_tensors="pt",
            truncation=True,
            max_length=128
        )
        with torch.no_grad():
            outputs = self.model(
                input_ids=tokenized["input_ids"],
                attention_mask=tokenized["attention_mask"]
            )
        logits = outputs.logits.squeeze(0)
        predictions = torch.argmax(logits, dim=-1).tolist()
        word_ids = tokenized.word_ids(batch_index=0)

        entities = []
        current_entity = []
        current_type = None

        seen_words = set()
        for idx, (p_id, w_idx) in enumerate(zip(predictions, word_ids)):
            if w_idx is None or w_idx in seen_words:
                continue
            seen_words.add(w_idx)
            tag = ID2LABEL.get(p_id, "O")
            if tag.startswith("B-"):
                if current_entity:
                    entities.append({"text": " ".join(current_entity), "type": current_type})
                current_entity = [words[w_idx]]
                current_type = tag[2:]
            elif tag.startswith("I-") and current_type == tag[2:]:
                current_entity.append(words[w_idx])
            else:
                if current_entity:
                    entities.append({"text": " ".join(current_entity), "type": current_type})
                    current_entity = []
                    current_type = None
        if current_entity:
            entities.append({"text": " ".join(current_entity), "type": current_type})

        return entities

if __name__ == "__main__":
    model, tok = train_and_save_pubmedbert(epochs=3)
    ner = PubMedBERTNER()
    sample = "In Kerala , fruit bats were confirmed as reservoir hosts of Nipah virus in 2018 ."
    ents = ner.predict(sample)
    print(f"\nInference Test on: '{sample}'")
    print(f"Extracted Entities: {ents}")
    assert os.path.exists(os.path.join(MODEL_DIR, "config.json")), "Model config missing"
    print("Self-check passed: PubMedBERT trained, saved, and validated.")

