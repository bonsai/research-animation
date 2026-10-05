# Literature Map — 生成画像の評価とフィードバック

本テーマに関連する論文群の索引。

詳細なメタデータ台帳は `PAPERS.md`（48件、旧台帳）を参照。ただし `PAPERS.md` は旧研究（文脈駆動Growing画像生成）のものであり、系統 **F〜J**（procedural / SVG / アニメ実務 / USD / 手描き2D）は本テーマから外れる。

## 関連系統と論文

### A — 監督・オーケストレーション（参照系統）
Director agent による model 選択、Quality Evaluator、Asset Memory、差し戻しループの先行例。

| ID | 論文 | 本テーマでの役割 |
|---|---|---|
| P01 | AniME: Anime Production Workflow System | 評価→差し戻しループの構成原型 |
| P02 | AniMatrix | 制作変数テンソル・オントロジー制御 |
| P03 | OGD (Ontology-Guided Diffusion) | ontology から diffusion 条件付け |
| P04 | Context Canvas | KG-RAG → context-enriched prompt → 自己修正ループ |

### B — 評価ループ（**本テーマの核**）
VLM critic による反復評価、履歴学習、リフレクション。

| ID | 論文 | 本テーマでの役割 |
|---|---|---|
| P05 | Iterative Refinement Improves Compositional Image Generation | **VLM critic ループ**。compute-matched 並列サンプリング、人手選好 58.7% |
| P06 | ReflectionFlow | LoRA corrector をリフレクション専用データで訓練 |
| P07 | Self-Refine | FEEDBACK ⇄ REFINE の2ステップ元祖 |
| P08 | Neural Resonance / Model Collapse | ⚠️ 反復ループの collapse 警告（SD系5回で崩壊） |

### C — 推論時文脈（重み無改変の対照）
ICL による適応がどこまで効くか。RQ0 の対照群 B に相当。

| ID | 論文 | 本テーマでの役割 |
|---|---|---|
| P09 | Tree-of-Thoughts for T2I In-Context Learning | 推論時 ICL、追加訓練ゼロ |
| P10 | SuTI | 少例適応、20倍高速 |
| P11 | IC-LoRA | **DiT の in-context 能力と少量 LoRA** |
| P12 | TF-TI2I | implicit context learning、追加訓練なし |
| P13 | DEFT | 被写体ごとの LoRA パラメータ分割 |

### D — 継続学習・LoRA統合（**本テーマの核**）
継続的な重み更新と忘却対策。

| ID | 論文 | 本テーマでの役割 |
|---|---|---|
| P14 | Continual Diffusion / C-LoRA | 概念順次追加での忘却定義 |
| P15 | Low-Rank Continual Personalization | 直交初期化＋マージで忘却回避 |
| P16 | Merge before Forget (SLAO) | **1本LoRA統合**。time-aware scaling、一定メモリ |
| P17 | Rank-1 Fisher from Diffusion | 無料で EWC 相当が得られる |
| P18 | SLoRA | ノイズ蓄積除去。過去データ・勾配不要 |

### E — 好みの機械化（個人嗜好・Reward Model）
個人別 reward model と汎用 RM の違い、美学の偏見。

| ID | 論文 | 本テーマでの役割 |
|---|---|---|
| P19 | PAMELA | **個人別 reward model**。70,000 ratings / 5,000 images / 15評価者 |
| P20 | ImageReward / ReFL | reward 基点（137k comparisons） |
| P21 | HG-DPO | AI feedback で DPO データセット自動構築 |
| P22 | Aesthetic Alignment Risks Assimilation | ⚠️ 既存RMの偏見。個人RMの必要性を示唆 |

## サマリー一覧

`summaries/` 以下に個別サマリーあり。

| ファイル | 内容 |
|---|---|
| `P05-iterative-refinement.md` | 反復評価ループの構成 |
| `P08-neural-resonance.md` | collapse の検出と警告 |
| `P11-ic-lora.md` | in-context LoRA |
| `P16-slao.md` | 1本LoRA統合（SLAO） |
| `P19-pamela.md` | 個人別 reward model |
| `P22-aesthetic-alignment.md` | RM の美学偏見 |
| `P30-chat2svg.md` | SVG 生成（本テーマの直接対象外） |
| `I01-usd-pipeline.md` | USD パイプライン（対象外） |
| `J01-ghibli-pipeline.md` | ジブリ型パイプライン（対象外） |
| `4koma-manuscript.md` | 4コマ原稿構造（対象外） |
| `P01-anime.md` | AniME 全体構成 |

---

## スコープ外の系統（archive参照）

- **F** procedural（Blender/Houdini）
- **G** SVG（template→detail）
- **H** アニメ実務（線画・間コマ）
- **I** USD/3Dパイプライン（ピクサー型）
- **J** 手描き2Dパイプライン（ジブリ型）

これらは morphing・animation interface・制作工程として `archive/` に保存。
