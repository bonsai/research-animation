# The Skeleton Dance (1929) — Motion Semantics Research

## Research question

Can the dance motion in Disney's The Skeleton Dance (1929) be represented as a reproducible stick-figure animation and compared with other motion sequences in a semantic feature space?

## Core hypothesis

Pose similarity alone is insufficient to describe dance similarity. Combining pose geometry, motion dynamics, and temporal/rhythmic structure may provide a more useful representation for comparing movement.

## Scope

- Case study: The Skeleton Dance (1929), produced by Walt Disney, animated by Ub Iwerks, with music by Carl W. Stalling.
- Primary output: a stick-figure animation reconstructed from a video-derived pose sequence.
- Analysis: movement segmentation, music/motion alignment, and comparison in a proposed Semantic Cube.
- This is a research specification; implementation and results are not yet claimed.

## Research questions

1. How reliably can major poses and motion segments be recovered from the film?
2. How do pose changes relate to musical beats and phrases?
3. Does a multi-axis feature space capture perceived motion similarity better than pose coordinates alone?
4. Which movements are distinctive because of timing, articulation, or using the skeleton body as a percussive instrument?

## Proposed Semantic Cube

| Axis | Meaning | Candidate measurements |
|---|---|---|
| X — Pose / Form | Body configuration | normalized joint coordinates, joint angles |
| Y — Dynamics | How the body moves | velocity, acceleration, trajectory, angular velocity |
| Z — Time / Rhythm | When and how cyclically it moves | beat alignment, duration, periodicity, segment boundaries |

These axes are a project proposal, not an established standard. Semantic labels such as jump, turn, sway, and body-percussion should be stored separately from numeric measurements.

## Workflow

1. Identify a legally accessible reference video and document its provenance.
2. Define an annotation schema for shots, movement segments, and musical events.
3. Extract pose/keypoints where the stylized animation permits reliable detection.
4. Normalize coordinates and compute pose, dynamics, and temporal features.
5. Render the extracted sequence as a stick figure.
6. Visualize selected features in a Semantic Cube and compare motion segments.
7. Evaluate reconstruction and semantic agreement; record failure cases.

## Literature RAG

The initial citation-first RAG prototype lives in [rag/](./rag/).

- [RAG README and run instructions](./rag/README.md)
- [Source registry](./rag/sources.jsonl)
- [Retrieval knowledge chunks](./rag/knowledge.jsonl)
- [Local query CLI](./rag/query.py)

The current retriever is lexical (BM25-like term scoring), not embedding-based semantic search. Its corpus contains paraphrased notes from public bibliographic/abstract records, not copied full papers. Each answer candidate includes a source URL and evidence type; verify claims against the original publication.

## Evaluation

- Pose reconstruction: normalized keypoint error where reference annotations are available.
- Segmentation: boundary precision/recall or F1 against manually annotated segments.
- Rhythm: time offset between annotated beats and movement events.
- Semantic comparison: human-rated similarity versus feature-space similarity.
- RAG quality: answerable research questions, expected source IDs, citation coverage, and unsupported-claim rate.
- Reproducibility: documented source, processing parameters, annotations, and scripts.

Do not report these metrics until an experiment has actually been run.

## Initial references

See [papers.md](./papers.md) for the bibliography and evidence notes, and [strategy.md](./strategy.md) for the experiment plan.

## Provenance and rights

Record the exact video source, access date, version, and timecodes before analysis. The film's age does not automatically make every upload, soundtrack, restoration, or derivative copy public domain in every jurisdiction. Prefer lawful sources and publish derived annotations or original code rather than redistributing the film.
