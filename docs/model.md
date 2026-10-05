# SDI Model

## 1. Static World

Static World は「何が存在し、どう関係しているか」を表す。

```text
World
├── Entity
├── Relation
└── Capability
```

現在の PoC では `sdi/world.json` が Static World を保持する。

### Entity

Entity は世界に存在する対象。

- `id`
- `type`
- `x`
- `y`
- `radius`
- `capabilities`

### Relation

Relation は Entity 間の接続・関係。

### Capability

Capability は Entity が受け入れられる Dynamic Behavior の条件。

例:

```json
{
  "id": "a",
  "type": "node",
  "capabilities": ["move", "rotate"]
}
```

## 2. Dynamic Behavior

Dynamic Behavior は時間によって Static World をどう変化させるかを定義する。

現在の PoC では `sdi/behaviors.json` に外部化している。

```text
Behavior
├── type
├── parameters
└── description
```

PoC では `orbit`, `pulse`, `attract` を同じ World に適用する。

## 3. Interface

SDI の責務は Static World と Dynamic Behavior の境界を保つこと。

```text
world.json ──┐
             ├── SDI ──> renderer
behaviors.json ─┘
```

Renderer は世界の意味を定義しない。

Renderer が担当するのは、

1. データを読む
2. Behavior を選択する
3. 時間を渡す
4. 結果を描画する

## 4. 次のモデル

次の段階では Behavior を単なる数式ではなく、状態機械として扱う。

```text
Event
  ↓
State
  ↓
Transition
  ↓
Behavior
  ↓
Frame
```

これにより animation / simulation / interaction を同じモデルで扱える可能性がある。
