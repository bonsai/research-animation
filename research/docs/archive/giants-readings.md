# 巨人の肩 — 成長を促す論文読書計画

> 「巨人の肩に乗って、巨人になりたい」— Isaac Newton (1675) より
> *If I have seen further, it is by standing on the shoulders of giants.*

## 前言

このファイルは 3 つの役割を持つ。

1. **肩に乗っている巨人の確認** — 既存 `PAPERS.md` の 36 件（A〜H 8 系統）を整理
2. **他分野の巨人の追加** — 統計・数学・機械学習・ループの基礎論文
3. **発達を促す読書課題** — 4 フェーズの自己鍛錬プラン（到達点付き）

**検索制約の注記**: 論文データベース（arXiv API / Semantic Scholar / Google Scholar）への直接アクセス unavailable なため、**既知の基礎論文を curated しました**。著者・venue・数値は `PAPERS.md` に従い **要照合** 扱いとし、一次ソース（arXiv abs / proceedings PDF）で確認してください。

---

## 0. 今、既に肩に乗っている巨人（既存 36 件の整理）

`PAPERS.md` の 8 系統を卒制との接点付きで再整理。それぞれの「巨人からの継承」と「自分が足すべきもの」を明確にする。

### A 監督（オーケストレーション）
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P01 AniME | Director agent / Quality Evaluator / Asset Memory / 差し戻し | 卒制固有のツール契約（MCP）に実装 |
| P02 AniMatrix | 制作変数テンソル 𝒯 / 昇格 CT→SFT→DPO | **ontology が先行** — 座標系設計 |
| P03 OGD | ontology trait → GNN embedding → cross-attention | P02 の 𝒯 と結合 |
| P04 Context Canvas | KG-RAG → 自己修正ループ / 早期停止 | ループの収束条件 |

### B 評価ループ（生成→評価→修正）
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P05 Iterative Refinement | VLM を critic として loop へ | compute-matched 並列サンプリングの実装 |
| P06 ReflectionFlow | reflection 専用データで LoRA corrector | **履歴→学習データ** のパイプ |
| P07 Self-Refine | FEEDBACK ⇄ REFINE の原型 | 参考 |
| P08 Neural Resonance | ⚠️ **collapse の解析** | **guard の設計** — これが novelty の要 |

### C 推論時文脈（重み無改変）
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P09 Tree-of-Thoughts | ToT で候補解釈を複数生成 → 評価 | 卒制適用 |
| P10 SuTI | 3〜5 枚で未訓練 style を適応（20倍高速） | 少例適応のフック |
| P11 IC-LoRA | 20〜100 サンプルだけの LoRA で起動 | **中核** |
| P12 TF-TI2I | MM-DiT の implicit-context を無訓練利用 | 参照生成 |
| P13 DEFT | 被写体別 LoRA 分割 | 分解 LoRA |

### D 継続学習（育てる・忘却回避）
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P14 Continual Diffusion | 順次追加で過去が壊れる | 忘却の定義 |
| P15 C-LoRA | 直交初期化＋マージで回避 | 対策 |
| P16 SLAO | **1 本の LoRA に統合し続ける** | **本命** |
| P17 Rank-1 Fisher | diffusion が無料で Fisher を近似 | 軽量 EWC |
| P18 SLoRA | ノイズ蓄積を除去（過去不要） | コスト低減 |

### E 好みの機械化
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P19 PAMELA | 個人別 reward model（5,000 images/5,000 ratings） | 個人 RM |
| P20 ImageReward | 137k 専門家比較 / CLIP 比 +38.6% | reward 基点 |
| P21 HG-DPO | AI feedback で DPO  datasets を自動構築 | データ工場 |
| P22 Aesthetic Assimilation | ⚠️ **既存 RM は都会派偏見で減点** | **自前 RM が要る** |

### F procedural（Blender/Houdini）
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P23 Houdini は LLM に最適 | ノード DAG が計算グラフと同型 | 設計根拠 |
| P24 VLMaterial | procedural graph → Python コード | コード生成 |
| P25/P26 MatFormer/MatFuse | ノード→エッジ→パラメータ | 先行例 |
| P27 BlenderAlchemy | procedural modeling を反復 refine | 反復 |
| P28 3D-GPT | LLM を planner として generator を組み合わせ | planner |
| P29 Terrain Diffusion | 手続きノイズ（Perlin）の後継を diffusion | 背景生成 |

