# Pipeline Design — 評価・フィードバック・再生成ループ

本テーマの中核となる実験パイプラインの設計書。

## 1. 全体構成

```
[Input]
   │ プロンプト・パラメータ・LoRA重み・シード
   ▼
┌─────────────────┐
│ 1. Generator    │  ComfyUI / SD / Flux 等
│    画像生成      │  出力: Image (I_t)
└─────────────────┘
   │
   ▼ I_t
┌─────────────────┐
│ 2. Evaluator    │  多軸評価
│    評価層       │  ├── VLM critic（自動）
│                 │  ├── 自動指標（CLIP/FID/美学的スコア）
│                 │  └── 人間評価（盲検 5段階）
└─────────────────┘
   │ 評価ベクトル E_t = (quality, style, semantic, preference)
   ▼
┌─────────────────┐
│ 3. Diff         │  E_t の変動・目標との差分
│    差分抽出      │  ΔE_t = E_target − E_t
└─────────────────┘
   │
   ▼ ΔE_t
┌─────────────────┐
│ 4. Feedback     │  差分 → 入力変換
│    フィードバック│  ├── 自然言語修正指示（プロンプト更新）
│                 │  └── パラメータ勾配（LoRA/ノード値更新）
└─────────────────┘
   │ 更新された入力
   ▼
┌─────────────────┐
│ 5. Guard        │  崩壊監視
│    分布モニタ    │  ├── FID drift
│                 │  ├── CLIP 散布度
│                 │  └── ループ回数カウンタ
└─────────────────┘
   │ OK / NG（閾値超過で停止・リセット）
   └──────────────────────┐
                          ▼
                    [次の反復 t+1]
```

## 2. 各層の詳細

### 2.1 Generator

- **対象モデル**: ローカル実行可能なモデル（Flux.1 Schnell / SD 1.5 / ComfyUI ワークフロー）
- **入力**: プロンプト、ネガティブプロンプト、CFG、ステップ数、シード、LoRA 重み
- **出力**: 画像ファイル + メタデータ JSON
- **制約**: VRAM 上限内での実行、1回生成の時間を計測

### 2.2 Evaluator（多軸評価）

評価は以下の4軸を基本とする。

| 軸 | 記号 | 自動評価 | 人間評価 |
|---|---|---|---|
| Quality | q | BRISQUE / NIMA 等 | 画質 5段階 |
| Style | s | CLIP style embed 距離 | スタイル一致 5段階 |
| Semantic | m | CLIP text-image 類似度 | 内容一致 5段階 |
| Preference | p | 個人RM スコア | 好み 5段階 |

- VLM critic（TEMPURA / Qwen2.5-VL）には「この画像はプロンプトにどれだけ従っているか」を問う。
- 人間評価は「生成意図に対する充足度」を測る。

### 2.3 Diff（差分抽出）

- 目標ベクトル `E_target` を設定（初期または段階的更新）。
- 各反復で `ΔE_t = E_target − E_t` を計算。
- 最も改善余地の大きい軸を優先フィードバック対象とする（greedy axis selection）。

### 2.4 Feedback（フィードバック変換）

**方式A: 自然言語修正指示**
```
ΔE_t（特に style・semantic の低下）
  → VLM critic に「どこが違うか」を叙述させる
  → 叙述文をプロンプトの付加・修正に使う
```

**方式B: パラメータ勾配**
```
ΔE_t（数値的な乖離）
  → CFG / ステップ数 / LoRA scale / サンプラーの slid
  → 簡易的なルールベースまたは軽量强化学习で更新
```

**方式C: LoRA 重み更新（継続学習）**
```
評価履歴から「良い生成」の条件を抽出
  → 少数サンプルで LoRA を継続更新（SLAO方式）
  → 忘却監視（過去概念テスト）
```

### 2.5 Guard（崩壊監視）

閾値を設定し、超過時にループを停止またはリセットする。

| 指標 | 閾値例 | 超過時の動作 |
|---|---|---|
| FID（前回からの増加） | ΔFID > 5.0 | 警告、 LoRA 更新抑制 |
| CLIP 散布度 | 分散が前回の 50% 以下に急減 | collapse 疑い、停止 |
| ループ回数 | t > 10 | 強制停止、中間最良を採用 |
| 同一画像類似度 | SSIM > 0.98（連続2回） | 停滞検出、パラメータランダム摂動 |

