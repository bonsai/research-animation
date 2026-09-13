# Research Themes — UiPath-assisted Research Animation

## 1. Positioning

The repository's main RQ asks how still images, points, and states can be designed as **change** and placed on a time axis so that they are perceived and understood as animation.

`anima` is positioned as the practical case for RQ5, while `dots` is the abstract case for RQ1–RQ4. The implementations remain outside the research argument.

This document defines the research themes that an external research agent can investigate and return as evidence for the theoretical argument.

## 2. Core research theme

### Research Theme A — Animation as designed change

**Question:** Can animation be theoretically described not as a sequence of images, but as the design and temporal organization of state changes?

**Investigate:**
- animation theory and definitions of movement/change
- frame, state, transition, interval, repetition, and pause
- perception of apparent motion and temporal organization
- theories that distinguish representation from transformation

**Expected output:** competing definitions, key concepts, primary sources, and a synthesis supporting or challenging the proposed RQ5 framing.

### Research Theme B — Change as the minimum semantic unit

**Question:** Is "change" a more useful analytical unit than "object" for explaining animation?

**Investigate:**
- object-centered vs event/change-centered descriptions
- Gestalt and perceptual organization
- motion perception and event perception
- whether meaning can emerge from relations between successive states

**Expected output:** theoretical arguments for and against treating change as the minimum unit.

### Research Theme C — State difference and motion

**Question:** Can movement be described as a difference between states rather than as a property of an object?

**Investigate:**
- state-transition models
- temporal difference
- discrete vs continuous motion
- computational representations of animation
- relations between transition rules and perceived movement

**Expected output:** a conceptual model linking `state_t → state_t+1 → perceived change`.

### Research Theme D — Time as meaning

**Question:** How do velocity, interval, repetition, synchronization, and stopping change what an animation means?

**Investigate:**
- timing and spacing
- rhythm and repetition
- anticipation, pause, acceleration, deceleration
- synchronization and phase differences
- temporal perception

**Expected output:** a taxonomy of temporal operations and their possible perceptual effects.

### Research Theme E — Abstract motion and conceptual perception

**Question:** Can non-narrative elements such as dots and simple shapes communicate concepts through motion alone?

**Investigate:**
- emergence / disappearance
- aggregation / dispersion
- synchronization / desynchronization
- alignment / deviation
- attraction / repulsion
- continuity / interruption

**Expected output:** a mapping between abstract motion patterns and candidate perceptual concepts, with evidence and counterexamples.

### Research Theme F — Animation generation as temporal design

**Question:** Can animation generation be redefined from "generate a video" to "design changing states and place them on a timeline"?

**Investigate:**
- procedural animation
- keyframes and state machines
- rule-based generation
- generative AI video vs structured animation
- controllability and reproducibility

**Expected output:** a theoretical comparison between direct video generation and state/time-based generation.

## 3. Research method

The research agent should follow:

```text
question
  ↓
search
  ↓
source selection
  ↓
extract claim
  ↓
compare theories
  ↓
record evidence
  ↓
map to RQ1–RQ5
  ↓
propose synthesis
```

Every important claim should preserve:

- author
- year
- title
- publication / venue
- URL or DOI
- exact claim or short quotation
- interpretation
- relation to RQ1–RQ5
- confidence

Do not treat an implementation result as theoretical evidence by itself.

## 4. UiPath research-agent task

UiPath can be used as the execution layer for browser/API research where repeated collection, extraction, normalization, and evidence capture are useful.

Target workflow:

```text
GitHub research task
        ↓
UiPath Agent
        ↓
web / API / documents
        ↓
structured evidence
        ↓
Markdown research report
        ↓
GitHub commit
```

The UiPath CLI exposes MCP through `uip mcp serve`, allowing MCP-aware agents to invoke `uip` commands. For agent development, UiPath also provides Python, LangGraph, LlamaIndex, MCP, and TypeScript SDKs.

For this repository, the preferred contract is **research first, implementation second**. The agent should return theory, evidence, and RQ mapping before proposing code changes.

## 5. First research batch

Start with five parallel questions:

1. What are the strongest theoretical definitions of animation as change over time?
2. What evidence supports change/state-transition as an analytical unit of animation?
3. How do timing and spacing alter perceived meaning in animation?
4. How can abstract motion communicate concepts without representational objects?
5. What theoretical basis supports state/time-based animation generation over direct video generation?

## 6. Deliverable

The first deliverable should be:

`research/LITERATURE-MAP-001.md`

with sections:

- Research question
- Search scope
- Sources
- Claims
- Conflicting positions
- RQ mapping
- Synthesis
- Open questions
- Candidate theoretical contribution

No implementation is required for this research batch.