### G SVG（2 段生成）
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P30 Chat2SVG | LLM が template → diffusion が細部 | **2 段の根拠** |
| P31 LLM4SVG | 学習可能 semantic token（Qwen2.5-VL SFT） | 大量データ |
| P32 SVGen | CoT 分解＋curriculum＋integrity reward | 分解＋RL |

### H アニメ実務
| 論文 | 継承 | あなたが足すこと |
|---|---|---|
| P33 AniDoc | 端の 2 枚から補間（sparse sketch training） | カラー化 |
| P34 AniDepth | depth-guided warped line-art（訓練不要） | 間コマ |
| P35 Anime Generation（综述） | LoRA/EditLoRA/PhotoDoodle/MangaNinja 整理 | 網羅確認 |
| P36 Interactive Drawing Guidance | StreamDiffusion+LoRA で手描きガイド | 制作支援 |

### 既存の 4 接合（PAPERS.md から再確認）
1. **監督 + オントロジ** (P01×P02×P03) — 個別は既出、接合は無い
2. **注入ループ** (P02×P04×P05) — **P08 の guard を同時に持つのは無い**
3. **歴史をデータに** (P06×P11×P14×P16) — SLAO 式 1 本統合との接合は無い
4. **好みの機械化** (P19×P22) — オントロジ付き制約下での個人 RM は無い

---

## 1. 他分野の巨人（統計・数学・機械学習・ループ）

### 1.1 統計学 — 不確実性を定量化する基礎

| 文献 | 型 | 卒制への接点 | 照合 |
|---|---|---|---|
| Bishop, *Pattern Recognition and Machine Learning* (2006) | 教科書 | 尤度・ベイズ推論・EM アルゴリズム | venue 確定 |
| Hastie/Tibshirani/Friedman, *The Elements of Statistical Learning* (2nd ed., 2009) | 教科書 | 正則化・モデル選択・誤差分解 | venue 確定 |
| Gelman et al., *Bayesian Data Analysis* (3rd ed., 2013) | 教科書 | 事後分布・MCMC | venue 確定 |
| Rasmussen/Williams, *Gaussian Processes for Machine Learning* (2006) | 教科書 | 不確実性付き回帰 | P19 RM の不確実性定量化 |
| Breiman, "Statistical Modeling: The Two Cultures" (Statistical Science, 2001) | 論文 | 予測モデル vs 因果モデルの対比 | arXiv 要照合 |
| Tibshirani, "Regression Shrinkage and Selection via the Lasso" (1996) | 論文 | Lasso・正則化 | **LoRA の低ランク近似の数学的正当性** |
| Wainwright, *High-Dimensional Statistics* (2019) | 教科書 | 高次元統計 | 大規模モデルの解析 |

### 1.2 数学 — 計算の土台

| 文献 | 型 | 卒制への接点 | 照合 |
|---|---|---|---|
| Shannon, "A Mathematical Theory of Communication" (Bell System Tech J, 1948) | 論文 | 情報理論・エントロピー | 評価指標の情報量解釈 |
| Kolmogorov, *Foundations of the Theory of Probability* (1933) | 書籍 | 確率の公理系 | ベイズ・拡散の基礎 |
| Boyd/Vandenberghe, *Convex Optimization* (2004) | 教科書 | 凸最適化（無料 PDF あり） | 学習の収束解析 |
| Cormen et al., *Introduction to Algorithms* (CLRS) | 教科書 | 計算量 | 各工程の O( ) 見積もり |
| Axler, *Linear Algebra Done Right* (2015) | 教科書 | 線形代数 | LoRA の特異値分解的構造 |
| Billingsley, *Probability and Measure* (1995) | 教科書 | 測度論的確率論 | 確率過程の厳密化 |
| Dijkstra, "On the Nature of Mathematical Writing" (1977) | 論文 | 証明の美しさ | 論文の書き方 |

### 1.3 機械学習（本流）

