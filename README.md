# research-animation

抽象的な変化を、点と運動だけで表現するアニメーション研究。

生成AIやSDは使わず、最初のPoCは **LangGraphの `aw` 変化セル + Pillow renderer** で構成する。

## dots PoC

```text
state
  ↓
LangGraph
  ↓
aw (change cell)
  ↓
next state
  ↓
Pillow
  ↓
GIF
```

`aw` は「どう変化するか」だけを担当し、Pillowは「どう描くか」だけを担当する。

```text
dots/
├── aw.py       # LangGraph state transition
├── render.py   # Pillow renderer
├── main.py     # animation runner
└── world.json  # PoC parameters
```

### Run

```bash
python -m pip install -r requirements-dots.txt
python -m dots.main --frames 60 --dots 24 --seed 42
```

出力:

```text
output/dots.gif
```

### Design

点を意味そのものとして扱うのではなく、運動によって抽象性を表現する。

- 集合 / 分散
- 同調 / ずれ
- 発生 / 消滅
- 反復 / 揺らぎ
- 同一性 / 変形

将来的に `aw` の実装だけを random / rule / Markov / LLM などへ交換できる。Pillow側は変更しない。

## Existing experiments

既存のSD・建築アニメーション実験は残す。dots PoCはそれらとは独立した、最小の状態遷移実験として追加する。
