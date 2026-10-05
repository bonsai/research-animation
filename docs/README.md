# research-animation / docs

このディレクトリは、アニメーションを「描画」ではなく、**Static World と Dynamic Behavior の関係**として研究するための設計ドキュメントです。

## Research map

```text
World Model
    │
    ▼
Static World
 Entity / Relation / Capability
    │
    ▼
Static–Dynamic Interface (SDI)
    │
    ▼
Dynamic Behavior
 Event / State / Transition
    │
    ▼
Animation / Simulation / Interaction
```

## Experiments

| Experiment | Purpose | Status |
|---|---|---|
| [SDI PoC 01](../sdi/) | 同じ Static World に複数の Behavior を差し替える | active |

## Documents

- [model.md](./model.md) — Static / Dynamic の境界とデータモデル
- [research.md](./research.md) — 仮説・検証項目・次の実験

## Design principle

**World を変更せず、Behavior を交換する。**

この原則を、animation だけでなく simulation や interaction にも適用できるかを検証する。
