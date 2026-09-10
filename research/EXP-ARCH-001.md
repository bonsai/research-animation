# EXP-ARCH-001 — Architectural Construction Animation

## Question

Can temporal construction of architecture reveal spatial relations that static 3D representation does not?

## Baseline sequence

`Site → Grid → Structure → Wall → Opening → Light → Human → Movement`

The baseline is procedural so that geometry and time are fully reproducible before introducing real CAD/BIM sources.

## Run

```bash
cd research-animation
python -m pip install -r research/requirements-architecture.txt
python research/architecture_animation.py --format gif
```

For MP4:

```bash
python research/architecture_animation.py --format mp4
```

For both:

```bash
python research/architecture_animation.py --format both
```

Useful quick test:

```bash
python research/architecture_animation.py --duration 3 --fps 5 --format gif
```

## Outputs

The renderer writes:

- `architectural-construction.gif`
- `architectural-construction.mp4` when requested
- `architectural-construction.manifest.json`

The manifest preserves experiment id, duration, frame rate, seed, renderer, camera and scene stages.

## Research boundary

The movie is a research artifact, not Evidence by itself.

```text
Geometry
  ↓
Animation
  ↓
Observation / Measurement
  ↓
Evaluation
  ↓
Evidence
```

RX records the researcher's experience separately:

```text
Observation → Experience → Interpretation → State Update → Next RQ
```

## Next

Compare the animated representation against static CAD/3D views under `bonsai/research-architecture` RQ-009 / EXP-002, then replace the procedural geometry with a real CAD/BIM/mesh source.
