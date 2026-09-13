# RQ-MORPHING — AnimationにおけるMorphing研究質問

## 0. Positioning

MorphingをAnimationと並列する独立研究領域として扱わない。

本研究では、MorphingをAnimationの下位にある**フレーム間変換の共通ロジック**として位置づける。
動画生成を単一の「動画」オブジェクトとしてではなく、画像状態と状態間の変換規則の系列として分析する。

```text
I₀ → T₀→₁ → I₁ → T₁→₂ → I₂ → ... → Iₙ
```

- `I` = image / frame state
- `T` = transformation / morphing rule
- `t` = temporal parameter

これは既存手法が同一実装であるという主張ではなく、Animation研究のための分析上の共通抽象である。

---

## 1. Main Research Question

> 動画を連続する画像フレームの集合として捉えたとき、フレーム間の変形規則をどのように記述・設計することで、時間的に連続した動画を生成できるか？

### Knowledge Gap

Classical image morphing、video frame interpolation、modern generative videoは、それぞれ異なる技術領域として発展している。一方で、これらを「画像状態」と「状態間変換」の系列として比較したとき、どこまで共通化でき、どこから共通化できなくなるのかは本研究の問いとして残る。

---

## 2. RQ-M1 — State

> 動画は、`I₀, I₁, ..., Iₙ` という画像状態の系列として記述できるか？

### H1
動画の時間構造を、離散的な画像状態の系列として最低限記述できる。

### H0 / Antithesis
動画の本質は個々のフレームではなく、潜在的な時空間表現にあり、画像状態の系列だけでは説明力が不足する。

### Falsification
主要な動画生成方式を状態系列として記述すると、重要な時間的性質が一貫して失われる場合。

### Method
Morphing、VFI、video diffusion等の文献で入力・中間状態・出力の関係を比較する。

### Expected Evidence
各方式が扱う入力状態、生成状態、時間条件、出力の記述。

---

## 3. RQ-M2 — Transformation

> `Iₜ → Iₜ₊₁` を、単なる2枚の画像ではなく明示的な変換規則として記述できるか？

### H1
対応関係、warp、flow、blend、latent transitionなどを、状態間の変換として記述できる。

### H0 / Antithesis
変換規則を明示すると、潜在表現や生成過程の重要部分を失うため、共通モデルとして不適切である。

### Falsification
主要方式の時間的変化が状態間変換として表現できず、別の基本単位を必要とする場合。

### Method
Classical morphing、VFI、生成動画の変換表現を横断比較する。

### Expected Evidence
correspondence、optical flow、depth-aware flow、intermediate frame、latent temporal dynamics等の対応関係。

---

## 4. RQ-M3 — Continuity

> 変換された状態系列が、どのような条件で知覚的に連続した運動として成立するか？

### H1
時間的連続性は、状態間変換の一貫性として一定程度説明できる。

### H0 / Antithesis
知覚的連続性は幾何学的変換だけでは説明できず、意味、物体、因果性、音、物語などを必要とする。

### Falsification
画素・幾何・flow等の変換的一貫性が高くても、知覚上の連続性が体系的に成立しない場合。

### Method
Temporal consistency、occlusion、large motion、semantic consistency等を扱う文献を比較する。

### Expected Evidence
連続性を評価する指標、失敗事例、モデルの制約。

---

## 5. RQ-M4 — Time

> 変換規則に時間パラメータ `t` を導入すると、速度、停止、加速、反復、持続時間をどのように記述できるか？

### H1
同じ状態間変換でも、時間配置を変えることで異なる運動として記述できる。

### H0 / Antithesis
時間的意味はフレーム間変換だけでは決まらず、より高次の時空間表現を必要とする。

### Falsification
時間配置を変えても説明できない重要な運動特性が体系的に存在する場合。

### Method
frame rate、timestep、interpolation、slow motion、temporal conditioningを比較する。

### Expected Evidence
時間条件と生成結果の関係、速度変化、任意時刻生成など。

---

## 6. RQ-M5 — Generation

> 動画生成を「動画を直接生成する問題」ではなく、「画像状態を生成し、状態間の変換を時間軸へ配置する問題」として再定義できるか？

### H1
少なくとも一部の動画生成方式について、この再定義が理論的な比較枠組みとして有効である。

### H0 / Antithesis
現代の生成動画は新規コンテンツと潜在的時空間ダイナミクスを同時に生成するため、画像状態＋明示的変換への還元は本質を失う。

