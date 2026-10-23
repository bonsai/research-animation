#!/usr/bin/env python3
"""Minimal citation-first lexical retrieval over knowledge.jsonl (stdlib only)."""
from __future__ import annotations
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN_RE = re.compile(r"[a-zA-Z0-9]+|[ぁ-んァ-ヶ一-龯ー]+", re.UNICODE)
STOP = {"the", "and", "for", "with", "from", "that", "this", "are", "was", "into", "how", "what", "does", "about", "研究", "論文", "について"}

def tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text) if t.lower() not in STOP and len(t) > 1]

def load_chunks(path: Path) -> list[dict]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            for key in ("chunk_id", "source_id", "text", "url"):
                if key not in row:
                    raise ValueError(f"missing {key}")
            rows.append(row)
        except Exception as exc:
            raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {exc}")
    return rows

def retrieve(query: str, chunks: list[dict], top_k: int) -> list[tuple[float, dict]]:
    q = Counter(tokens(query))
    docs = []
    df = Counter()
    for row in chunks:
        body = " ".join([row.get("title", ""), row.get("text", ""), " ".join(row.get("topics", []))])
        tf = Counter(tokens(body))
        docs.append((row, tf, body.lower()))
        df.update(set(tf))
    n = max(1, len(docs))
    ranked = []
    for row, tf, body in docs:
        score = 0.0
        for term, qcount in q.items():
            if tf[term]:
                idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
                score += idf * (tf[term] * 2.2) / (tf[term] + 1.2) * min(qcount, 2)
        if query.lower() in body:
            score += 1.0
        if score > 0:
            ranked.append((score, row))
    return sorted(ranked, key=lambda x: x[0], reverse=True)[:top_k]

def main() -> None:
    ap = argparse.ArgumentParser(description="Search cited Skeleton Dance research notes.")
    ap.add_argument("query", help="Research question or keywords")
    ap.add_argument("--top-k", type=int, default=4)
    args = ap.parse_args()
    if args.top_k < 1:
        ap.error("--top-k must be >= 1")
    chunks = load_chunks(HERE / "knowledge.jsonl")
    hits = retrieve(args.query, chunks, args.top_k)
    print(f"Query: {args.query}\nRetrieved: {len(hits)} chunk(s)\n")
    if not hits:
        print("No matching notes. Try English keywords such as music, pose, rhythm, skeleton, segmentation.")
        return
    for rank, (score, row) in enumerate(hits, 1):
        print(f"[{rank}] {row.get('title', row['chunk_id'])}")
        print(f"    score={score:.3f} | source={row['source_id']} | chunk={row['chunk_id']} | year={row.get('year', 'n/a')}")
        print(f"    {row['text']}")
        print(f"    Evidence type: {row.get('evidence_type', 'unspecified')}")
        print(f"    Source: {row['url']}\n")
    print("Note: lexical relevance scores are ranking signals, not confidence. Verify claims against the cited source.")

if __name__ == "__main__":
    main()
