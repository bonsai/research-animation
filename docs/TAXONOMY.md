# Change Ontology Taxonomy

## Purpose

This taxonomy defines a reusable conceptual tool for generative agents to construct change.
It is not an implementation specification and does not belong to any single medium.

The same vocabulary should be applicable to `anima`, `dots`, and future generative domains.

## Core taxonomy

```text
ENTITY
  ↓
STATE
  ↓
RELATION
  ↓
DIFFERENCE
  ↓
TRANSFORM
  ↓
TIME
  ↓
SEQUENCE
  ↓
PERCEPTION
  ↓
GENERATION
```

### 1. Entity

What exists or is being operated on.

Examples: object, image, point, data structure, character, interface element.

### 2. State

A describable condition of an entity or system at a given moment.

The important unit is not the thing itself but **the thing-in-a-state**.

### 3. Relation

How entities or states are connected.

Examples: position, proximity, containment, dependency, correspondence, synchronization.

### 4. Difference

The distinction between states.

```text
STATE A → STATE B
          ↑
       DIFFERENCE
```

Difference is the basic candidate for the minimal unit of change.

### 5. Transform

An operation that turns one state into another.

```text
STATE A + TRANSFORM → STATE B
```

A generative agent can therefore reason about *how* a change is constructed rather than merely predicting an output.

### 6. Time

The placement, duration, ordering, interval, repetition, or pause of change.

Time converts a set of state differences into a temporal experience.

### 7. Sequence

An ordered construction of states and transformations.

```text
S0 → S1 → S2 → S3
```

A sequence is the primary generative structure for animation, but can also describe non-visual processes.

### 8. Perception

The interpretation of a sequence as movement, transformation, emergence, disappearance, rhythm, causality, or other meaningful change.

Perception is not assumed to be identical to the underlying transformation.

### 9. Generation

The production of a concrete artifact from the ontology.

```text
ONTOLOGY
   ↓
GENERATION PLAN
   ↓
ARTIFACT
```

The artifact may be frames, animation, data, UI, simulation, or another medium.

## Generative construction rule

The ontology can be used as a conceptual construction tool:

```text
What exists?
  → ENTITY

What state is it in?
  → STATE

What is related?
  → RELATION

What changes?
  → DIFFERENCE

How does it change?
  → TRANSFORM

When does it change?
  → TIME

How are changes ordered?
  → SEQUENCE

How might the change be perceived?
  → PERCEPTION

What should be generated?
  → GENERATION
```

## Case positioning

### anima

`anima` tests the ontology through concrete visual change: an entity is represented across changing states and placed on a temporal sequence.

Implementation remains in `bonsai/anima`.

### dots

`dots` tests the ontology through abstract state and structural change. The entity need not be a conventional visual object; state and difference can be represented independently of a concrete object.

Implementation remains in `bonsai/dots`.

## Central hypothesis

> Animation and other generative processes can be described as the construction of state differences and their temporal relations.

The stronger research hypothesis is:

> A medium-independent change ontology can provide generative agents with a common conceptual construction tool for producing transformations across different domains.

## Boundary

`research-animation` develops the ontology, taxonomy, research questions, and theory.

Implementation, APIs, schemas, rendering, and generation pipelines remain in the respective case repositories.
