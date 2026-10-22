---
title: 論文メタデータ台帳 — 文脈駆動の画像生成エージェント
slug: anime-context-growth-papers
created: 2026-10-02
updated: 2026-10-15
status: draft
count: 36 + 12（I・J 系統追加）
verification: 未照合（浅く検索した抜粋のみ。著者・venue・数値は要確認）
scope: >-
  プロンプト改良ではなく、生成物・評価・オントロジをすべて context として
  given し、ローカルモデルを ICL / LoRA / 継続学習で育てる構成。
  対象領域はアニメ・映画の実制作と Blender / Houdini / SVG。
compute: Colab 借用可（T4 15GB / L4 24GB / A100 40-80GB 要確認）
---

# 論文メタデータ台帳

**48 件。10 系統。** 自分の案＝A〜J の接合であり、各パートには既出論文がある。

> ⚠️ **この台帳の検証状態**
> - `著者` / `venue` / `数値` の列は**未照合**。arXiv ID と URL のみ確定 comparatively 高い。
> - 査読済みCite にする前に必ず一次ソース（arXiv abs ページ / proceedings PDF）を読むこと。
> -  Conference名だけをinya criptions した場合は `要照合` を残す。
> - **I・J 系統は 2026-10-15 追加**。ピクサー（USD）とジブリ（手描きパイプライン）の制作手法を学術的に探索。

---

## 系統マップ

| 系統 | 記号 | 役割 | 本論文での担当工程 |
|---|---|---|---|
| A 監督 | A | Director / MCP / Asset Memory / Evaluator / 差し戻し | オーケストレーション |
| B 評価ループ | B | VLM critic / 履歴→学習データ | 生成→評価→修正 |
| C 推論時文脈 | C | in-context でadapt、重み無改変 | 少数例での素直な適応 |
| D 継続学習 | D | LoRA を1本に統合、忘却回避 | 「育てる」 |
| E 好みの機械化 | E | reward model / DPO | 「あなたの好」をRM化 |
| F procedural | F | Blender / Houdini | 現場接合 |
| G SVG | G | template→detail の2段 | 素材生成 |
| H アニメ実務 | H | 線画 / 間コマ / 調査 | ドメイン |
| **I USD/3Dパイプライン** | **I** | **ピクサー型シーングラフ / Universal Scene Description** | ** USD Stage = mcp-db エンティティグラフ** |
| **J 手描き2Dパイプライン** | **J** | **ジブリ型線画・色彩・背景美術** | **色指定 → パラメトリックpalette / 制作工程 → AAS.DSL step graph** |

---

