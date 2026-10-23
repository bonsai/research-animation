#!/usr/bin/env python3
"""Citation-first LangChain RAG over the curated Skeleton Dance JSONL corpus."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever

HERE = Path(__file__).resolve().parent


def load_documents(path: Path) -> list[Document]:
    documents: list[Document] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            for key in ("chunk_id", "source_id", "text", "url"):
                if key not in row:
                    raise ValueError(f"missing required field: {key}")
            page_content = (
                f"Title: {row.get('title', row['chunk_id'])}\n"
                f"Year: {row.get('year', 'n/a')}\n"
                f"Topics: {', '.join(row.get('topics', []))}\n"
                f"Evidence type: {row.get('evidence_type', 'unspecified')}\n"
                f"Research note: {row['text']}"
            )
            documents.append(
                Document(
                    page_content=page_content,
                    metadata={
                        "chunk_id": row["chunk_id"],
                        "source_id": row["source_id"],
                        "title": row.get("title", row["chunk_id"]),
                        "year": row.get("year"),
                        "url": row["url"],
                        "evidence_type": row.get("evidence_type", "unspecified"),
                    },
                )
            )
        except Exception as exc:
            raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    if not documents:
        raise SystemExit(f"No documents found in {path}")
    return documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the Skeleton Dance research corpus with LangChain.")
    parser.add_argument("query", help="Research question in Japanese or English")
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--retrieve-only", action="store_true", help="Show retrieved evidence without calling an LLM")
    parser.add_argument("--model", default=os.getenv("RAG_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--base-url", default=os.getenv("OPENAI_BASE_URL"))
    parser.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY"))
    args = parser.parse_args()
    if args.top_k < 1:
        parser.error("--top-k must be >= 1")

    docs = load_documents(HERE / "knowledge.jsonl")
    retriever = BM25Retriever.from_documents(docs)
    retriever.k = args.top_k
    hits = retriever.invoke(args.query)

    print(f"Query: {args.query}\nRetriever: LangChain BM25 | hits: {len(hits)}\n")
    if not hits:
        print("No matching notes. Try terms such as music, pose, rhythm, skeleton, segmentation.")
        return

    for index, doc in enumerate(hits, 1):
        meta = doc.metadata
        print(f"[{index}] {meta['title']}")
        print(f"    source_id={meta['source_id']} | chunk_id={meta['chunk_id']} | year={meta.get('year')}")
        print(f"    {doc.page_content.split('Research note: ', 1)[-1]}")
        print(f"    Evidence type: {meta['evidence_type']}")
        print(f"    Source: {meta['url']}\n")

    if args.retrieve_only or not args.api_key:
        if not args.api_key and not args.retrieve_only:
            print("LLM answer skipped: OPENAI_API_KEY is not set. Use --retrieve-only for explicit retrieval-only mode.")
        print("Ranking is lexical relevance, not confidence. Verify claims against the cited publication.")
        return

    # Imports are deferred so retrieval-only use stays lightweight after installation.
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    context = "\n\n".join(
        f"[{i}] source_id={doc.metadata['source_id']} | chunk_id={doc.metadata['chunk_id']}\n"
        f"Title: {doc.metadata['title']} ({doc.metadata.get('year', 'n/a')})\n"
        f"Evidence type: {doc.metadata['evidence_type']}\n"
        f"URL: {doc.metadata['url']}\n{doc.page_content}"
        for i, doc in enumerate(hits, 1)
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a careful research assistant. Answer only from the supplied retrieved notes.
Distinguish published-paper summaries from project hypotheses. Do not invent methods, findings, page numbers, or citations.
Attach citations inline using [source_id] and include the exact source URLs in a Sources list.
If the notes do not support an answer, say what is unknown and what original source needs checking.
The indexed notes are paraphrases, not the full papers."""),
        ("human", "Research question: {question}\n\nRetrieved evidence:\n{context}\n\nWrite a concise answer in the same language as the question, with explicit limits.")
    ])
    llm_kwargs = {"model": args.model, "temperature": 0}
    if args.base_url:
        llm_kwargs["base_url"] = args.base_url
    chain = prompt | ChatOpenAI(**llm_kwargs)
    answer = chain.invoke({"question": args.query, "context": context})
    print("\n=== LangChain grounded answer ===\n")
    print(answer.content)


if __name__ == "__main__":
    main()
