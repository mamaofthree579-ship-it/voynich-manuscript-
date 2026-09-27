#!/usr/bin/env python3
"""
Voynich ZL3b transition-analysis pipeline
Author: Hope Jones
Purpose:
  Parse Zandbergen-Landini ZL3b IVTFF 2.0 while preserving folio/locus metadata,
  build terminal-state -> qo-initial transition tables, and run reproducible
  null-model tests.

Input:
  ZL3b-n.txt from https://www.voynich.nu/data/ZL3b-n.txt

Usage:
  python voynich_transition_pipeline.py ZL3b-n.txt --out results --permutations 20000

The script intentionally keeps:
  - raw text
  - cleaned token
  - uncertainty flag
  - folio
  - line/locus
  - Currier language
  - hand
  - paragraph/locus type

It does NOT claim semantic meanings for EVA strings.
"""

from __future__ import annotations
import argparse
import csv
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

FOLIO_RE = re.compile(r"^<([^>]+)>\s+(.*)$")
LOCUS_RE = re.compile(r"^<([^>]+)>\s+(.*)$")

def parse_header_meta(meta: str) -> dict:
    out = {}
    for k, v in re.findall(r"\$([A-Za-z]+)=([^\s>]+)", meta):
        out[k] = v
    return out

def clean_text(raw: str) -> tuple[str, bool]:
    """Deterministic primary reading: first alternative in [a:b]."""
    uncertain = False

    def alt(m):
        nonlocal uncertain
        uncertain = True
        return m.group(1)

    text = re.sub(r"\[([^:\]]+):[^\]]+\]", alt, raw)
    if "[" in raw or "]" in raw:
        uncertain = True

    # Remove brace comments/uncertain readings.
    def braces(m):
        nonlocal uncertain
        uncertain = True
        return ""

    text = re.sub(r"\{[^}]*\}", braces, text)

    # Remove non-text inline annotations and common markup.
    text = re.sub(r"<![^>]*>", "", text)
    text = re.sub(r"<->", " ", text)
    text = re.sub(r"@(?:\d+|[A-Za-z0-9_]+)", "", text)
    text = text.replace("<$>", " ")
    text = text.replace("<%>", " ")
    text = text.replace("$", " ")
    text = text.replace("%", " ")
    text = text.replace("=", " ")
    text = text.replace(",", ".")
    return text, uncertain

def token_class(token: str) -> dict:
    t = token.strip(". ")
    terminal_y = t.endswith("y")
    dy = t.endswith("dy")
    ly = t.endswith("ly")
    qo = t.startswith("qo")
    q = t.startswith("q")
    return {
        "token": t,
        "terminal_y": terminal_y,
        "dy": dy,
        "ly": ly,
        "qo": qo,
        "q_initial": q,
    }

def parse_zl3b(path: Path):
    records = []
    current = {
        "folio": None, "Q": None, "P": None, "F": None, "B": None,
        "I": None, "L": None, "H": None, "C": None, "X": None
    }

    for line_no, rawline in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = rawline.rstrip("\n")
        if not line or line.startswith("#"):
            continue

        m = FOLIO_RE.match(line)
        if not m:
            continue

        locus, payload = m.groups()

        # Folio header such as <f1r> <! $Q=A ...>
        if re.fullmatch(r"f\d+[rv](?:\.\d+)?", locus) and "." not in locus:
            meta = parse_header_meta(payload)
            if meta:
                current = {
                    "folio": locus,
                    "Q": meta.get("Q"),
                    "P": meta.get("P"),
                    "F": meta.get("F"),
                    "B": meta.get("B"),
                    "I": meta.get("I"),
                    "L": meta.get("L"),
                    "H": meta.get("H"),
                    "C": meta.get("C"),
                    "X": meta.get("X"),
                }
            continue

        # Text locus: f75r.12,+P0 etc.
        if "." not in locus:
            continue

        clean, uncertain = clean_text(payload)

        # Determine locus suffix, e.g. @P0, +P0, =Pt, @L0
        parts = locus.split(",", 1)
        page_line = parts[0]
        locus_type = parts[1] if len(parts) == 2 else ""

        words = [w for w in re.split(r"\s+|\.", clean) if w]
        for idx, word in enumerate(words):
            tc = token_class(word)
            records.append({
                "source_line": line_no,
                "folio": current["folio"],
                "locus": locus,
                "page_line": page_line,
                "locus_type": locus_type,
                "word_index": idx,
                "raw_word": word,
                "token": tc["token"],
                "uncertain": int(uncertain),
                "language": current["L"],
                "hand": current["H"],
                "section": current["I"],
                "quire": current["Q"],
                "paragraph": current["P"],
                **{k: int(v) for k, v in tc.items() if k != "token"},
            })

    return records

def adjacent_pairs(records, preserve_boundaries=True):
    """Pairs are within each folio/paragraph stream; never cross folio."""
    streams = defaultdict(list)
    for r in records:
        key = (r["folio"], r["P"] if preserve_boundaries else "ALL")
        streams[key].append(r)

    pairs = []
    for seq in streams.values():
        for a, b in zip(seq, seq[1:]):
            pairs.append((a, b))
    return pairs