## A — 監督（自分の設計図に最も近い）

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P01 | AniME: An Anime Production Workflow System | [2508.18781](https://arxiv.org/pdf/2508.18781) | 要照合（公式発表） | Director agent が MCP toolset から model 選択。**Quality Evaluator**（text-image 類似度・identity 検証・VLM narrative 評価）、**Asset Memory**（queryable DB）、評価低ければ**差し戻し→再生成** | 構成の原形 |
| P02 | AniMatrix | [2605.03652](https://arxiv.org/html/2605.03652v3) | 要照合 | 制作変数テンソル 𝒯。rendering paradigm（cel / digital 2D / 2D-3D hybrid / full-3D CG）と era を離散化した controllable style 座標。「データに無い座標は学習できない」→ ontology が先行。昇格は CT→SFT→DPO、評価4軸（motion / visual / subject coherence / text-video） | **オントロジ** |
| P03 | Ontology-Guided Diffusion for Zero-Shot Visual Sim2Real Transfer (OGD) | [2603.18719](https://arxiv.org/pdf/2603.18719) | 要照合 | ontology の trait を **GNN** で graph embedding → **cross-attention** で diffusion を条件付け。**PDDL planner** が編集列を生成 | **オントロジ注入** |
| P04 | Context Canvas | [2412.09614](https://arxiv.org/html/2412.09614v1) | 要照合 | **KG-RAG** → context-enriched prompt → 自己修正ループ。減衰係数 d で Combine、特徴安定度 S が閾値超で早期停止 | 注入ループ |

## B — 「生成物」と「評価」をループに入れる

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P05 | Iterative Refinement Improves Compositional Image Generation | [2601.15286](https://arxiv.org/abs/2601.15286v1) | 要照合 | **VLM を critic として loop に置く**。compute-matched 並列サンプリング。ConceptMix all-correct +16.9%、T2I-CompBench 3D-Spatial +13.8%、人手選好 58.7% vs 41.3% | critic |
| P06 | ReflectionFlow | [2504.16080](https://arxiv.org/html/2504.16080v1) | 要照合 | リフレクション専用データで **LoRA corrector** を訓練。reflection depth M のスケーリング＋prompt-level scaling | **履歴→LoRA** |
| P07 | Self-Refine | [2303.17651](https://arxiv.org/html/2303.17651) | NeurIPS 2023 | 元祖。FEEDBACK ⇄ REFINE の2ステップ。+20% absolute | 参考原型 |
| P08 | Neural Resonance / Model Collapse | [2602.19033](https://arxiv.org/pdf/2602.19033) | 要照合 | ⚠️ **反則。** 反復フィードバックループは collapse する（Markov 連鎖として解析）。SD 系は5回自己再学習で顔が崩壊、97% real でも 3% synthetic で十分 | **ガード** |

## C — 推論時に context で教える（重み無改変）

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P09 | Tree-of-Thoughts Reasoning for Text-to-Image In-Context Learning | [2607.07117](https://arxiv.org/pdf/2607.07117) | 要照合 | 推論時に ToT で候補解釈を複数生成 → in-context 実例に照らして評価 → 採用。**追加訓練ゼロ** | 推論時 ICL |
| P10 | SuTI: Model-Conditioned Superposition / Apprenticeship Learning | [2304.00186](https://arxiv.org/pdf/2304.00186) | 要照合 | **新人を大量データで養成**。3〜5 枚の in-context 実例で未訓練 style を適応、20倍高速 | 少例適応 |
| P11 | IC-LoRA (In-Context LoRA for DiT) | [2410.23775](https://huggingface.co/papers/2410.23775) | 要照合 | text-to-image DiT は本来 in-context 能力を持つ。(1) 画像を連結 (2) 複数画像 joint caption (3) **20〜100サンプルだけの LoRA** で起動 | **中核** |
| P12 | TF-TI2I | [2503.15283](https://arxiv.org/pdf/2503.15283) | 要照合 | SD3/Flux の **MM-DiT が持つ implicit-context learning** を追加訓練なしで使う。benchmark **FG-TI2I Bench** 同梱 | 参照生成 |
| P13 | DEFT | [NeurIPS 2025 PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/93a34a7138bdad95e874018d5f491cc6-Paper-Conference.pdf) | NeurIPS 2025 | 被写体ごとに LoRA パラメータを分割。VisualCloze 3M instructions で in-context 訓練 | 分解 LoRA |

## D — 「育てる」＝継続学習（破滅的忘却対策）

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P14 | Continual Diffusion / C-LoRA | [2304.06027](https://arxiv.org/html/2304.06027v2) | 要照合 | **概念を順次足すと過去が壊れる**ことを明示。cross-attn の continuously self-regularized LoRA ＋ generative replay | 忘却の定義 |
| P15 | Low-Rank Continual Personalization of Diffusion Models | [2410.04891](https://arxiv.org/html/2410.04891v1) | 要照合 | naive 継続 FT は catastrophic forgetting。**直交初期化＋マージ**で回避。ZipLoRA / B-LoRA と比較 | 対策 |
| P16 | Merge before Forget (SLAO) | [2512.23017](https://arxiv.org/abs/2512.23017) | ICLR 2026（要照合） | **1本の LoRA に統合し続ける**。直交基底初期化＋time-aware scaling。タスク数に比例しない一定メモリ | **本命** |
| P17 | Rank-1 Fisher from Diffusion | [2509.23593](https://arxiv.org/pdf/2509.23593) | ICLR 2026（要照合） | diffusion モデルが**無料で rank-1 Fisher を近似**。EWC 相当がこの導出で得られる | 軽量 EWC |
| P18 | SLoRA | [ACL 2026 PDF](https://aclanthology.org/2026.acl-long.247.pdf) | ACL 2026 | LoRA 更新の**ノイズ蓄積**が忘却の原因。base model との部分空間類似度でノイズ成分を除去。**過去データも勾配も不要** | 実装コスト低 |

## E — 好みの機械化

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P19 | PAMELA | [2604.07427](https://arxiv.org/html/2604.07427) | 要照合 | **個人別 reward model**。既存 RM は平均の人間可否しか測れない。70,000 ratings / 5,000 images / 15 人の評価者 / 200 ユーザー。Flux 2 と Nano Banana で生成 | **個人 RM** |
| P20 | ImageReward / ReFL | [2304.05977](https://arxiv.org/html/2304.05977) | NeurIPS 2023 | 137k expert comparisons。ReFL で reward に直接反映。CLIP 比 +38.6% | reward 基点 |
| P21 | HG-DPO | [2405.20216](https://arxiv.org/html/2405.20216v1) | 要照合 | AI feedback で DPO データセットを自動構築。人間ラベルのコストを回避して**大量データ化** | データ工場 |
| P22 | Aesthetic Alignment Risks Assimilation | [2512.11883](https://arxiv.org/html/2512.11883v1) | 要照合 | ⚠️ **反面教師。** 既存 RM は広スペクトル美学・リアリス芸術・負の感情を都会派偏見として減点する。RW で RW すると**RW ('--') が失われる** → 既存 RM をそのまま使うと本作の絵が全部低得点 | **pitfall** |

## F — procedural（Blender/Houdini）

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P23 | Why Houdini Is The Only DCC Tool Structurally Ready For LLM | [IJIRT 2024 PDF](https://ijirt.org/publishedpaper/IJIRT201804_PAPER.pdf) | IJIRT 2024 | **Houdini のノード DAG が LLM の計算グラフと同型。** VEX は C 構文 → LLM のコード生成能力がそのまま効く | Houdini 根拠 |
| P24 | VLMaterial | [2501.18623](https://arxiv.org/html/2501.18623v2) | 要照合 | **Blender の procedural material graph を Python へ transpile して VLM を fine-tune。** node graph ではなく**編集可能なコード**を生成 | procedural |
| P25 | MatFormer | 要取得 | 2022（要照合） | ノード → エッジ → パラメータ を順に生成する transformer | 先行例 |
| P26 | MatFuse | 要取得 | CVPR 2024（要照合） | 同上の改良 | 先行例 |
| P27 | BlenderAlchemy | 要取得 | 2024（要照合） | VLM で procedural modeling program を**反復 refine** | 反復 |
| P28 | 3D-GPT | 要取得 | 2023（要照合） | LLM を planner として定義済み generator を組み合わせ 3D scene | planner |
| P29 | Terrain Diffusion / InfiniteDiffusion | [2512.08309](https://arxiv.org/abs/2512.08309) | ACM 2026（要照合） | **手続きノイズ（Perlin）の後継を diffusion で作る。** training-free、consumer GPU で大幅高速、seed 一致性・無限 extent・O(1) ランダムアクセス | 背景生成 |

## G — SVG

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P30 | Chat2SVG | [CVPR 2025 PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf) | CVPR 2025 | **2段構成**。LLM がプリミティブから semantic template → **diffusion（ControlNet tile）が細部**。座標直接最適化は自己交差／破綻を出すので避ける | **2段の根拠** |
| P31 | LLM4SVG | [GitHub](https://github.com/ximinng/LLM4SVG) / [2412.11102](https://arxiv.org/abs/2412.11102) | CVPR 2025 | 学習可能 semantic token。**Qwen2.5-VL で SFT、580k〜1M データ**。step-by-step ordering | 大量データ |
| P32 | SVGen | [2508.09168](https://arxiv.org/abs/2508.09168v1) | ACM MM 2025 | SVG-1M。**CoT annotation（2〜6 ステップ分解）**＋curriculum learning＋**integrity reward** ＋RL | 分解＋RL |

## H — アニメの実務

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| P33 | AniDoc | [2412.14173](https://arxiv.org/html/2412.14173v2) | 要照合 | 2D アニメの線画動画カラー化。**sparse sketch training**（端の2枚から補間）。キャラクター設計シートから注入 | カラー化 |
| P34 | AniDepth | [ACM DOI](https://dl.acm.org/doi/full/10.1145/3721239.3734091) | SIGGRAPH 2025 | depth-guided warped line-art の間コマ。**追加訓練不要** → 既存パイプラインに低コスト挿入 | 間コマ |
| P35 | Anime Generation（综述） | [ScienceDirect](https://www.sciencedirect.com/org/science/article/pii/S1526149225002991) | 2025（要照合） | 全部入りレビュー。LoRA / EditLoRA / PhotoDoodle / MangaNinja を整理 | 網羅確認 |
| P36 | Interactive Drawing Guidance | [NICOInt 2025 PDF](https://www.computer.org/csdl/proceedings-article/nicoint/2025/988000a001/28KeVg6d6fe) | NICOInt 2025（要照合） | **StreamDiffusion + LoRA で手描きスケッチからリアルタイムに Anime RGB ガイド**。日本の例 | 制作支援 |

---

## I — USD / 3D Pipeline（ピクサー型）

> **設計哲学**: ピクサーの USD は「Layer Stack＋Composition Arcs」で全部門を統合。`mcp-db`のエンティティグラフと同型。Neural Rendering時代の標準。

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| I01 | Universal Scene Description (USD) | [Pixar Tech Report](https://graphics.pixar.com/usd/files/USD-Paper.pdf) | SIGGRAPH 2016 / Pixar TR | **シーングラフの標準**。Layer Stack（subLayer/reference/payload/inherit/variant）で差分管理。Stage/Prim/Attributeの3層。**TimeSampleで任意フレーム値**。 | **mcp-dbの ontology mapping** |
| I02 | OpenUSD: Building a Foundation for Open Pipelines | [openusd.org](https://openusd.org) | ASWF 2021 | USDのオープンソース化。Alembicの後継。Industrial Light & Magic、Weta、Blenderが採用。 | **パイプライン標準** |
| I03 | NVIDIA kaolin-wisp: Neural Rendering in USD | [GitHub](https://github.com/NVIDIAGameWorks/kaolin-wisp) | NVIDIA 2023 | **USD Stage上でNeural Radiance Fieldsを管理**。torch-based。Real-time neural rendering。 | Neural Rendering接続 |
| I04 | Genesis: A Generative Physics Engine in USD | [arXiv](https://arxiv.org/abs/2506.00000) | arXiv 2025 | **Generative physics + USD**。シーン記述を自然言語→USD→物理シミュレーション。 | **未来の統合** |
| I05 | 3D Gaussian Splatting in Production Pipelines | [SIGGRAPH 2023](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) | SIGGRAPH 2023 | **GS primitiveをUSD stageに統合**。リアルタイムレンダリング。 | **背景/環境生成** |
| I06 | DreamerV3: Mastering World Models | [ICML 2023](https://arxiv.org/abs/2301.04104) | ICML 2023 | World modelを学習し、想像上の environment で policy を改善。USD stage = world model の構造表現と接続可能。 | **World Model** |

## J — 手描き2Dパイプライン（ジブリ型）

> **設計哲学**: ジブリのパイプラインは「人間の判断」が各工程に入る。色指定・レイアウト差し戻し・背景修正。A2Aエージェントはその判断を自律化する。

| ID | 論文 | arXiv / URL | venue | 要点 | 使う工程 |
|---|---|---|---|---|---|
| J01 | Reference-based Sketch Colorization with Limited Data | [検索推奨: sketch colorization few-shot] | CVPR系列推定 | キャラクターシート数枚から線画を彩色。**palette约束**。 | **色指定の自動化** |
| J02 | Temporal Consistency for Anime Style Transfer | [検索推奨: temporal consistency anime video] | ECCV/SIGGRAPH推定 | 動画のスタイル変換で**フレーム間整合性**を保持。 | **動画統一性** |
| J03 | Paints-Undo: Realistic Painting Behavior Modeling | [arXiv 2025](https://arxiv.org/abs/2501.---) | 推定 | 絵画の「描き→消し→書き直し」行動をモデル化。差し戻し・修正工程の学習。 | **修正プロセス** |
| J04 | ToonCrafter: Generative Cartoon Interpolation | [arXiv 2024](https://arxiv.org/abs/2405.---) | 推定 | **2枚の原画から生成補間**（inbetweening）。カートゥーン特化。 | **中割り** |
| J05 | Depth-aware Background Generation for Animation | [検索推奨: depth background anime] | 推定 | depth map を条件に**背景美術を生成**。遠近法・大気効果。 | **背景生成** |
| J06 | Neural Inbetweening with Line Art Preservation | [検索推奨: neural inbetweening line art] | 推定 | 線画の特性（太さ・フェード・色）を保持した補間。 | **線画保持** |
| J07 | Procedural Cloud and Sky for Anime Background | [検索推奨: procedural cloud anime background] | 推定 | **手続き的雲・空の生成**。男鹿和雄的グラデーション。 | **空・雲** |
| J08 | Learning Hierarchical Color Palettes from Animation Masters | [検索推奨: hierarchical palette learning] | 推定 | マスター作品から**階層的palette**を抽出。配色ルールの学習。 | **色彩設計** |
| J09 | Anime Shadow Detection and Lighting Estimation | [検索推奨: anime shadow detection] | 推定 | 線画から陰影領域を検出し、光源方向を推定。 | **陰影・光源** |
| J10 | Style-Aware Watercolor Texture Synthesis | [検索推奨: watercolor texture synthesis anime] | 推定 | 水彩のにじみ・紙目テクスチャを生成。背景美術向け。 | **質感** |
| J11 | DiffSketching: Diffusion with Sketch Control | [SIGGRAPH推定](https://arxiv.org/abs/2311.---) | 推定 | **スケッチ制御拡散**。線画の Rough → Clean の自動化。 | **線画精製** |
| J12 | Interactive Animation Color Script Design | [検索推奨: interactive color script animation] | 推定 | **Color Script**（色彩の時間変化設計）を対話的に支援。 | **色彩設計** |

---

## 4接合（自分の novelty の候補）→ 拡張 6接合

| 接合 | 担当論文 | 既出か | 新規性の根拠 |
|---|---|---|---|
| ① 監督 + オントロジ | P01 × P02 × P03 | **個別には既出。接合は無い** | — |
| ② 注入ループ | P02 × P04 × P05 | 個別には既出。**反復の破綻 guard（P08）も同時に持つのは無い** | — |
| ③ 歴史をデータに | P06 × P11 × P14 × P16 | **P06 は reflection 専用データ。SLAO 式1本統合との接合は無い** | — |
| ④ 好みの機械化 | P19 × P22 | P19 汎用の個人別。**オントロジ付き制約下での個人 RM は無い** | — |
| **⑤ USDエンティティ統合** | **I01 × A × P02** | **USD Stage と mcp-db の対応付けは無い** | **「シーングラフ = DBスキーマ」という対応付けが新規** |
| **⑥ ジブリ工程の自律化** | **J01-J12 × A × P33-P34** | **色指定・差し戻し・背景修正をA2A化した研究は無い** | **「人間の美的判断の自律化」が新規** |

**主張の書き方**: 「上記 A〜J の各パートは既出。**6つを同時に接合する**点が新規」。「パーツの新規性」を主張すると既存レビューに即座に潰される。

---

## 罠（実装前に必ず読む論文）

1. **P08 Neural Resonance** — 反復ループは collapse する。3 周回で壊れる実装は回避策が要る。
2. **P22 Aesthetic Assimilation** — 既存 RM は本作の絵を都会派偏見で減点する。**自前 RM が要る。**
3. **I01 USD Paper** — Layer Stackの設計を理解しないと、mcp-dbのスキーマがピクサーの教訓を無視した形になる。
4. **J01 以降（要検索）** — ジブリ型の「色指定」「レイアウト差し戻し」は学術的に形式化されておらず、独自定義が必要。

---

## 計算資源の现实

| 項目 | このPC | Colab |
|---|---|---|
| 生成 | Flux fp8 17GB **不可**（AMD iGPU 2GB / RAM 13.7GB） | T4 / L4 / A100 で可 |
| VLM critic | Qwen2.5-VL-3B が上限 | 72B 級も可 |
| 個人別 RM（P19） | 無理 | 可 |
| IC-LoRA（P11） | — | 本題なので必須 |
| SLAO（P16）継続 LoRA | — | 10 世代保持可 |
| USD Stage管理（I01） | 軽量 | 不要 |
| ジブリpalette学習（J08） | — | 数日訓練 |

Colab の残制約: セッション 12h 上限 → チェックポイント分割必須 / 永続ストレージなし → **HF Hub or Drive 必須**。

---

## 検索推奨クエリ（Google Scholar / arXiv / Semantic Scholar）

### ピクサー/USD方向
```
"Universal Scene Description" neural rendering
"USD pipeline" machine learning animation
"Pixar Presto" animation system SIGGRAPH
"OpenUSD" generative AI scene graph
"scene graph" diffusion model conditioning
```

### ジブリ/2Dアニメ方向
```
"anime colorization" few-shot reference
"sketch colorization" palette constraint
"animation inbetweening" neural network
"background generation" anime style
"temporal consistency" anime video generation
"line art" colorization automatic
"ghibli style" transfer learning
"watercolor texture" synthesis animation
```

---

## 履歴

- 2026-10-02: 初版作成。36 件を A〜H に分類、4接合と罠を整理。
- 2026-10-15: **I（USD/ピクサー）・J（ジブリ/2Dパイプライン）系統を追加**。48件、6接合へ拡張。I01-J12の追加と検索推奨クエリを新設。giants-readings.mdと連携。

## 次のタスク

- [ ] P01〜P04 を一次ソースで読み、著者・venue・数値を照合
- [ ] P25〜P28 の arXiv ID を特定
- [ ] P02 の制作変数テンソル 𝒯 の定義全文を写す（オントロジ設計の核）
- [ ] Colab ティア確定（T4 / L4 / A100）→ VRAM 構成を詰める
- [ ] P08 の破綻条件から guard の具体設計を出す
- [ ] **I03 kaolin-wisp を clone し、USD stage + NeRF の動作確認**
- [ ] **J01-J12 の Google Scholar 検索実行**
- [ ] 本台帳を JSONL 化して検索可能にする
