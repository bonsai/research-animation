# Research Plan — Morphing as Video Generation Logic

## 0. Principle

This research treats **Morphing as a lower-level research object of animation**: not a separate domain, but a common logic for constructing video from a sequence of image states and transformations between them.

`Research Plan → RQ → Thesis/Antithesis → Gap → RW → TF → AW → Evidence → Evaluation → Revision → Next Question`

## 1. Purpose

Identify whether image morphing, video frame interpolation, motion estimation, and modern video generation can be understood through a common abstraction:

`state → transformation → state → transformation → ...`

The goal is to establish a research-grounded logic for video generation rather than to implement a new video model at this stage.

## 2. Scope

- Domain: animation / moving image / video generation
- Subdomain: morphing and frame-to-frame transformation
- Object: image states, frame sequences, transformations, temporal continuity
- Cases: classical image morphing, frame interpolation, video generation, `anima`
- Boundary: theory and prior research first; implementation remains in existing case repositories
- Exclusions: training a foundation model, benchmarking a new model, production video tooling

## 3. Research Questions

### RQ-M1 — State

Can a video be described as a sequence of image states `I₀ ... Iₙ`?

### RQ-M2 — Transformation

Can the transition `Iₜ → Iₜ₊₁` be described as an explicit transformation rule rather than merely as a pair of images?

### RQ-M3 — Continuity

What conditions make a sequence of transformed states perceptually continuous as motion?

### RQ-M4 — Time

How does introducing a temporal parameter `t` change the representation of transformation, including speed, pause, acceleration, repetition, and duration?

### RQ-M5 — Generation

Can video generation be reframed as generation of image states plus transformation rules, rather than direct generation of a video object?

## 4. Working Thesis

### T-M1

**Claim:** A useful common abstraction across image morphing, frame interpolation, and video generation is a sequence of states connected by transformation rules.

**Status:** proposed

**Confidence:** medium

### T-M2

**Claim:** Temporal continuity can be studied as a property of the transformation sequence, not only as a property of the generated frames themselves.

**Status:** proposed

**Confidence:** low

### T-M3

**Claim:** Modern image-to-video generation can be theoretically compared with classical morphing and frame interpolation when both are represented as state-transition systems.

**Status:** proposed

**Confidence:** low

## 5. Antithesis

### A-M1

Video cannot be reduced to independent images plus transformations because temporal coherence may emerge from latent spatiotemporal representations that are not expressible as explicit frame-to-frame rules.

### A-M2

Morphing and frame interpolation solve constrained interpolation problems, while generative video models synthesize new content; treating them as the same process may erase essential differences.

### A-M3

Perceptual continuity cannot be explained only by geometric or pixel-level transformation because semantics, objects, causality, sound, and narrative also contribute to video experience.

## 6. Falsification Conditions

The working thesis should be weakened or rejected if the literature shows that:

- a common state-transition representation cannot adequately describe major classes of video generation;
- temporal coherence depends fundamentally on representations that cannot be expressed through state transitions or transformations;
- the abstraction produces no explanatory advantage over existing terminology;
- the abstraction collapses important distinctions between morphing, interpolation, animation, and generative video.

## 7. Research Way (RW)

`Question → Literature Exploration → Concept Extraction → Hypothesis → Cross-domain Comparison → Verification → Observation → Evidence → Evaluation → Revision`

### Phase 1 — Literature map

Survey classical image morphing, frame interpolation, optical flow, motion estimation, temporal consistency, and video diffusion.

### Phase 2 — Concept normalization

Extract recurring concepts such as:

- state
- correspondence
- transformation
- interpolation
- motion
- optical flow
- temporal consistency
- continuity
- occlusion
- latent dynamics
- temporal conditioning

### Phase 3 — Cross-domain matrix

Compare papers by:

`input states / transformation representation / temporal variable / continuity mechanism / output / limitations`

### Phase 4 — RQ mapping

Map each claim and piece of evidence to RQ-M1–RQ-M5.

### Phase 5 — Gap analysis

Identify what existing research explains well and what remains fragmented between morphing, interpolation, animation, and generative video.

### Phase 6 — Synthesis

Propose a minimal common model and explicitly state where the model fails.

## 8. Task Force (TF)

### TF-Literature

Find primary papers and authoritative surveys.

### TF-Concept

Extract definitions, mechanisms, assumptions, and limitations.

### TF-Comparison

Construct the cross-domain comparison matrix.

### TF-Critique

Search for counterexamples and literature that contradicts the working thesis.

### TF-Synthesis

Produce the final literature map and candidate theoretical model.

LlamaIndex is the research retrieval/organization layer for literature and evidence. It is not itself evidence for the thesis.

## 9. AW Execution Contract

`Work → Job → Task → Action → Outcome → Evidence`

### Work

Morphing literature research.

### Job

Determine whether frame-to-frame transformation is a useful common abstraction for video generation.

### Task

Search, retrieve, normalize, compare, and map primary literature.

### Action

LlamaIndex-based retrieval and indexing; source-level extraction; structured claim recording; contradiction search.

### Outcome

`research/LITERATURE-MAP-MORPHING-001.md`

### Evidence

Every substantive claim must retain source provenance: author, year, title, venue, DOI/URL, and the specific passage or result supporting the claim.

## 10. Evidence Discipline

`Observation ≠ Interpretation ≠ Hypothesis ≠ Conclusion`

A paper saying that a model performs frame interpolation is an observation about the paper, not evidence that all video generation is frame interpolation.

Evidence must distinguish:

1. what the source explicitly states;
2. our interpretation of that statement;
3. the hypothesis supported by the interpretation;
4. the scope and limitations of the conclusion.

## 11. Evaluation

Evaluate the proposed abstraction on four criteria:

- **Coverage:** Can it represent classical morphing, interpolation, and generative video?
- **Discrimination:** Can it preserve meaningful differences between those approaches?
- **Explanatory value:** Does it clarify existing fragmented terminology?
- **Research utility:** Can it generate testable future questions or design rules?

## 12. Revision

Do not overwrite historical claims. Record changes chronologically.

Possible outcomes:

- strengthen the state-transition thesis;
- qualify it as an analytical abstraction only;
- split geometric transformation from semantic generation;
- restrict the thesis to frame-sequence construction;
- reject the common abstraction if counterevidence is decisive.

## 13. Next Question

The next RQ should be generated from the strongest unresolved contradiction found in the literature map.

Candidate follow-up:

> What is the minimum representation of a transformation rule that preserves perceptual continuity between generated image states?
