# Skeleton Dance Literature RAG (LangChain)

Citation-first research RAG for Disney's *The Skeleton Dance* (1929), music/movement relations, dance pose analysis, and animation studies.

## Architecture

`knowledge.jsonl` → JSONL loader → LangChain `Document` objects → `BM25Retriever` → source-labelled context → optional `ChatOpenAI` answer chain.

- **Retrieval:** LangChain community BM25 retriever.
- **Generation:** LangChain prompt chain with `langchain-openai`; optional.
- **Citations:** every retrieved chunk preserves `source_id`, `chunk_id`, `evidence_type`, and source URL.
- **No key required** to retrieve evidence.
- This is lexical retrieval, not embedding/vector search. Scores are not confidence.
- Seed corpus is paraphrased notes from accessible metadata/abstract records, not full-text papers.

## Setup

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run retrieval only

```bash
python query.py "music structure and movement" --retrieve-only
python query.py "dance pose temporal segmentation" --top-k 5 --retrieve-only
```

## Generate a grounded answer

Set `OPENAI_API_KEY` in the environment (or copy `.env.example` to `.env` and load it using your preferred environment manager), then run:

```bash
# PowerShell
$env:OPENAI_API_KEY = "your-key"
python query.py "How does music structure relate to movement?"
```

Optional `OPENAI_BASE_URL` lets you use an OpenAI-compatible endpoint. Never commit real API keys. `--model` or `RAG_MODEL` selects the model.

## Data contract

One JSON object per line in `knowledge.jsonl`:

```json
{"chunk_id":"sd-001-a","source_id":"sd-001","title":"...","year":2021,"topics":["music","movement"],"evidence_type":"abstract_summary","text":"Paraphrased research note.","url":"https://doi.org/..."}
```

## Research integrity

- Do not present a project hypothesis as a published finding.
- Confirm claims in the original source before using them as factual conclusions.
- Respect the source's license and copyright; ingest full text only where permitted.
- Evaluate retrieval with research questions and expected source IDs before relying on answers.
- Similarity/retrieval ranking is not a probability of correctness.
