# Research Strategy — The Skeleton Dance

## Objective

Build a small, reproducible pipeline that turns selected dance passages into a stick-figure animation and compares movement segments using explicit geometric, dynamic, temporal, and semantic features.

## Phase 0 — Source and research audit

- [ ] Read the direct film-analysis papers listed in papers.md.
- [ ] Identify a lawful, stable video source; record provenance and version.
- [ ] Select a short representative excerpt and write down start/end timecodes.
- [ ] Confirm whether pose extraction is reliable on the monochrome, stylized animation.
- [ ] Record uncertainty and manual corrections rather than silently filling missing keypoints.

Deliverable: a source register in CSV or JSONL plus a short evidence summary.

## Phase 1 — Annotation schema

Each frame or sampled timestamp should support:
- source_id
- timestamp_ms
- shot_id
- segment_id
- keypoints
- keypoint_confidence
- movement_label
- musical_event
- annotation_method (automatic, manual, or corrected)
- notes

Use JSONL as the portable record format. Keep raw observations separate from derived features.

## Phase 2 — Stick-figure baseline

1. Sample frames at a documented rate.
2. Extract pose keypoints using a pose estimator if appropriate; manually annotate a small subset as a reference.
3. Normalize coordinates for frame size and body scale.
4. Interpolate only short, explicitly marked gaps; preserve missing-value indicators.
5. Render a 2D stick figure with a timestamp and frame index.
6. Compare the rendering against source frames side by side.

Success criterion: the selected excerpt can be replayed with stable timing and documented limitations. Do not set a numerical accuracy target until a reference annotation subset exists.

## Phase 3 — Motion features

For each segment calculate:
- Pose: normalized joint positions and joint angles.
- Dynamics: per-joint velocity, acceleration, angular velocity, trajectory curvature.
- Rhythm: movement onset/offset, duration, periodicity, offset to annotated beat/phrase events.
- Semantics: manually reviewed labels such as turn, jump, sway, extend, collapse, or body-percussion.

Avoid mixing raw coordinates and semantic labels into one untraceable score. Preserve feature definitions and normalization choices.

## Phase 4 — Semantic Cube visualization

Proposed axes:
- X = pose/form similarity.
- Y = motion/dynamics similarity.
- Z = temporal/rhythmic similarity.

Plot movement segments as points or trajectories. Use a separate visual encoding for semantic labels and uncertainty. Document axis scaling and whether each dimension represents a measured feature, a composite score, or a user-controlled parameter.

Baseline comparisons:
1. Pose-only.
2. Pose + dynamics.
3. Pose + dynamics + timing.
4. Full feature set with semantic annotations.

Evaluate against human similarity judgments on a small, clearly described sample. The cube is a visualization and hypothesis, not proof of semantic equivalence.

## Phase 5 — Evaluation and reporting

- Segment-level boundary agreement.
- Keypoint reconstruction error on manually annotated frames.
- Beat/movement-event timing offset.
- Agreement between machine similarity ranking and human ratings.
- Error analysis by shot, occlusion, stylization, and unusual skeletal proportions.

Include negative results and failure cases.

## Proposed implementation modules

- source/ — source manifest and timecodes (no redistributed copyrighted film).
- annotations/ — JSONL annotations.
- scripts/extract_pose.py — frame sampling and pose extraction.
- scripts/render_stick_figure.py — stick-figure rendering.
- scripts/compute_features.py — feature derivation.
- viz/semantic_cube.html — interactive 3-axis visualization.
- reports/ — experiment results and figures.

These are proposed paths; do not create placeholder implementation files until the first experiment is ready.

## Risks and controls

| Risk | Control |
|---|---|
| Stylized skeletons confuse pose estimation | manually annotate a small benchmark subset |
| Camera cuts or framing changes distort coordinates | segment shots and normalize consistently |
| Timing mismatch with soundtrack | document source version and audio offset |
| Pose similarity mistaken for semantic similarity | compare multiple baselines and human ratings |
| Copyright or source uncertainty | keep provenance; do not redistribute film/audio |
| Unsupported claims from abstracts | verify full text and cite exact pages |

## Immediate next step

Read the two film-specific sources first, choose one short excerpt, and create a minimal manually checked pose sequence. Implement only after the annotation schema and evaluation baseline are agreed.