## 3. マニフェスト（実験記録）

各 run は以下を JSON で記録する。

```json
{
  "run_id": "EXP-EVAL-001-RUN-001",
  "rq": "RQ0",
  "group": "D",
  "loop_index": 3,
  "input": {
    "prompt": "...",
    "negative_prompt": "...",
    "cfg": 7.0,
    "steps": 20,
    "seed": 42,
    "lora": {...}
  },
  "output": {
    "image_path": "...",
    "generation_time_sec": 12.4
  },
  "evaluation": {
    "vlm_score": 0.72,
    "clip_similarity": 0.81,
    "human_score": 4,
    "preference_score": 0.65
  },
  "diff": {
    "target": [0.9, 0.9, 0.9, 0.8],
    "delta": [0.18, 0.05, 0.09, 0.15]
  },
  "feedback": {
    "type": "prompt_append",
    "content": "add more dramatic lighting"
  },
  "guard_status": "OK"
}
```

## 4. 実装スケジュール（仮）

| 段階 | 内容 | 出力 |
|---|---|---|
| 0 | 最小 generator（ComfyUI or SD）の導通 | 単発生成成功 |
| 1 | VLM critic の選定と結合 | 自動評価スコア取得 |
| 2 | プロンプトフィードバック（方式A） | 自然言語ループの動作 |
| 3 | パラメータフィードバック（方式B） | 数値ループの動作 |
| 4 | LoRA 継続更新（方式C） | 重み更新ループの動作 |
| 5 | Guard の閾値調整 | collapse の検出・回避実証 |

## 5. 依存

- `code/generate_frames.py` — 画像生成の baseline（ローカル SD 1.5）
- `code/prompts.json` — プロンプト preset
- `code/render_video.py` — 一連の評価履歴を動画化（オプション）
- 外部: ComfyUI / LM Studio / VLM critic model

## 6. 拡張戦略: 全要素コンテキスト（方式D詳細）

主RQの**方式D**（全要素コンテキスト群）では、反復ごとに以下5要素をテキスト入力に積み重ねる。

### 6.1 含める要素

| 要素 | 内容 | テキスト化方法 |
|:---|:---|:---|
| 生成プロンプト | 前回の positive / negative prompt | そのまま引用 |
| 生成画像 | 前回の出力画像 | パス記録（VLM入力時は画像そのもの） |
| パラメータ | CFG, steps, seed, width, height 等 | JSON から key=value 羅列 |
| オントロジ | STATE / DIFFERENCE / TRANSFORMATION / RELATION タグ | タグ列挙 |
| 細かな採点 | quality, composition, color, line, mood, semantic, preference | `key=score` 表記 |

### 6.2 プロンプト構造

```
[Target]
{目標記述}
Ontology: {目標タグ}

[History]
Run1: {前回プロンプト}
  p={cfg=7, steps=20, seed=42, w=512, h=512}
  scores=(qua=3, com=2, col=4, lin=3, moo=2)
  feedback: {評価者の自然言語指示}

[Directive from last evaluation]
{feedback文}

[Generate]
{feedbackを反映したプロンプト}
```

### 6.3 自動化

- `code/build_context.py` が context JSON → 上記テキストを自動生成
- `feedback_text` を `current_run.prompt` の prefix に連結し、次回生成へ反映
- 評価スコアはサブ軸ごとに記録し、未達成軸を `feedback_text` に優先的に含める

### 6.4 実験定義

詳細は `experiments/EXP-CTX-001.md` を参照。

| 項目 | 内容 |
|:---|:---|
| 実験ID | EXP-CTX-001 |
| 統制群 | A（単発）/ B（プロンプト継承）/ C（プロンプト＋総合採点）/ D（全要素コンテキスト） |
| 採点軸 | quality, composition, color, line, mood, semantic, preference（1〜5） |
| 目標例 | 夕暮れの廃工場に立つ少女。構図左寄り、色温度低、線力強、ムード寂寥 |
| 中止条件 | 全軸達成 / 10回 / 停滞3回 / 単調減少3回 |
| 評価指標 | 到達反復回数、最終スコア、スコア上昇率 |

---
*この設計は仮説であり、実験段階で改訂される。*