| 論文 | venue/year | arXiv | 卒制への接点 |
|---|---|---|---|
| LeCun/Bengio/Hinton, "Deep Learning" | Nature 521 (2015) | arXiv:1503.02531 | 本流の全体像 |
| Krizhevsky et al., "AlexNet" | NIPS 2012 | arXiv:1207.0580 | CNN 出発点 |
| Goodfellow et al., "GANs" | NIPS 2014 | arXiv:1406.2661 | 生成モデルの双璧 |
| Kingma/Welling, "VAE" | ICLR 2014 | arXiv:1312.6114 | 潜在空間 |
| **Vaswani et al., "Attention Is All You Need"** | **NeurIPS 2017** | **arXiv:1706.03762** | **P11/P12 の土台（Transformer/MMDiT）** |
| **Ho et al., "DDPM"** | **ICML 2020** | **arXiv:2006.11239** | **P04-P06 全般（拡散の数式）** |
| Dhariwal/Nichol, "Diffusion beats GANs" | NeurIPS 2021 | arXiv:2105.05233 | 拡散の性能 |
| Rombach et al., "Latent Diffusion (Stable Diffusion)" | CVPR 2022 | arXiv:2112.10752 | 本業の直接の土台 |
| Peebles/Xie, "Scalable Diffusion Models with Transformers (DiT)" | ICCV 2023 | arXiv:2212.09748 | P12 の土台 |
| Lipman et al., "Flow Matching" | NeurIPS 2022 | arXiv:2210.02747 | 拡散の別アプローチ |
| Devlin et al., "BERT" | NAACL 2019 | arXiv:1810.04805 | コンテキスト理解 |
| **Brown et al., "Language Models are Few-Shot Learners"** | **NeurIPS 2020** | **arXiv:2005.14165** | **P09/P10/P12（in-context の根本）** |
| Wei et al., "Chain of Thought" | ICLR 2022 | arXiv:2201.11903 | ToT の元 |
| Wang et al., "Self-Consistency" | ICLR 2023 | arXiv:2203.17995 | 多数決投票 |
| Mnih et al., "Deep Q Network" | Nature 2015 | arXiv:1312.5602 | RL 出発点 |
| Silver et al., "AlphaGo" | Nature 2016 | arXiv:1611.01224 | 計画＋学習 |
| Schulman et al., "PPO" | arXiv:2017.06347 | arXiv:1707.06347 | RL の標準 |
| Haarnoja et al., "SAC" | NeurIPS 2018 | arXiv:1812.05905 | 連続行動 |
| Lester et al., "The Power of Scale for Parameter-Efficient Prompt Tuning" | EMNLP 2021 | **arXiv:2106.09685** | **P11/P16 の隣接（LoRA）** |
| Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed., 2018) | 教科書 | - | RL の圣经 |

### 1.4 ループ — 反復・継続・学習するシステム

| 論文 | venue/year | arXiv | 卒制への接点 |
|---|---|---|---|
| **Kirkpatrick et al., "EWC: Overcoming catastrophic forgetting"** | **PNAS 2017** | **arXiv:1612.00796** | **D システム全体（忘却の定量化）** |
| Lopez-Paz/Ranzato, "GEM" | NeurIPS 2017 | arXiv:1703.03953 | グラディエント競合の回避 |
| Hassabis et al., "Experience Replay" | NIPS 2017 | 要照合 | **B システムの履歴→データ** |
| Bengio et al., "Curriculum Learning" | IJCNN 2009 | arXiv:0906.0628 | 学習順序の設計 |
| Graves, "Learning to Learn" | ICML 2013 | arXiv:1306.0661 | メタ学習の原点 |
| Andrychowicz et al., "Optimization as a Model for Few-Shot" | ICLR 2016 | arXiv:1610.03483 | メタ学習 |
| Schaul et al., "Prioritized Experience Replay" | ICLR 2016 | arXiv:1511.05952 | 優先度付きループ |
| Lin, "Self-Improving Reactive Agents" | Machine Learning 1993 | 要照合 | **経験再生の原点（ループの原型）** |
| Shinn et al., "Reflexion" | NeurIPS 2024 | arXiv:2303.11174 | 言語エージェントの自己修正 |
| Yao et al., "Tree of Thoughts" | arXiv:2023.05 | **arXiv:2305.10601** | P09 との接点（ToT） |
| Park et al., "Generative Agents" | CHI 2023 | arXiv:2304.03442 | エージェントのメモリ/自己反省 |
| Shen et al., "HuggingGPT" | ICLR 2024 | arXiv:2303.17580 | エージェント×モデル選定 |
| Liu et al., "Tool Learning with Foundation Models" | arXiv:2023.07 | **arXiv:2307.16789** | **A システム（MCP ツール選定）** |
| Wang et al., "Few-Shot Learning Survey" | IEEE TPAMI 2020 | arXiv:2010.03591 | C システムの網羅 |
| Rusu et al., "Progress & Compress" | arXiv:2018.10 | **arXiv:1810.02266** | **D システム（継続学習の代表手法）** |
| Settles, "Active Learning Survey" | UW TR 1648 (2009) | - | ラベル効率 |
| Schmidhuber, "Learning to Learn by Self-Critique" | 1987 | 要照合 | **P08 collapse の系譜（自己評価の歴史）** |

