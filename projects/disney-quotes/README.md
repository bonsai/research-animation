# DISNEY-QUOTES CORPUS

ディズニー（ウォルト・ディズニー）の言葉を、**アニメ映画生成の理論**に接続する研究用コーパス。

単なる名言集ではなく、以下の 5 段階ピラミッドで構造化する。

```text
QUOTE
  ↓
SOURCE / CONTEXT
  ↓
DOMAIN CONCEPT
  ↓
ONTOLOGICAL CANDIDATE
  ↓
GENERATION OPERATION
```

## 構成

- `corpus/` — SQLite DB (`../disney-quotes.db`) + JSONL 出力。machine-readable な本体。
  - `schema.sql` / `seed.py` / `seed_data.json` / `database.py`
  - 情報源（出典）は `sources` テーブルで管理（`corpus/schema.sql` 参照）。
- `ontology/` — 概念ライブラリと、制作原理（12 Principles）への対応表。
- `scripts/` — 収集・検証・統合・可視化のパイプライン。
- `viz/` — D3.js によるネットワークグラフビューア（quote ↔ concept ↔ operation）。
- `site/` — 生成される静的サイト（`index.html`）。
- `docs/` — 方法論・出典ポリシー・生成操作ライブラリ。
- `run.sh` — パイプライン一連実行。

## 設計原則

- 名言をそのまま「理論」とは扱わない。すべて仮説として記録し、出典強度を区別する。
- 生成操作は本研究側による**理論的抽象化**。
- DB を一次形式とし、Markdown / HTML / JSONL は出力結果（生成物）とする。
- 依存は標準ライブラリのみ（Python 3.11+）。

## 使い方

WSL inside で実行する（SQLite は `\\wsl.localhost\` の UNC パスで
`database is locked` になるため、Windows Python からは実行不可）。

```bash
cd projects/disney-quotes

# パイプライン一連実行（validate → graph → viz → site → jsonl）
./run.sh

# コーパスを作り直してから実行
./run.sh --init
```

個別に実行する場合:

```bash
python3 scripts/init.py           # コーパス初期化（12 個の Seed 名言）
python3 scripts/validate.py       # 整合性検証
python3 scripts/harvest.py        # 収集スタブ → corpus/candidates.jsonl
python3 scripts/graph-builder.py  # viz/network.json
python3 scripts/build-viz.py      # viz/index.html
python3 scripts/build-site.py     # site/index.html
```

生成物はすべて DB から作り直せる。手で編集するファイルは
`corpus/seed_data.json` と `corpus/schema.sql` のみ。

## 現在の状態

- 名言 12 件 / 概念 32 件 / 生成操作 13 件 / エッジ 49 本
- 出典検証済み 6 件、未検証（WARNING）6 件
- 次は出典の追跡と Pixar 比較モジュール

## Next

1. 出典の追跡（Walt Disney Archives / D23 の一次資料を優先）。
2. 名言の分類（story / character / animation / audience / collaboration / technology / iteration）。
3. 12 Principles との接続。
4. Pixar・吉卜力との比較分析モジュール。
5. 収集スクリプトの自動化（harvest.py）。

## 参照

- The Walt Disney Company — Mickey / Walt quote
- D23 — Disney storytelling / production history
- Walt Disney Archives / *The Official Walt Disney Quote Book*
- Karal Ann Marling, "Disneyland, 1955: Just Take the Santa Ana Freeway to the American Dream," *American Art* (1991)
- Randy Bright, *Disneyland: Inside Story* (1987)
- Derek Walker, *Animated Architecture* (1982)
