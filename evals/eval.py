# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
from typing import Dict, List

from conllu import Token, parse_incr

Sentence = List[Token]


def read_conllu(path: str) -> List[Sentence]:
    sentences: List[Sentence] = []
    with open(path, "r") as f:
        for tokenlist in parse_incr(f):
            tokens: Sentence = [t for t in tokenlist if isinstance(t["id"], int)]
            tokens.sort(key=lambda t: t["id"])
            sentences.append(tokens)
    return sentences


def accuracy(
    gold: List[Sentence], pred: List[Sentence], field: str, skip_punct: bool = False
) -> float:
    correct = 0
    total = 0
    for g_sent, p_sent in zip(gold, pred):
        for g_tok, p_tok in zip(g_sent, p_sent):
            if skip_punct and g_tok.get("upos") == "PUNCT":
                continue
            if g_tok.get(field) == p_tok.get(field):
                correct += 1
            total += 1
    return correct / total if total > 0 else 0.0


def feats_accuracy(
    gold: List[Sentence], pred: List[Sentence], skip_punct: bool = False
) -> float:
    correct = 0
    total = 0
    for g_sent, p_sent in zip(gold, pred):
        for g_tok, p_tok in zip(g_sent, p_sent):
            if skip_punct and g_tok.get("upos") == "PUNCT":
                continue
            g_feats = g_tok.get("feats") or {}
            p_feats = p_tok.get("feats") or {}
            if g_feats == p_feats:
                correct += 1
            total += 1
    return correct / total if total > 0 else 0.0


def head_accuracy(
    gold: List[Sentence],
    pred: List[Sentence],
    skip_punct: bool = False,
    labeled: bool = False,
) -> float:
    correct = 0
    total = 0
    for g_sent, p_sent in zip(gold, pred):
        for g_tok, p_tok in zip(g_sent, p_sent):
            if skip_punct and g_tok.get("upos") == "PUNCT":
                continue
            if g_tok.get("head") == p_tok.get("head"):
                if labeled:
                    if g_tok.get("deprel") == p_tok.get("deprel"):
                        correct += 1
                else:
                    correct += 1
            total += 1
    return correct / total if total > 0 else 0.0


def proportion_with_cycles(sentences: List[Sentence]) -> float:
    cycle_count = 0
    for sent in sentences:
        has_cycle = False
        for tok in sent:
            visited: set[int] = set()
            current: Token = tok
            while current["head"] != 0:
                if current["head"] in visited:
                    has_cycle = True
                    break
                visited.add(current["id"])
                head_idx = current["head"] - 1
                if head_idx < 0 or head_idx >= len(sent):
                    break
                current = sent[head_idx]
            if has_cycle:
                break
        if has_cycle:
            cycle_count += 1
    return cycle_count / len(sentences) if sentences else 0.0


def proportion_with_multiple_roots(sentences: List[Sentence]) -> float:
    multi_root_count = 0
    for sent in sentences:
        root_count = sum(1 for tok in sent if tok["head"] == 0)
        if root_count > 1:
            multi_root_count += 1
    return multi_root_count / len(sentences) if sentences else 0.0


def evaluate(gold_path: str, pred_path: str) -> Dict[str, float]:
    gold = read_conllu(gold_path)
    pred = read_conllu(pred_path)

    return {
        "LEMMA": accuracy(gold, pred, "lemma", skip_punct=True),
        "UPOS": accuracy(gold, pred, "upos"),
        "DEPREL": accuracy(gold, pred, "deprel"),
        "FEATS": feats_accuracy(gold, pred),
        "UAS": head_accuracy(gold, pred, labeled=False),
        "LAS": head_accuracy(gold, pred, labeled=True),
        "CYCLE_PROP": proportion_with_cycles(pred),
        "MULTIROOT_PROP": proportion_with_multiple_roots(pred),
    }


def main() -> None:
    gold_file = sys.argv[1]
    pred_file = sys.argv[2]

    results = evaluate(gold_file, pred_file)

    print("Metric            | Accuracy / Proportion")
    print("------------------+--------------------")
    for k, v in results.items():
        print(f"{k:18} | {v*100:6.2f}")


if __name__ == "__main__":
    main()
