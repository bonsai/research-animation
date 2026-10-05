# SDI — Static–Dynamic Interface

Static–Dynamic Interface (SDI) is a small animation research experiment for separating **what exists** from **how it behaves**.

## Core hypothesis

> The same Static World can accept interchangeable Dynamic Behaviors without changing its entities or relations.

```text
world.json
  Entity / Relation / Capability
          │
          ▼
         SDI
          │
          ├── behaviors.json
          │      ├── orbit
          │      ├── pulse
          │      └── attract
          │
          ▼
      animation
```

## Repository model

| Layer | File | Responsibility |
|---|---|---|
| Static World | `world.json` | entities, relations, capabilities, initial geometry |
| Dynamic Behavior | `behaviors.json` | behavior definitions and parameters |
| Interface / Renderer | `index.html` | loads both layers and renders the result |

The important boundary is:

- **Static**: identity, type, position, relation, capability
- **Dynamic**: time-dependent transformation
- **Renderer**: presentation only

## PoC 01

The four nodes and their connections stay unchanged while `orbit`, `pulse`, and `attract` are swapped.

Open `index.html` in a browser and switch the behavior buttons.

## Research questions

1. Can behaviors be defined entirely outside the renderer?
2. Can a behavior be selected from an entity's capabilities?
3. Can SDI represent Event → State → Transition?
4. Can an architectural model become a Static World?
5. Can the same world drive animation, simulation, and interaction?

## Next step

The next useful experiment is not another animation effect. It is to formalize the interface:

```text
Static World
  Entity
  Relation
  Capability
       │
       ▼
Dynamic Behavior
  Event
  State
  Transition
       │
       ▼
Renderer / Simulator
```

This keeps the experiment focused on the **interface between static semantics and dynamic behavior**, rather than on graphics effects.
