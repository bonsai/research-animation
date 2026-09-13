# Change Ontology for Generative Agents

## Definition

This ontology describes the concepts and relations an agent needs in order to **construct and generate change**.

It is medium-independent. Animation is the initial research domain, but the ontology is intended to apply to images, data, interfaces, simulations, games, robotics, stories, and other generative systems.

> **The ontology is not a catalog of things. It is a vocabulary of relations that makes change generatable.**

## Ontological primitives

### Entity

An identifiable thing, element, object, process, or abstract unit that can participate in a state.

### State

A condition of an entity or system that can be described at a given point in a process.

### Relation

A meaningful connection between entities or states.

### Difference

A distinction between two states. Difference is the fundamental candidate for representing change.

### Transformation

A rule, operation, or process that maps one state to another.

### Time

The dimension in which states and transformations are ordered, delayed, repeated, accelerated, or paused.

### Sequence

An ordered set of states and/or transformations.

### Perception

The interpretation of a sequence as meaningful change: motion, emergence, disappearance, rhythm, causality, synchronization, deviation, and so on.

### Generation

The act of constructing a concrete artifact or process from an abstract specification of states, differences, transformations, and temporal relations.

## Core relations

```text
Entity ──has──> State
Entity ──relates_to──> Entity
State ──differs_from──> State
State ──transformed_by──> Transformation
Transformation ──produces──> State
State ──ordered_by──> Time
State ──part_of──> Sequence
Sequence ──may_be_perceived_as──> Change
Ontology ──guides──> Generation
```

## Montage relation

Film montage provides an important historical case for the ontology of change.

Eisenstein's montage theory is useful here not because the phrase **「コマとコマの間に映画が宿る」** can be established as a verified direct quotation, but because his theory explicitly treats the relation between shots as productive of meaning. The safer research formulation is:

> **映画はショットそのものだけではなく、ショットとショットの関係によって生成される。**

In particular, montage can be modeled as a relation in which two independently presented units produce a third perceived meaning:

```text
SHOT A + SHOT B
      ↓
   RELATION / COLLISION
      ↓
  PERCEIVED MEANING C
```

This is closely related to the ontology's distinction between **STATE**, **DIFFERENCE**, **RELATION**, and **PERCEPTION**.

For research precision, use **ショット** or **モンタージュ単位** when discussing Eisenstein rather than treating the claim as a statement about individual film frames. Extending the idea from shot-to-shot montage to frame-to-frame animation is a later theoretical generalization.

Kurosawa's editing practice likewise provides a concrete cinematic case in which action and emotional effect are constructed across cuts and fragmented shots. However, the exact phrase 「コマとコマの間に映画が宿る」 should not be attributed to Kurosawa without a primary-source citation.

The pedagogical aphorism **“What happens between shots happens between your ears”** is useful as a description of shot-relational perception, but should not be presented as a quotation by Eisenstein or Kurosawa without evidence.

## Generative graph

```text
        ENTITY
           │
        has STATE
           │
      ┌────┴────┐
      │         │
   STATE A   STATE B
      │         │
      └── DIFF ─┘
           │
     TRANSFORMATION
           │
         TIME
           │
       SEQUENCE
           │
       PERCEPTION
           │
       GENERATION
```

The montage case adds an important relational branch:

```text
STATE A ──┐
          ├── RELATION ──> PERCEIVED MEANING
STATE B ──┘
```

The agent therefore needs to represent not only **what changes**, but also **what relation between states produces a perceived effect**.

## Agent use

The ontology provides a conceptual intermediate representation between an intention and a generated artifact.

```text
INTENTION
   ↓
ONTOLOGICAL DESCRIPTION
   ↓
STATE / DIFFERENCE / RELATION / TRANSFORMATION / TIME
   ↓
GENERATION PLAN
   ↓
ARTIFACT
```

This suggests a research direction in which the agent generates **change specifications first**, and only then generates the medium-specific output.

## Animation as a test domain

Animation is treated as a particularly clear test of the ontology because the same conceptual structure can describe both concrete and abstract change.

### anima

A concrete visual entity changes state across a temporal sequence.

```text
image/object
   → state difference
   → temporal sequence
   → animation
```

### dots

An abstract entity or system changes state without requiring a conventional object as the semantic center.

```text
state/structure
   → state difference
   → temporal sequence
   → animation
```

### montage

A cinematic unit acquires or changes meaning through its relation to another unit.

```text
shot A
   + relation
shot B
   → perceived meaning
```

The three cases therefore test different aspects of the same ontology:

- **anima** — concrete visual state change
- **dots** — abstract structural state change
- **montage** — relational meaning generated between states/units

## Ontology vs taxonomy

`ONTOLOGY.md` defines the **entities, concepts, and relations** needed for generative reasoning.

`TAXONOMY.md` organizes those concepts into a practical hierarchy for constructing change.

In short:

```text
ONTOLOGY = what concepts and relations exist?
TAXONOMY = how are those concepts organized for construction?
```

## Central proposition

> **Generative agents need an ontology of change, not merely an ontology of objects.**

A stronger formulation emerging from montage theory is:

> **Generative agents need to represent not only states and their differences, but also the relations through which differences become perceptible meaning.**

The research question is therefore not only how an agent can identify what exists, but how it can represent **what can become different, how it becomes different, what relation connects the states, and how that difference can be constructed and perceived in time**.
