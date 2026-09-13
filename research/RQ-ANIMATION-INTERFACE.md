# RQ-ANIMATION-INTERFACE — Research ArchitectureとAnimationの界面

## 0. Positioning

本RQは、`research-architecture` と `research-animation` の間にある未定義の接続面を研究対象とする。

Animationは単なる動画出力ではない。Research Architectureから渡されたResearch Question / Research Objectを、時間軸上の状態変化として実行可能なResearch Runへ変換し、その結果を再びObservation可能な形で返す。

```text
Research Question
        ↓
Research Object
        ↓
Animation Research Interface
        ↓
Temporal Transformation
        ↓
Animation Run
        ↓
Artifact + Manifest + Observation Anchors
        ↓
Research Architecture
```

---

## 1. Main Research Question

> Research Architectureから与えられたResearch QuestionとResearch Objectを、Animation固有の時間・変化・状態の構造へ変換し、再現可能なAnimation Runとして実行・観察・返却するためには、どのような界面が必要か？

### Knowledge Gap

Research ArchitectureはRQ、Hypothesis、Evidence、Evaluationを扱い、research-animationはrenderer、frame、animation artifactを扱う。しかし、両者を接続する「何をAnimationとして実験し、何をObservationとして研究側へ返すか」という契約が明示されていない。

したがって問題はrendererの不足ではなく、**Research QuestionとAnimation Experimentの間のinterface不足**である。

---

## 2. RQ-AI1 — Research Input

> Research ArchitectureのRQ / Research Objectを、Animation Experimentが受け取れる最小入力へどのように変換できるか？

### H1
RQ、対象、初期状態、変換対象、時間条件を持つResearch Requestへ正規化できる。

### H0 / Antithesis
Animationは研究質問から独立した表現活動であり、共通入力契約を持たせると研究上の自由度を失う。

### Falsification
主要なAnimation実験で共通入力契約が成立せず、個別の文脈情報が不可欠となる場合。

---

## 3. RQ-AI2 — Temporal Transformation

> Research Objectの変化を、Animation固有のTemporal Transformationとしてどのように記述できるか？

### H1
状態、変換、時間パラメータの組としてAnimation Experimentを記述できる。

```text
I₀ → T₀→₁ → I₁ → T₁→₂ → I₂ → ... → Iₙ
```

### H0 / Antithesis
Animationの時間性は状態間変換には還元できず、より高次の時空間・知覚・物語構造を必要とする。

### Falsification
状態＋変換モデルがAnimationの重要な時間的性質を体系的に欠落させる場合。

---

## 4. RQ-AI3 — Observation Interface

> Animation Artifactを、Research Architectureが観察・評価可能なEvidence候補へどのように接続できるか？

### H1
ArtifactそのものとObservationを分離し、frame/timeを指示するObservation Anchorによって接続できる。

```text
Artifact
  ├─ frame
  ├─ time
  └─ manifest
       ↓
Observation Anchor
       ↓
Observation
       ↓
Evidence
```

### H0 / Antithesis
動画全体が不可分な研究対象であり、frame/time単位への分解は意味を損なう。

### Falsification
重要なAnimation現象がAnchor単位で再現・参照できず、全体的な知覚経験を必要とする場合。

---

## 5. RQ-AI4 — Provenance

> Animation Runを再現可能なResearch Artifactとして成立させるために、どのようなProvenanceを保持すべきか？

### H1
Input、Transformation、Temporal Parameters、Renderer、Version、Run ID、Artifactを紐付ければ、少なくとも実験条件を再構成できる。

### H0 / Antithesis
Animationの再現性はパラメータだけでは保証できず、環境・モデル・乱数・生成過程などを含むより広い記録が必要である。

### Falsification
同一Manifestでは実験条件を再現できない重要因子が継続的に発生する場合。

---

## 6. RQ-AI5 — Repository Boundary

> Research Architectureとresearch-animationの責務境界をどこに置けば、ArtifactとEvidenceの重複を避けながら研究の連続性を保てるか？

### H1
`research-animation`はAnimation Artifact / Manifest / Runを所有し、`research-architecture`はObservation / Evidence / Evaluation / Thesisを所有する境界が成立する。