def classify_transition(a, b):
    return {
        "terminal_y_to_qo": a["terminal_y"] and b["qo"],
        "dy_to_qo": a["dy"] and b["qo"],
        "other_terminal_y_to_qo": a["terminal_y"] and not a["dy"] and b["qo"],
        "ly_to_qo": a["ly"] and b["qo"],
        "q_to_o": a["q_initial"] and b["token"].startswith("o"),
    }

def observed_counts(records):
    pairs = adjacent_pairs(records, preserve_boundaries=True)
    total = len(pairs)
    out = Counter()
    denominators = Counter()

    for a, b in pairs:
        if a["terminal_y"]:
            denominators["terminal_y"] += 1
        if a["dy"]:
            denominators["dy"] += 1
        if a["terminal_y"] and not a["dy"]:
            denominators["other_terminal_y"] += 1
        if a["ly"]:
            denominators["ly"] += 1
        if a["q_initial"]:
            denominators["q_initial"] += 1
        if b["qo"]:
            denominators["qo_targets"] += 1

        for k, v in classify_transition(a, b).items():
            out[k] += int(v)

    return pairs, out, denominators, total

def shuffle_counts(records, rng, n_perm):
    """Unrestricted within-stream token shuffles; preserves stream lengths."""
    streams = defaultdict(list)
    for r in records:
        streams[(r["folio"], r["P"])].append(r)

    observed_features = []
    for _ in range(n_perm):
        total_counts = Counter()
        for seq in streams.values():
            # Shuffle only token identities; metadata remains attached to positions.
            flags = [(
                r["terminal_y"], r["dy"], r["ly"], r["q_initial"], r["qo"]
            ) for r in seq]
            rng.shuffle(flags)

            for a, b in zip(flags, flags[1:]):
                ay, ady, aly, aq, _ = a
                _, _, _, _, bqo = b
                total_counts["terminal_y_to_qo"] += int(ay and bqo)
                total_counts["dy_to_qo"] += int(ady and bqo)
                total_counts["ly_to_qo"] += int(aly and bqo)
        observed_features.append(total_counts)
    return observed_features

def summarize_null(observed, nulls):
    keys = sorted(observed.keys())
    rows = []
    for k in keys:
        vals = [x[k] for x in nulls]
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        sd = math.sqrt(var)
        z = (observed[k] - mean) / sd if sd else float("nan")
        p_upper = (1 + sum(x >= observed[k] for x in vals)) / (len(vals) + 1)
        rows.append({
            "feature": k,
            "observed": observed[k],
            "null_mean": mean,
            "null_sd": sd,
            "z": z,
            "p_upper": p_upper,
        })
    return rows

def transition_matrix(records):
    classes = ["qo", "q", "terminal_y_dy", "terminal_y_other", "ly", "other"]
    def cls(r):
        if r["qo"]: return "qo"
        if r["q_initial"]: return "q"
        if r["dy"]: return "terminal_y_dy"
        if r["terminal_y"]: return "terminal_y_other"
        if r["ly"]: return "ly"
        return "other"

    M = Counter()
    for a, b in adjacent_pairs(records, preserve_boundaries=True):
        M[(cls(a), cls(b))] += 1
    return classes, M

def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path, default=Path("voynich_transition_results"))
    ap.add_argument("--permutations", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20260927)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    records = parse_zl3b(args.input)

    # Full parsed token table.
    token_fields = [
        "source_line","folio","locus","page_line","locus_type","word_index",
        "raw_word","token","uncertain","language","hand","section","quire",
        "paragraph","terminal_y","dy","ly","qo","q_initial"
    ]
    write_csv(args.out / "tokens.csv", records, token_fields)

    pairs, obs, den, total = observed_counts(records)
    summary = [{
        "total_tokens": len(records),
        "within_stream_pairs": total,
        **{f"observed_{k}": v for k, v in obs.items()},
        **{f"denominator_{k}": v for k, v in den.items()},
    }]
    write_csv(args.out / "observed_summary.csv", summary, list(summary[0].keys()))

    rng = random.Random(args.seed)
    nulls = shuffle_counts(records, rng, args.permutations)
    null_summary = summarize_null(obs, nulls)
    write_csv(
        args.out / "null_summary.csv",
        null_summary,
        ["feature","observed","null_mean","null_sd","z","p_upper"]
    )

    classes, M = transition_matrix(records)
    matrix_rows = []
    for a in classes:
        row = {"from": a}
        for b in classes:
            row[b] = M[(a,b)]
        matrix_rows.append(row)
    write_csv(args.out / "transition_matrix.csv", matrix_rows, ["from"] + classes)

    # Machine-readable provenance.
    (args.out / "README.txt").write_text(
        f"""Voynich ZL3b transition analysis
Input: {args.input}
Random seed: {args.seed}
Permutations: {args.permutations}

Parser policy:
- ZL3b IVTFF 2.0
- first alternative retained for [a:b]
- uncertainty retained as a flag
- brace annotations removed from clean token
- word boundaries split on periods/whitespace
- transitions never cross folio or paragraph stream
- no semantic interpretation is applied

Important:
These outputs test structural transitions in the transcription.
They do not establish historical meanings or a decipherment.
""",
        encoding="utf-8"
    )

    print(f"Parsed tokens: {len(records):,}")
    print(f"Within-stream adjacent pairs: {total:,}")
    print("Observed:")
    for k, v in obs.items():
        print(f"  {k}: {v:,}")
    print(f"Results written to: {args.out.resolve()}")

if __name__ == "__main__":
    main()
