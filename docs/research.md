# Research Notes

## Hypothesis

> 同じ Static World に対して Dynamic Behavior だけを交換できる。

PoC 01 はこの仮説を最小構成で検証する。

## PoC 01

### Fixed

- Entity
- Relation
- Capability
- 初期位置
- Entity の大きさ

### Variable

- Behavior
- Behavior parameters
- 時間による変化

### Behaviors

| Behavior | 役割 |
|---|---|
| orbit | Entity の位置を時間に応じて回転 |
| pulse | Entity の大きさを周期的に変化 |
| attract | 中心方向への見え方を時間的に変化 |

## Validation

### V1 — Behavior の外部化

Behavior の実装・パラメータを World から分離する。

**Result:** `behaviors.json` を導入済み。

### V2 — World 不変で Behavior を交換

同じ `world.json` を読み込み、Behavior だけを切り替える。

**Result:** `index.html` で `orbit / pulse / attract` を切り替え可能。

### V3 — Capability による選択

Entity の Capability と Behavior の要求 Capability を照合して、適用可能な Behavior を選択する。

**Status:** next

### V4 — Event / State / Transition

時間だけでなく Event を入力として State を変化させる。

**Status:** next

### V5 — Architecture → Static World

建築・空間モデルを Entity / Relation / Capability に変換する。

**Status:** research

## Success criteria

SDI が成立したと言える条件:

1. World の意味構造を変更せず Behavior を交換できる
2. Renderer に Behavior の個別実装を増やさなくてよい
3. Capability から適用可能な Behavior を選択できる
4. Event / State / Transition を同じ境界に接続できる

## Next experiment

次はグラフィックを増やすのではなく、**Capability → Behavior Selection** を実装する。

```text
Entity
  │
  └─ Capability
       │
       ▼
Behavior Registry
       │
       ▼
Selection
       │
       ▼
Event → State → Transition
       │
       ▼
Animation
```
