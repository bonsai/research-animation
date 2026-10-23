# Skeleton Dance Literature RAG

A small, source-grounded RAG prototype for research around Disney's *The Skeleton Dance* (1929), music–movement relationships, dance pose analysis, and animation studies.

## Scope

- Seed corpus is a curated set of bibliographic records and short research notes, not full-text copies of papers.
- Answers retrieve relevant JSONL chunks and show source IDs/URLs.
- Claims are limited to what the indexed notes support; retrieval is lexical and is **not** semantic embedding search.
- To improve coverage, add legally obtained full texts or abstracts with license/permission checks, then split them into small chunks while retaining page/section provenance.

## Files

- `sources.jsonl`: source metadata, DOI/URL, access notes.
- `knowledge.jsonl`: retrieval chunks; each record has a stable `chunk_id`, `source_id`, topic tags, text, and citation URL.
- `query.py`: dependency-free lexical retrieval CLI.

## Run

From this directory:

```bash
python query.py "How does music structure relate to movement?"
python query.py "dance pose temporal segmentation" --top-k 5
```

Python 3.10+; standard library only.

## Data contract

Each line in `knowledge.jsonl` is one JSON object:

```json
{"chunk_id":"sd-001-a","source_id":"sd-001","title":"...","year":2021,"topics":["music","movement"],"text":"Short paraphrased research note.","url":"https://doi.org/...","evidence_type":"abstract_summary"}
```

## Next iteration

1. Verify each source and retrieve permitted full text where available.
2. Add page/section offsets and exact quoted evidence only when legally permitted.
3. Add multilingual query expansion (Japanese/English), then embeddings/vector retrieval.
4. Evaluate with a small set of research questions and expected source IDs.
5. Keep factual notes, hypotheses, and project-specific proposals clearly separated.

## Research caution

The corpus currently contains paraphrased notes based on accessible bibliographic/abstract records. It is not a substitute for reading the complete papers. Similarity scores rank candidate notes; they are not confidence scores.