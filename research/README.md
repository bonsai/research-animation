# research — 生成画像の評価とフィードバック

本ディレクトリは **生成されたイメージを対象とした評価・フィードバックの研究** を蓄積する。

ドキュメントとコードは分離して管理する。

```
research/
├── docs/        # 設計書・実験定義・結果報告・文献マップ
└── src/         # 生成・評価・コンテキスト構築・可視化スクリプト
```

---

## docs/ — ドキュメント

| パス | 内容 |
|---|---|
| `docs/README.md` | テーマ宣言と構成の詳細 |
| `docs/RQ.md` | 研究質問（主RQ・副RQ・反証条件） |
| `docs/pipeline/design.md` | 評価→フィードバック→生成のパイプライン設計 |
| `docs/literature/` | 論文マップとサマリー |
| `docs/experiments/` | 実験定義・テンプレート・採点シート・結果報告 |
| `docs/archive/` | 旧卒制資料・morphing 計画・AAS 設計書など |

### 進行中の実験

- **EXP-CTX-001** — 全要素コンテキスト反復生成
  - 詳細: `docs/experiments/EXP-CTX-001.md`
  - 結果: `docs/experiments/EXP-CTX-001-RESULTS.md`
  - 実験記録: `docs/experiments/EXP-CTX-001/{A,B,C,D}/`

---

## src/ — コード

| パス | 内容 |
|---|---|
| `src/generate_mock.py` | モック画像生成（パイプラインテスト用） |
| `src/generate_flux.py` | Diffusers ベース画像生成（Flux/SD fallback） |
| `src/generate_frames.py` | SD 1.5 ローカル生成（frame pool 用） |
| `src/build_context.py` | コンテキスト JSON → 自然言語プロンプト構築 |
| `src/plot_results.py` | スコア推移グラフ・レーダーチャート生成 |
| `src/plot_comparison.py` | 4群比較グラフ生成 |
| `src/playback.py` | フレームプールから再生レシピ作成 |
| `src/render_video.py` | ffmpeg による MP4 レンダリング |
| `src/architecture_animation.py` | PyVista 建築アニメーション |
| `src/gen_img.sh` | フレームプール生成バッチ |
| `src/gen_mov.sh` | 動画生成バッチ |
| `src/prompts.json` | プロンプト preset 設定 |
| `src/requirements-architecture.txt` | Python 依存パッケージ |

### 実行例

```bash
# モック画像生成（パイプラインテスト）
cd research
python3 src/generate_mock.py --prompt "sunset factory" --seed 42 --out-dir docs/experiments/EXP-CTX-001/D/runs --run-id run-004

# コンテキストからプロンプト構築
python3 src/build_context.py --context docs/experiments/EXP-CTX-001/D/context-run3.json --output-prompt /tmp/prompt.txt

# 比較グラフ生成
python3 src/plot_comparison.py --base-dir docs/experiments/EXP-CTX-001 --output docs/experiments/EXP-CTX-001/comparison.png
```

---

## 規約

- `docs/` は文書のみ。実行可能コードは置かない。
- `src/` は実行可能コードと設定のみ。論文や実験記録は置かない。
- 実験の記録（コンテキスト JSON、採点結果、グラフ）は `docs/experiments/` に保存する。

---
*基準日: 2026-10-05（document/code 分離）*