### Falsification
代表的な生成動画方式を分析した結果、状態＋変換モデルが説明上の利点を持たず、かえって重要な差異を隠す場合。

### Method
Classical morphing → VFI → video diffusionを同一の分析表へ配置し、共通点と非共通点を明示する。

### Expected Evidence
入力形式、状態表現、変換表現、時間表現、連続性機構、生成能力、失敗条件。

---

## 7. Working Thesis

### T-M1
Image morphing、frame interpolation、video generationを比較する際、**状態系列＋状態間変換**は有用な共通抽象になり得る。

Status: proposed  
Confidence: medium

### T-M2
時間的連続性は、生成されたフレーム単体だけでなく、**変換系列の性質**として研究できる。

Status: proposed  
Confidence: low

### T-M3
Modern image-to-video generationは、classical morphingやframe interpolationと実装上同一ではないが、**state-transition systemとして理論比較できる可能性がある**。

Status: proposed  
Confidence: low

---

## 8. Antitheses

### A-M1
Videoは独立した画像＋変換へ還元できない。潜在的な時空間表現そのものが時間的整合性を担う可能性がある。

### A-M2
Morphing / interpolationは制約された補間問題であり、generative videoは新しい内容を生成する問題である。両者の共通化は差異を消す可能性がある。

### A-M3
知覚的連続性はgeometry / pixelsだけでは説明できない。semantic consistency、object identity、causality、sound、narrative等も寄与する。

---

## 9. Falsification Conditions

以下のいずれかが強く確認された場合、共通抽象を縮小・分割・棄却する。

1. 主要な動画生成方式がstate-transitionとして十分に記述できない。
2. temporal coherenceが状態間変換では表現できない基本表現に依存する。
3. 共通抽象による説明力が、方式ごとの個別説明を上回らない。
4. Morphing / VFI / generative videoの重要な差異を共通化によって失う。

---

## 10. Research Method

```text
Question
  ↓
Literature Exploration
  ↓
Concept Extraction
  ↓
Hypothesis
  ↓
Cross-domain Comparison
  ↓
Verification
  ↓
Observation
  ↓
Evidence
  ↓
Evaluation
  ↓
Revision
```

### Phase 1 — Literature Map

対象:
- classical image morphing
- video frame interpolation
- optical flow / motion estimation
- temporal consistency
- video diffusion / generative video

### Phase 2 — Concept Normalization

最低限、以下を整理する。

- state
- correspondence
- transformation
- interpolation
- motion
- optical flow
- temporal consistency
- continuity
- occlusion
- latent dynamics
- temporal conditioning

### Phase 3 — Cross-domain Matrix

各方式を以下で比較する。

| 項目 | 内容 |
|---|---|
| Input States | 入力画像・フレーム |
| State Representation | 状態の表現 |
| Transformation | 状態間変換 |
| Temporal Variable | 時間の表現 |
| Continuity Mechanism | 連続性の機構 |
| Output | 出力状態系列 |
| Limitation | 限界・失敗条件 |

### Phase 4 — RQ Mapping

各文献の主張をRQM1〜RQM5へ対応付ける。

### Phase 5 — Gap Analysis

共通モデルで説明できる領域と、説明できない領域を分離する。

### Phase 6 — Synthesis

最小共通モデルと、その明示的な失敗条件を定義する。

---

## 11. Evidence Discipline

```text
Observation ≠ Interpretation ≠ Hypothesis ≠ Conclusion
```

ある論文がframe interpolationを実行していることは、その論文についてのEvidenceである。それだけから「すべてのvideo generationはframe interpolationである」と結論してはならない。

LlamaIndexは文献探索・検索・整理のための研究基盤として使用できるが、LlamaIndex自体を理論的根拠とはしない。

---

## 12. Evaluation

研究モデルは以下で評価する。

1. **Coverage** — どれだけ多くの方式を記述できるか
2. **Discrimination** — 方式間の重要な差異を保持できるか
3. **Explanatory Value** — 単なる分類以上の説明力を持つか
4. **Research Utility** — 次の研究質問を生成できるか

---

## 13. Revision Rules

Evidenceに応じて以下のいずれかへ更新する。

- strengthen
- qualify
- geometric transformation / semantic generationへ分割
- frame-sequence constructionに限定
- common abstractionをreject

---

## 14. Next Question

> 状態間の知覚的連続性を保持するために必要な、変換規則の最小表現は何か？

このRQを、Morphing研究からAnimation研究へ戻す接続点とする。
