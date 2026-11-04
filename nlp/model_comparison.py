"""
OneHealth Nexus — Comparative NLP Model Evaluation (Pipeline A vs Pipeline B)
Evaluates Existing NLP Model against fine-tuned PubMedBERT on identical held-out test split.
Generates Precision, Recall, F1, Latency, Confusion Matrix, and Error Analysis.
"""
import os
import sys
import json
import time
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix

from nlp.entity_extraction import DISEASE_LEXICON, PATHOGEN_LEXICON, ANIMAL_LEXICON, LOCATION_PATTERNS
from nlp.pubmedbert_ner import PubMedBERTNER, LABELS, LABEL2ID, ID2LABEL

DATASET_PATH = "data/evaluation/biomedical_ner_dataset.json"
RESULTS_PATH = "data/evaluation/model_comparison_results.json"
PLOT_PATH = "analysis/model_comparison_metrics.png"

def evaluate_pipeline_a(tokens):
    """Pipeline A: Word-boundary dictionary matching & regex patterns"""
    sentence = " ".join(tokens)
    pred_tags = ["O"] * len(tokens)

    def tag_matches(lexicon, label_prefix):
        for canonical, patterns in lexicon.items():
            for pat in patterns:
                for m in re.finditer(pat, sentence, re.IGNORECASE):
                    start_char = m.start()
                    end_char = m.end()
                    # map char span back to token index
                    char_cursor = 0
                    matched_indices = []
                    for t_idx, t in enumerate(tokens):
                        t_start = char_cursor
                        t_end = t_start + len(t)
                        char_cursor = t_end + 1  # space
                        if t_start >= start_char and t_end <= end_char:
                            matched_indices.append(t_idx)
                        elif t_start < end_char and t_end > start_char:
                            matched_indices.append(t_idx)
                    for i, idx in enumerate(matched_indices):
                        if 0 <= idx < len(pred_tags) and pred_tags[idx] == "O":
                            pred_tags[idx] = f"B-{label_prefix}" if i == 0 else f"I-{label_prefix}"

    tag_matches(DISEASE_LEXICON, "DISEASE")
    tag_matches(PATHOGEN_LEXICON, "PATHOGEN")
    tag_matches(ANIMAL_LEXICON, "ANIMAL")

    # Locations
    for loc in LOCATION_PATTERNS:
        for m in re.finditer(r"\b" + re.escape(loc) + r"\b", sentence, re.IGNORECASE):
            char_cursor = 0
            matched_indices = []
            for t_idx, t in enumerate(tokens):
                t_start = char_cursor
                t_end = t_start + len(t)
                char_cursor = t_end + 1
                if t_start < m.end() and t_end > m.start():
                    matched_indices.append(t_idx)
            for i, idx in enumerate(matched_indices):
                if 0 <= idx < len(pred_tags) and pred_tags[idx] == "O":
                    pred_tags[idx] = "B-LOCATION" if i == 0 else "I-LOCATION"

    # Dates
    for m in re.finditer(r"\b(19\d\d|20\d\d)\b", sentence):
        char_cursor = 0
        matched_indices = []
        for t_idx, t in enumerate(tokens):
            t_start = char_cursor
            t_end = t_start + len(t)
            char_cursor = t_end + 1
            if t_start < m.end() and t_end > m.start():
                matched_indices.append(t_idx)
        for i, idx in enumerate(matched_indices):
            if 0 <= idx < len(pred_tags) and pred_tags[idx] == "O":
                pred_tags[idx] = "B-DATE" if i == 0 else "I-DATE"

    return pred_tags

def evaluate_pipeline_b(tokens, pubmedbert_model):
    """Pipeline B: Fine-tuned PubMedBERT token classifier"""
    tokenizer = pubmedbert_model.tokenizer
    model = pubmedbert_model.model

    tokenized = tokenizer(
        tokens,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )
    with __import__("torch").no_grad():
        outputs = model(
            input_ids=tokenized["input_ids"],
            attention_mask=tokenized["attention_mask"]
        )
    preds = __import__("torch").argmax(outputs.logits.squeeze(0), dim=-1).tolist()
    word_ids = tokenized.word_ids(batch_index=0)

    pred_tags = ["O"] * len(tokens)
    seen_words = set()
    for p_id, w_idx in zip(preds, word_ids):
        if w_idx is not None and w_idx < len(pred_tags) and w_idx not in seen_words:
            seen_words.add(w_idx)
            pred_tags[w_idx] = ID2LABEL.get(p_id, "O")

    return pred_tags