### H0 / Antithesis
研究ArtifactとEvidenceを分離すると、研究文脈が分断されるため、同一リポジトリまたは同一文書へ統合すべきである。

### Falsification
Repository Boundaryによって参照関係が複雑化し、研究追跡性が明確に低下する場合。

---

## 7. Working Thesis

### T-AI1
Animation Researchには、Research QuestionとAnimation Artifactの間を接続する明示的なResearch Interfaceが必要である。

Status: proposed  
Confidence: medium

### T-AI2
最小界面は、`Research Request → Temporal Transformation → Animation Run → Artifact/Manifest → Observation Anchor`として記述できる。

Status: proposed  
Confidence: medium

### T-AI3
ArtifactとEvidenceを同一視せず、ManifestとObservation Anchorを介して接続することで、AnimationとResearch Architectureの責務を分離できる。

Status: proposed  
Confidence: medium

---

## 8. Antitheses

### A-AI1
Animationは研究質問から独立した創作・生成行為であり、Research Interfaceによる標準化は不適切である。

### A-AI2
時間的・知覚的現象はframe/time Anchorでは十分に記述できない。

### A-AI3
Repository BoundaryはResearch Contextを分断し、Evidence Traceabilityを悪化させる。

---

## 9. Falsification Conditions

1. 共通Research Requestが複数のAnimation実験に適用できない。
2. Temporal Transformationが重要なAnimation現象を説明できない。
3. Observation Anchorでは研究上重要な現象を参照できない。
4. Manifestを保持しても再現性が改善しない。
5. Repository BoundaryによってTraceabilityが実質的に低下する。

---

## 10. Research Method

```text
Research Architecture Issues
        ↓
Interface Gap Extraction
        ↓
RQ Definition
        ↓
Existing Animation Cases
        ↓
Cross-case Comparison
        ↓
Interface Candidate
        ↓
Counterexample Search
        ↓
Revision
```

### Evidence Sources

- `research-architecture` Issues / RQ / experiments
- `research-animation` Issues / RQ / experiments
- Animation experiment manifests
- Existing renderer outputs
- Observation / evidence records
- Morphing / VFI / generative-video literature

---

## 11. Interface Contract — Candidate

```yaml
animation_run:
  id: EXP-XXX-RUN-XXX
  research_question: RQ-XXX

  input:
    research_object: ...
    initial_state: ...

  transformation:
    type: ...
    rule: ...

  time:
    duration: ...
    fps: ...
    timeline: ...

  execution:
    renderer: ...
    version: ...
    parameters: ...

  artifact:
    animation: ...
    manifest: ...

  observation:
    anchors:
      - frame: ...
        time: ...

  provenance:
    source: ...
    run_id: ...
```

これは実装仕様ではなく、**研究上の界面を検証するための仮説モデル**である。

---

## 12. Responsibility Boundary

| Concern | research-animation | research-architecture |
|---|---|---|
| Research Question | reference | owner |
| Research Object | transform | define |
| Temporal Transformation | owner | reference |
| Animation Run | owner | reference |
| Renderer | owner | — |
| Frame / Video Artifact | owner | reference |
| Manifest | owner | reference |
| Observation Anchor | owner | consume |
| Observation | — | owner |
| Evidence | — | owner |
| Evaluation | — | owner |
| Thesis / Revision | — | owner |

---

## 13. Relation to Morphing

Morphing研究で導入した

```text
STATE → TRANSFORMATION → STATE
```

をAnimation InterfaceのTemporal Transformationとして扱う。

したがってMorphingはこのInterfaceの具体的な研究対象の一つであり、Interfaceそのものではない。

```text
Research Architecture
        ↓
Animation Research Interface
        ↓
Temporal Transformation
   ┌────┼──────────┐
Morphing  VFI  Generative Video
   └────┼──────────┘
        ↓
Animation Artifact
```

---

## 14. Next Question

> Animation Research Interfaceを通して、異なるAnimation実験を同一のResearch Questionに対する比較可能なEvidenceへ変換するための最小Observation単位は何か？
