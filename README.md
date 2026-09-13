# research-animation

抽象的な変化を、点と運動だけで表現するアニメーション研究。

アニメーションを「動画を生成すること」ではなく、**変化を設計し、時間軸へ配置すること**として研究する。

## Research map

```text
変化の設計
   ├── dots PoC
   │    state → aw → next state → Pillow → GIF
   │
   └── Case Study: anima / PANACHE
        storyboard → frame extraction → temporal assembly → video
```

## Case Study: anima / PANACHE

`anima` は、絵コンテ駆動型アニメーションの実践事例として回収する。

2026/09/13 の PANACHE 告知用ローファイアニメーションでは、32コマを4fpsで連結して8秒の映像にする。前半16コマはりんごの巨大化、後半16コマは齧られていく変化を設計する。

画像生成側には動きそのものを要求せず、複数コマの絵コンテとして生成し、動画側で時間を与える。この「静止画の連続を状態変化として扱う」方法を、research-animation の実作品ケースとして位置づける。

詳細: `cases/anima-panache.md`

## dots PoC

生成AIやSDは使わず、最初のPoCは **LangGraphの `aw` 変化セル + Pillow renderer** で構成する。

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

既存のSD・建築アニメーション実験は残す。`anima` は作品化された絵コンテ駆動型のケース、dots PoCはそれとは独立した最小の状態遷移実験として扱う。