#### 統計・数学との接合点（D システムのために）

| 他分野の巨人 | 卒制 D（継続学習）への接点 |
|---|---|
| EWC (Kirkpatrick 2017) | Fisher 情報で「重要な重み」を特定 → P17(P18) の rank-1 Fisher と同一の発想 |
| Lasso (Tibshirani 1996) | 正則化＝スパース化 → LoRA の低ランク更新との親和性 |
|凸最適化 (Boyd) | 忘却なしの更新が凸問題として定式化できるか検討 |
| 情報理論 (Shannon 1948) | 忘却＝情報漏洩として定量化（エントロピー増） |

#### ループとの接合点（B システムのために）

| 他分野の巨人 | 卒制 B（評価ループ）への接点 |
|---|---|
| Experience Replay (Lin 1993) | 生成履歴を replay buffer として保存 → P06 の「履歴→学習データ」 |
| Curriculum Learning (Bengio 2009) | 評価ループ内の難易度制御 → collapse 前の停止条件 |
| Reflexion (Shinn 2024) | 言語ベースの自己修正 → P05 の VLM critic との親和性 |
| ToT (Yao 2023) | 複数候補の評価 → P09 の ToT-ICL と共通設計 |
| Self-Refine (Madaan 2023, 既に P07) | 元祖の FEEDBACK⇄REFINE |

---

### 1.5 制作スタジオの巨人（ピクサー・ジブリ）— パイプライン設計の実務知

アカデミックな論文だけでは見えない「現場のパイプライン設計」がある。ピクサーとジブリは対極的なアプローチだが、両方から学ぶと機械化すべき「判断」の輪郭が見える。

#### ピクサー — 工学主義のパイプライン

| 要素 | ピクサーの手法 | 学術的対応 | 卒制への接点 |
|---|---|---|---|
| **USD Stage** | 部門横断の単一シーングラフ | I01 (USD Paper) | `mcp-db`のエンティティグラフ設計 |
| **Layer Stack** | 差分合成で編集履歴管理 | Git-like versioning | `asset.version` + `workflow.step_index` |
| **Variant Set** | 同一アセットの複数表現 | 条件付き生成 | LoRA条件切り替え |
| **Task Graph (Tractor)** | 依存関係グラフで分散レンダリング | DAG execution | AAS.DSLのdependency graph |
| **Presto** | アニメーター向けリアルタイムビュー | Interactive generation | StreamDiffusion / LCM |
| **Renderman** | 物理ベースレンダリング | PBR theory | 背景の photorealistic / anime 切り替え |
| **Dailies Review** | 毎日の制作物レビュー | Human-in-the-loop | `mcp-ojev`の評価ループ |

#### ジブリ — 芸術主義のパイプライン

| 要素 | ジブリの手法 | 学術的対応 | 卒制への接点 |
|---|---|---|---|
| **絵コンテ** | 演出の全貌を1枚の絵で設計 | Storyboard generation | `mcp-storyboard` |
| **レイアウト** | 背景とキャラの位置関係 | Spatial composition | `mcp-2d-pipeline.layout` |
| **原画** | 動きの"設計図" | Keyframe generation | `mcp-comfyui` + ControlNet pose |
| **動画（中割り）** | 原画間を手動補間 | Inbetweening (P34) | `mcp-2d-pipeline.interpolate` |
| **色指定** | キャラシートからpalette決定 | Palette recommendation (J08) | `mcp-lms.auto_color` |
| **仕上げ** | 線画の内側を塗り分け | Colorization (P33) | `mcp-2d-pipeline.color` |
| **背景美術** | 水彩・油彩による環境構築 | Background generation (J05) | `mcp-2d-pipeline.background` |
| **撮影効果** | コンポジット・ゴッドレイ | Post-processing / effects | `mcp-2d-pipeline.composite` |
| **差し戻し** | 演出判断で工程を巻き戻し | Human-in-the-loop feedback | AAS.DSLの`IfNode` + feedback edge |

