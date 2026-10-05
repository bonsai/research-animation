# research-animation

**アニメ映画生成の理論を構築する研究プロジェクト群。**

## Projects

| Project | Research question | Status |
|---|---|---|
| [SDI](./projects/sdi/) | Static World と Dynamic Behavior を分離できるか | active |
| [Dots](./projects/dots/) | 最小の点群で状態変化を記述できるか | active |
| [Morph](./projects/morph/) | State A → B の変化経路を記述できるか | research |
| [Montage](./projects/montage/) | 状態／ショット間の関係から意味を生成できるか | research |
| [Architecture](./projects/architecture/) | 建築・空間を Static World として扱えるか | research |

## Common theory

複数プロジェクトを横断する共通モデルは以下で管理する。

- [DOMAIN](./DOMAIN.md) — 研究対象と境界
- [ONTOLOGY](./ONTOLOGY.md) — Change Ontology
- [TAXONOMY](./TAXONOMY.md) — 概念の分類
- [RQ](./RQ.md) — Research Questions
- [PRINCIPLES](./PRINCIPLES.md) — 研究原則

## Architecture

```text
research-animation
│
├── projects/          # 問いごとの研究プロジェクト
│   ├── sdi/
│   ├── dots/
│   ├── morph/
│   ├── montage/
│   └── architecture/
│
├── research/          # 実験記録・調査・スクリプト
├── sdi/               # SDI PoC implementation
├── dots/              # Dots implementation
└── docs/              # 共通ドキュメント
```

原則は **1 project = 1 research question**。

実装をプロジェクト定義に混ぜず、`projects/` は「何を検証するか」、実装ディレクトリは「どう検証するか」を担当する。

## Core model

```text
ENTITY
  ↓
STATE
  ↓
DIFFERENCE
  ↓
RELATION
  ↓
TRANSFORMATION / MORPH
  ↓
TIME
  ↓
SEQUENCE
  ↓
PERCEPTION
  ↓
GENERATION
  ↓
ANIMATED FILM
```
