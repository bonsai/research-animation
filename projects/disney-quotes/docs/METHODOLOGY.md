# DISNEY-QUOTES CORPUS — Methodology

このプロジェクトは、ディズニー名言を収集して**アニメ映画生成の理論**に接続することを目的とする。
名言は「理論」として採用されるのではなく、本研究側による**理論的抽象化の仮説**として記録される。

## 5 段階ピラミッド

```text
QUOTE                      収集対象の発言（一次/二次テキスト）
   ↓
SOURCE / CONTEXT           いつ・どこで・誰に語られたか（出典・文脈）
   ↓
DOMAIN CONCEPT             言語学的・意味論的な抽象語（例: origin, constraint, iteration）
   ↓
ONTOLOGICAL CANDIDATE      生成系ontology の候補タグ（大文字コード、本研究独自の語彙）
   ↓
GENERATION OPERATION       その名言が示唆する具体的な生成操作（コード + 説明）
```

各レイヤは多対多の関係になり得る。1 つの名言が複数の概念と複数の操作に対応し、
1 つの操作も複数の名言によって支えられる。

## 処理パイプライン

1. **収集 (harvest)** — 情報源からの引用取得。候補は `confidence` (0.0–1.0) でグレード分け。
2. **検証 (validate)** — スキーマ整合、未所属のマッピングのチェック。
3. **接続 (pipeline)** — 5 段階を DB 結合で結び、ビュー `v_quote_pipeline` で参照。
4. **出力** — JSONL、静的サイト、D3 ネットワークグラフへ展開。

## 出典強度 (source strength)

- `PRIMARY` — 一次資料（録音・自伝・直接インタビュー）に裏打ち
- `SECONDARY` — 信頼性の高い伝記・研究書による引用
- `TERTIARY` — 名言集サイトなど二次的流通
- `UNKNOWN` — 出典不明

## データ形式の役割分担

- **SQLite** `disney-quotes.db` — 一次データベース（生成物）
- **JSONL** `corpus/*.jsonl` — ポータブルな交换形式
- **Markdown** `docs/*.md` — 人間が読むドキュメント（生成物）
- **Markdown** `projects/DISNEY-QUOTES.md` — レガシー（このプロジェクトに統合済み）

## 拡張の方向

- 比較モジュール（Pixar / Ghibli の名言との差分抽出）
- 収集スクリプトの実装（API/スクレイピング、Robots 遵守）
- 12 Principles との双方向リンク
- 生成実験との対応付け（`research/` の実験結果へのリンク）