**重要な洞察**: ピクサーは「計算グラフの最適化」、ジブリは「人間の判断の最適化」。A2Aシステムは両方を統合する — USD-likeなエンティティ管理 + ジブリ-likeな美的判断の自律化。

#### 2つのパイプラインから学ぶべき「機械化できないもの」

1. **演出判断（direction）**: 「このカットはキャラではなく風を主役にする」→ オントロジのpriority付け
2. **色の"空気感"**: 数字では測れない温度・湿度の感覚 → PAMELA (P19) の個人別RM化
3. **リズム・間**: アクションとカットのタイミング → 未解決。動画生成のtemporal controlが近い
4. **意外性**: 予期せぬ構図の発見 → 生成モデルの「創造性」とは異なる。能動的探索（active learning）の領域

---

## 2. 読書計画（5 フェーズの自己鍛錬）

> 方針: 読むだけでは「肩に乗っただけ」。**課題（アウトプット）を伴って「巨人になる」**。

### Phase A — 基礎固め（2 週間）｜「背を伸ばす」

**目標**: 卒制で使う確率・統計・計算量を自分で説明できる

**読む**（優先度順）:
1. Bishop ch.1-3（ベイズ・確率・線形代数の復習）
2. CLRS ch.1-2（計算量・漸近表現）
3. Shannon (1948) 全文（情報理論の原点）
4. Kolmogorov (1933) 序論（確率の公理系）

**課題（到達点）**:
- A1: 「卒制で使う確率用語（尤度、事後分布、期待値、分散、エントロピー）を自分で 1 頁に定義し、それぞれの数式と直感的意味を記す」
- A2: 「卒制の各工程（生成・評価・修正・LoRA 更新）の計算量 O( ) を見積もり、ボトルネックを 1 つ指摘する」

**成果物**: `research/read-log/phase-a-notes.md`

### Phase B — 本流の理解（3 週間）｜「巨人の足元を見る」

**目標**: あなたの生成システム全体を支える数式を全て紙に書き下ろせる

**読む**（優先度順）:
1. Vaswani (2017) — Attention / Transformer（P11/P12 の土台）
2. Ho (2020) DDPM — 拡散の数式全体
3. Rombach (2022) Latent Diffusion — 実装に直結
4. Brown (2020) Few-shot LMs — in-context の根本（C システム）
5. Kirkpatrick (2017) EWC — 忘却の定量化（D システム）
6. Lester (2021) LoRA / Hu (2021) — 低ランク適応の数学

**課題（到達点）**:
- B1: 「DDPM の数式をゼロから紙に書き下ろし、diffusion coefficient の物理的意味を 3 行で説明する」
- B2: 「LoRA の低ランク近似がなぜメモリ節約になるかを特異値分解の図解付きで説明する（SVD と rank-r 更新）」
- B3: 「EWC の Fisher 情報と、卒制 P17(P18) の rank-1 Fisher 近似の関係を 1 頁で対比し、どちらが卒制に適か判断する」

**成果物**: `research/read-log/phase-b-equations.pdf`（手書きスキャン）

### Phase C — ループの設計（2 週間）｜「巨人を超える」

**目標**: collapse しない評価ループを再設計できる

**読む**（優先度順）:
1. Lin (1993) Experience Replay — ループの原型
2. Bengio (2009) Curriculum Learning — 順序の科学
3. Graves (2013) Learning to Learn — メタ学習
4. Schaul (2016) PER — 優先度付きサンプリング
5. Shinn (2024) Reflexion — 言語自己修正
6. P08 Neural Resonance — **collapse の正体（必ず読む）**