def run_comparative_evaluation():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    test_set = data["test"]
    print(f"Loaded held-out test set: {len(test_set)} examples.")

    pubmedbert = PubMedBERTNER()

    gold_flat = []
    pipe_a_flat = []
    pipe_b_flat = []

    pipe_a_times = []
    pipe_b_times = []

    error_analysis = []

    for ex_idx, ex in enumerate(test_set):
        tokens = ex["tokens"]
        gold = ex["ner_tags"]

        # Pipeline A
        t0 = time.perf_counter()
        pred_a = evaluate_pipeline_a(tokens)
        t_a = (time.perf_counter() - t0) * 1000.0
        pipe_a_times.append(t_a)

        # Pipeline B
        t0 = time.perf_counter()
        pred_b = evaluate_pipeline_b(tokens, pubmedbert)
        t_b = (time.perf_counter() - t0) * 1000.0
        pipe_b_times.append(t_b)

        gold_flat.extend(gold)
        pipe_a_flat.extend(pred_a)
        pipe_b_flat.extend(pred_b)

        error_analysis.append({
            "sentence": " ".join(tokens),
            "gold": gold,
            "pipeline_a": pred_a,
            "pipeline_b": pred_b
        })

    # Overall Metrics
    cats = ["DISEASE", "ANIMAL", "PATHOGEN", "LOCATION", "DATE"]

    def compute_metrics(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)

        # Entity-level category metrics
        per_cat = {}
        for c in cats:
            bin_true = [1 if c in tag else 0 for tag in y_true]
            bin_pred = [1 if c in tag else 0 for tag in y_pred]
            cp, cr, cf1, _ = precision_recall_fscore_support(bin_true, bin_pred, average="binary", zero_division=0)
            per_cat[c] = {"precision": round(cp, 4), "recall": round(cr, 4), "f1": round(cf1, 4)}

        return {
            "accuracy": round(acc, 4),
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1": round(f1, 4),
            "per_category": per_cat
        }

    metrics_a = compute_metrics(gold_flat, pipe_a_flat)
    metrics_a["avg_latency_ms"] = round(float(np.mean(pipe_a_times)), 2)

    metrics_b = compute_metrics(gold_flat, pipe_b_flat)
    metrics_b["avg_latency_ms"] = round(float(np.mean(pipe_b_times)), 2)

    # Confusion matrices
    cm_labels = ["O", "DISEASE", "ANIMAL", "PATHOGEN", "LOCATION", "DATE"]
    def simplify_tags(tag_list):
        return [t.replace("B-", "").replace("I-", "") for t in tag_list]

    sim_gold = simplify_tags(gold_flat)
    sim_a = simplify_tags(pipe_a_flat)
    sim_b = simplify_tags(pipe_b_flat)

    cm_a = confusion_matrix(sim_gold, sim_a, labels=cm_labels).tolist()
    cm_b = confusion_matrix(sim_gold, sim_b, labels=cm_labels).tolist()

    results = {
        "evaluation_dataset": {
            "total_test_sentences": len(test_set),
            "total_test_tokens": len(gold_flat)
        },
        "pipeline_a_existing_nlp": metrics_a,
        "pipeline_b_pubmedbert": metrics_b,
        "confusion_matrix_labels": cm_labels,
        "confusion_matrix_pipeline_a": cm_a,
        "confusion_matrix_pipeline_b": cm_b,
        "error_analysis_samples": error_analysis[:4]
    }

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 55)
    print("COMPARATIVE EVALUATION RESULTS (HELD-OUT TEST SET)")
    print("=" * 55)
    print(f"{'Metric':<25} | {'Pipeline A (Existing)':<20} | {'Pipeline B (PubMedBERT)':<20}")
    print("-" * 70)
    print(f"{'Accuracy':<25} | {metrics_a['accuracy']:<20} | {metrics_b['accuracy']:<20}")
    print(f"{'Weighted Precision':<25} | {metrics_a['precision']:<20} | {metrics_b['precision']:<20}")
    print(f"{'Weighted Recall':<25} | {metrics_a['recall']:<20} | {metrics_b['recall']:<20}")
    print(f"{'Weighted F1-score':<25} | {metrics_a['f1']:<20} | {metrics_b['f1']:<20}")
    print(f"{'Inference Latency (ms)':<25} | {metrics_a['avg_latency_ms']:<20} | {metrics_b['avg_latency_ms']:<20}")
    print("-" * 70)
    for c in cats:
        f1_a = metrics_a["per_category"][c]["f1"]
        f1_b = metrics_b["per_category"][c]["f1"]
        print(f"{c + ' F1-score':<25} | {f1_a:<20} | {f1_b:<20}")
    print("=" * 55)

    # Plot comparison chart
    os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Overall metrics plot
    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
    vals_a = [metrics_a["accuracy"], metrics_a["precision"], metrics_a["recall"], metrics_a["f1"]]
    vals_b = [metrics_b["accuracy"], metrics_b["precision"], metrics_b["recall"], metrics_b["f1"]]

    x = np.arange(len(metrics_names))
    width = 0.35

    axes[0].bar(x - width/2, vals_a, width, label="Pipeline A (Existing NLP)", color="#3b82f6")
    axes[0].bar(x + width/2, vals_b, width, label="Pipeline B (PubMedBERT)", color="#10b981")
    axes[0].set_ylabel("Score (0.0 - 1.0)")
    axes[0].set_title("Overall NER Performance on Test Set")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(metrics_names)
    axes[0].set_ylim(0, 1.05)
    axes[0].legend()
    axes[0].grid(axis="y", linestyle="--", alpha=0.6)

    # Per-category F1 plot
    f1_cats_a = [metrics_a["per_category"][c]["f1"] for c in cats]
    f1_cats_b = [metrics_b["per_category"][c]["f1"] for c in cats]

    x2 = np.arange(len(cats))
    axes[1].bar(x2 - width/2, f1_cats_a, width, label="Pipeline A", color="#3b82f6")
    axes[1].bar(x2 + width/2, f1_cats_b, width, label="Pipeline B (PubMedBERT)", color="#10b981")
    axes[1].set_ylabel("F1-Score")
    axes[1].set_title("Per-Category F1-Score Comparison")
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(cats, rotation=15)
    axes[1].set_ylim(0, 1.05)
    axes[1].legend()
    axes[1].grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=200)
    plt.close()
    print(f"Comparison chart saved to {PLOT_PATH}")

    return results

if __name__ == "__main__":
    run_comparative_evaluation()