**課題（到達点）**:
- C1: 「既存 B システム（P05-P08）の評価ループを、collapse しないよう EWC/ER/Curriculum の視点で再設計する設計書（1-2 頁）」
- C2: 「ループの停止条件を 3 つ定める（最大周回数、評価の飽和、collapse 検知）」
- C3: 「P08 の Markov 連鎖解析を自分のループに適用し、『何周でどれくらい劣化する』を推定式で書く」

**成果物**: `project/anijev/docs/04-design-loop.md`

### Phase D — 既存 36 件との接合（継続）｜「巨人のネットワークを描く」

**目標**: 他分野巨人 × 既存 36 件の接合表を全て埋める

**読む**: `PAPERS.md` の A〜H を系統別に対照（Phase A〜C で読んだ他分野論文を軸に）

**課題（到達点）**:
- D1: 「接合表を埋める。例：P16 SLAO × EWC × 忘却の数学」「P08 collapse × Markov 連鎖解析」「P11 IC-LoRA × Few-shot Survey」「A システム × Tool Learning (arXiv:2307.16789)」「B システム × Reflexion」
- D2: 「自分の novelty の 4 接合（PAPERS.md）を他分野巨人で裏付け、各接合がなぜ既出と競合しないかを 1 文ずつ書く」
- D3: 「PAPERS.md を JSONL 化して検索可能にする（既存タスク）」

**成果物**: `research/giants-connectivity.md`

### Phase E — スタジオ実務の理解（2 週間）｜「現場の空気を知る」

**目標**: ピクサーとジブリのパイプラインから、機械化すべき「判断」と残すべき「人間性」を区別できる

**読む**（優先度順）:
1. Pixar USD Paper (I01) — Layer Stackの設計哲学
2. 「スタジオジブリの現場」（NHK 2005）— 制作フローの全体像
3. 宮崎駿『出発点』— 絵コンテの考え方（演出判断の根拠）
4. 宮崎駿『折り返し点』— 色彩と光の哲学
5. "The Pixar Touch" (David A. Price, 2008) — 企業史と技術投資
6. "Creativity, Inc." (Ed Catmull, 2014) — ピクサーのマネジメント哲学

**課題（到達点）**:
- E1: 「ピクサーのUSD Layer Stackと、卒制 `mcp-db` のテーブル設計を対応付けたマッピング表を作成。どのテーブルが Prim/Attribute/Relationship に相当するか」
- E2: 「ジブリの『色指定』を機械化する際に、何が容易（palette制約）で何が困難（"空気感"の数値化）かを1ページで整理」
- E3: 「AAS.DSLのstep graphと、ジブリの制作工程（絵コンテ→レイアウト→原画→動画→仕上げ）を対応させ、どの工程に`mcp-ojev`の評価を入れるか設計」
- E4: 「『機械化できないもの』のリストを5つ挙げ、それぞれをA2Aシステムではどう扱うか（人間介入ポイントとして定義）」

**成果物**: `research/studio-pipeline-mapping.md`

---

## 3. 読書ノートテンプレート

```markdown
## [論文タイトル]
- **著者・venue・year**: （一次ソースで確認）
- **arXiv**: [リンク]
- **要点**（3 行以内）:
- **数式/定理**（重要ならコピー）:
- **卒制との接点**（P01〜P36 の ID 付き。例：P11 の IC-LoRA に直接利用）:
- **批判・疑問点**:
- **照合状態**: [ ] 要照合 / [ ] venue 確定 / [ ] 数値確定
```

## 4. 照合フロー（`PAPERS.md` に準ずる）

1. arXiv abs ページで著者・year を確認
2. venue が査読済み proceedings かどうか確認（PDF を入手）
3. 数値（accuracy、サイズ、周回数など）は PDF 本文で確認
4. 照合済みの列は「要照合」→確定値に更新（履歴を残す）

---

## 履歴

- 2026-10-05: 初版作成。既存 36 件を整理＋他分野の基礎論文を curated。著者・venue・数値は要照合。
- 2026-10-15: **I・J 系統追加**。ピクサー（USDパイプライン）とジブリ（手描き2Dパイプライン）を「制作スタジオの巨人」として新設。Phase E（スタジオ実務）を追加。giants-readings.mdとPAPERS.mdの連携強化。
- 今後: Phase A〜E を順に実行。読書ノートは `research/read-log/` に蓄積。
