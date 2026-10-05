# AAS × Change Ontology 統合設計

> `research-animation` の理論と `agentic-anime-studio` の実装を接合する設計書。
> 
> **Goal**: Change Ontology の各概念を AAS.DSL ノード・mcp-db エンティティ・MCP ツールへマッピングし、
> `anima`/`dots`/`montage`/`morph` の4ケースをエンドツーエンドで実行可能にする。

---

## 1. 概念マッピング表

| Change Ontology | AAS.DSL ノード | mcp-db エンティティ | MCP ツール | 意味 |
|:---|:---|:---|:---|:---|
| **ENTITY** | `VarRefNode`（ワークフロー内変数） | `Asset`, `Project`, `Organization` | `mcp-db.save_asset` | 操作対象の存在 |
| **STATE** | `LiteralNode`（JSON 値） | `Asset` + `version` + `ParameterPreset` | `mcp-db.get_asset_by_id` | 記述可能な一時的条件 |
| **RELATION** | `BinaryOpNode`（比較・論理） | `asset.recipe_id` (FK), `asset.tags` (M2M) | `mcp-db.search_assets_by_tag` | 状態間・エンティティ間の接続 |
| **DIFFERENCE** | `BinaryOpNode`（数値差・類似度） | `Evaluation`（vlm_score 差分） | `mcp-ojev.verify_asset_quality` | 状態間の区別 = 変化の最小単位 |
| **TRANSFORMATION** | `ToolCallNode` | `Workflow`（tool 実行履歴） | `mcp-comfyui.generate` 等 | 状態を別状態へ写像する操作 |
| **MORPH** | `ForEachNode` + `StepNode`（補間） | `AssetGroup`（frame序列） | `mcp-2d-pipeline.interpolate` | 中間状態を明示する変化経路 |
| **TIME** | `StepNode.step_index` / ワークフロー順序 | `asset.created_at`, `workflow.VERSION` | `mcp-db.list_workflow_versions` | 状態変化の順序・間隔・繰り返し |
| **SEQUENCE** | `WorkflowNode.steps[]` | `Workflow` + `Step` (1:N) | `mcp-db.save_workflow` | 順序付き状態・変換の構造 |
| **PERCEPTION** | `IfNode`（条件分岐＝知覚判断） | `Evaluation`（意味の評価記録） | `mcp-ojev.verify_temporal_consistency` | シーケンスが知覚される変化 |
| **GENERATION** | ワークフロー全体の実行 | `Asset`（成果物へのリンク） | 実際の MCP ツールコール | 抽象仕様から具体成果物への生成 |

---

## 2. Change Ontology → AAS.DSL コード生成規則

```
ONTOLOGICAL DESCRIPTION          AAS.DSL YAML
─────────────────────────────────────────────────────────────
ENTITY: asset_id: "char_A"        →  variables: { asset_id: "char_A" }

STATE: seed=42, cfg=7.0          →  params: { seed: 42, cfg: 7.0 }

RELATION: asset_id → recipe      →  {{asset_id}} で変数参照

DIFFERENCE: score_delta > 0.1    →  condition: "{{eval.score}} - {{prev.score}} > 0.1"

TRANSFORMATION: generate image   →  tool: mcp-comfyui.generate

MORPH: A → [A₁,A₂,A₃] → B       →  foreach: interpolation_steps + generate each

TIME: frame 1, 12, 24            →  foreach: [1, 12, 24]  or step_index

SEQUENCE: shot_1 → shot_2 → ...  →  steps: [step_1, step_2, ...]

PERCEPTION: quality > threshold  →  if: condition → then/else

GENERATION: execute workflow     →  dsl_executor.run(workflow_yaml)
```

---

## 3. 4ケースの AAS.DSL 実装

### 3.1 anima — concrete visual state change

絵コンテ駆動の具像的アニメーション。`ENTITY`（キャラクター）が`STATE`（ポーズ・表情）を`TIME`軸上で変化。

```yaml
workflow:
  name: "anima_concrete_visual_change"
  variables:
    char_id: "girl_red_hair"
    scene: "sunflower_field_walk"
    style_preset: "ghibli_v3"
    
  steps:
    # STATE 0: 初期状態（立ち止まる）
    - name: state_0_standing
      tool: mcp-comfyui.generate
      params:
        prompt: "{{char_id}}, standing in sunflower field, {{style_preset}}"
        controlnet: openpose
        openpose_file: "standing.json"
        seed: 42
      save_as: standing_frame
      
    # STATE 1: 歩き始める（DIFFERENCE: pose変化）
    - name: state_1_walking
      tool: mcp-comfyui.generate
      params:
        prompt: "{{char_id}}, walking in sunflower field, {{style_preset}}"
        controlnet: openpose
        openpose_file: "walking_1.json"
        seed: 43
        # RELATION: standing と walking の対応（同一キャラ同一環境）
        ipadapter: "{{standing_frame.output}}"
      save_as: walking_frame
      
    # TRANSFORMATION: standing → walking の MORPH（補間）
    - name: morph_standing_to_walking
      tool: mcp-2d-pipeline.interpolate
      params:
        start_image: "{{standing_frame.output}}"
        end_image: "{{walking_frame.output}}"
        frames: 12  # intermediate states
        method: "depth_guided"
      save_as: morph_frames
      
    # TIME: 12フレームから48フレームシーケンスへ配置
    - name: sequence_48fps
      tool: mcp-2d-pipeline.temporal_compose
      params:
        keyframes: ["{{standing_frame.output}}"]
        intermediates: "{{morph_frames.outputs}}"
        total_frames: 48
        timing_curve: "ease_in_out"
      save_as: final_sequence
      
    # PERCEPTION: 動きの自然さを評価
    - name: perception_check
      tool: mcp-ojev.verify_temporal_consistency
      params:
        asset_ids: "{{final_sequence.frame_ids}}"
      save_as: consistency_eval
      
    # 評価が閾値未満なら差し戻し（Montage的PERCEPTIONループ）
    - name: feedback_loop
      if: "{{consistency_eval.verdict}} != 'perfect'"
      then:
        tool: mcp-lms.critique_and_feedback
        params:
          frame_ids: "{{final_sequence.frame_ids}}"
          issue_type: "{{consistency_eval.verdict}}"
      else:
        tool: mcp-db.save_asset
        params:
          name: "{{scene}}_final"
          file_path: "{{final_sequence.output}}"
          tags: ["anima", "{{char_id}}", "{{scene}}"]
```

### 3.2 dots — abstract structural state change

点・構造・関係だけで変化する抽象アニメーション。`ENTITY`が具象的ビジュアルではなく「状態そのもの」。

```yaml
workflow:
  name: "dots_abstract_state_change"
  variables:
    n_dots: 24
    width: 256
    height: 256
    frames: 60
    
  steps:
    # STATE 0: ランダム分散（高エントロピー）
    - name: state_0_random
      tool: mcp-lms.procedural_generate
      params:
        type: "dots"
        n: "{{n_dots}}"
        distribution: " uniform"
        width: "{{width}}"
        height: "{{height}}"
        seed: 42
      save_as: random_state
      
    # STATE 1: 円周上への同調（秩序化）
    - name: state_1_circle
      tool: mcp-lms.procedural_generate
      params:
        type: "dots"
        n: "{{n_dots}}"
        distribution: "circle"
        radius: 100
        center: [128, 128]
        seed: 42
      save_as: circle_state
      
    # MORPH: 分散 → 同調の経路（中間状態を明示）
    - name: morph_random_to_circle
      foreach: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
      steps:
        - name: interpolate_state
          tool: mcp-lms.procedural_interpolate
          params:
            start: "{{random_state.data}}"
            end: "{{circle_state.data}}"
            t: "{{item}}"
            easing: "sine_in_out"
          save_as: "frame_{{item}}"
          
    # PERCEPTION: 構成の変化を評価（情報理論的）
    - name: perception_entropy
      tool: mcp-ojev.verify_asset_quality
      params:
        asset_id: "frame_0.5"
        criterion: "structural_coherence"
        options: ["ordered", "transitional", "chaotic"]
      save_as: entropy_eval
      
    # GENERATION: GIF出力
    - name: generate_gif
      tool: mcp-lms.render_sequence
      params:
        frames: "{{morph_random_to_circle.outputs}}"
        format: "gif"
        fps: 10
      save_as: dots_animation
```

### 3.3 montage — relational meaning between states

ショット間の関係が知覚される意味を生成。Eisenstein的モンタージュ。

```yaml
workflow:
  name: "montage_relational_meaning"
  variables:
    sequence: "confrontation_buildup"
    
  steps:
    # STATE A: キャラクターAの顔（中景）
    - name: shot_a_face
      tool: mcp-comfyui.generate
      params:
        prompt: "character A looking determined, medium close-up, ghibli style"
        seed: 100
      save_as: shot_a
      
    # STATE B: キャラクターBの顔（中景）
    - name: shot_b_face
      tool: mcp-comfyui.generate
      params:
        prompt: "character B looking calm but tense, medium close-up, ghibli style"
        seed: 101
      save_as: shot_b
      
    # RELATION: ショットAとショットBの collision → PERCEIVED MEANING C（対立の緊張）
    # この関係を評価
    - name: relation_juxtaposition
      tool: mcp-ojev.verify_asset_quality
      params:
        asset_id: "{{shot_a.output}},{{shot_b.output}}"
        criterion: "montage_tension"
        options: ["neutral", "tense", "confrontational", "emotional"]
      save_as: montage_eval
      
    # DIFFERENCEが小さければ（A≈B）、モンタージュ効果なし → 修正
    - name: feedback_if_weak_relation
      if: "{{montage_eval.decision}} == 'neutral'"
      then:
        steps:
          - name: regenerate_shot_b
            tool: mcp-lms.critique_and_feedback
            params:
              asset_id: "{{shot_b.output}}"
              issue: "relation too weak for montage"
              prompt_addition: "(intense lighting, dramatic expression:1.3)"
      else:
        tool: mcp-db.save_asset
        params:
          name: "montage_{{sequence}}"
          file_path: "{{shot_a.output}}"
          tags: ["montage", "shot_a"]
          
    # SEQUENCEとして結合
    - name: sequence_edit
      tool: mcp-2d-pipeline.composite
      params:
        shots: ["{{shot_a.output}}", "{{shot_b.output}}"]
        cut_duration: ["2s", "2s"]
        transition: "hard_cut"
      save_as: montage_sequence
```

### 3.4 morph — explicit path of transformation

状態Aから状態Bへ至る経路そのものを生成対象とする。アニメーションで最も重要な概念。

```yaml
workflow:
  name: "morph_explicit_path"
  variables:
    entity: "flower_bud"
    start_state: "bud"
    end_state: "bloom"
    n_intermediates: 8
    
  steps:
    # STATE A: つぼみ
    - name: state_a_bud
      tool: mcp-comfyui.generate
      params:
        prompt: "{{entity}}, {{start_state}}, ghibli flower"
        seed: 200
      save_as: bud_image
      
    # STATE B: 満開
    - name: state_b_bloom
      tool: mcp-comfyui.generate
      params:
        prompt: "{{entity}}, {{end_state}}, ghibli flower"
        seed: 201
      save_as: bloom_image
      
    # MORPH SPECIFICATION: 経路を明示的に設計
    # 物理的制約: つぼみ → ほころび → 部分開花 → 満開
    - name: morph_path_design
      tool: mcp-lms.generate_morph_spec
      params:
        start: "{{bud_image.output}}"
        end: "{{bloom_image.output}}"
        n_stages: "{{n_intermediates}}"
        constraints:
          - "petals unfold progressively"
          - "center remains stable"
          - "color shifts from green to pink"
      save_as: morph_spec
      
    # 各中間状態を生成
    - name: generate_intermediates
      foreach: "{{morph_spec.stages}}"
      steps:
        - name: morph_frame
          tool: mcp-comfyui.generate
          params:
            prompt: "{{item.description}}, ghibli flower"
            controlnet: lineart
            lineart_image: "{{item.lineart}}"
            seed: "{{item.seed}}"
          save_as: "morph_{{item.index}}"
          
    # PERCEPTION: 変化の連続性を検証
    - name: verify_morph_continuity
      tool: mcp-ojev.verify_temporal_consistency
      params:
        asset_ids: "{{generate_intermediates.outputs}}"
        criterion: "morph_smoothness"
      save_as: morph_eval
      
    # 不通過なら経路を再設計
    - name: path_refinement
      if: "{{morph_eval.verdict}} == 'broken'"
      then:
        tool: mcp-lms.critique_and_feedback
        params:
          issue: "morph discontinuity detected"
          n_additional_intermediates: 4
      else:
        tool: mcp-db.save_asset
        params:
          name: "{{entity}}_morph_{{start_state}}_to_{{end_state}}"
          file_path: "{{generate_intermediates.outputs}}"
          tags: ["morph", "{{entity}}"]
```

---

## 4. SDI (Static-Dynamic Interface) 統合

`research-animation` の `sdi/` は「静的な世界定義」 (`world.json`) と「動的な振る舞い」を分離する実験。

これは AAS の「mcp-db (static ontology) + AAS.DSL (dynamic execution)」アーキテクチャと完全に同一。

```
┌─────────────────────────────────────────────────────┐
│              Static World (mcp-db)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Entity   │  │ Relation │  │Capability│           │
│  │ (Asset)  │  │ (FK/M2M) │  │(Recipe)  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│           ↑                              ↑           │
│           │        SDI Boundary          │           │
│           ↓                              ↓           │
│              Dynamic Behavior (AAS.DSL)              │
│  ┌──────────────────────────────────────────┐        │
│  │ Workflow = Behavior definition            │        │
│  │ Step     = State transition rule         │        │
│  │ ToolCall = Capability activation         │        │
│  └──────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

### SDI の AAS 実装

```yaml
# world.json → mcp-db スキーマ対応
# static world definition (事前登録済み)

workflow:
  name: "sdi_dynamic_behavior"
  variables:
    static_world_id: "dots_world_001"
    behavior: "orbit"  # orbit | pulse | attract
    
  steps:
    # 1. Static World を db から取得
    - name: load_world
      tool: mcp-db.list_assets_in_project
      params:
        project_id: "{{static_world_id}}"
        tag: "entity"
      save_as: entities
      
    # 2. Dynamic Behavior 選択（SDI の分離点）
    - name: apply_behavior
      tool: mcp-lms.procedural_behavior
      params:
        entities: "{{entities}}"
        behavior: "{{behavior}}"
        # Capability に応じた Behavior 選択
        duration: 60
        fps: 10
      save_as: behavior_frames
      
    # 3. 同じ World に異なる Behavior を適用可能（SDIの核心）
    - name: compare_behaviors
      foreach: ["orbit", "pulse", "attract"]
      steps:
        - name: behavior_variant
          tool: mcp-lms.procedural_behavior
          params:
            entities: "{{entities}}"
            behavior: "{{item}}"
            duration: 60
          save_as: "behavior_{{item}}"
```

---

## 5. 東映動画語彙 → AAS オントロジー候補

| 東映動画語彙 | 機能 | AAS オントロジー対応 | 実装 |
|:---|:---|:---|:---|
| 作画監督 | COORDINATION / QUALITY CONTROL | `Evaluation.evaluator_type` | `mcp-ojev` |
| 演出 | DIRECTION / INTENTION | `Workflow.director_notes` | `mcp-storyboard` |
| 原画 | KEY STATE | `Asset` with `asset_type: "keyframe"` | `mcp-comfyui` |
| 動画 | INTERMEDIATE STATE | `Asset` with `asset_type: "inbetween"` | `mcp-2d-pipeline.interpolate` |
| レイアウト | SPATIAL STATE / STAGING | `ParameterPreset` with layout params | `mcp-2d-pipeline.layout` |
| シート | TIME / TEMPORAL CONTROL | `Workflow` + step_index | AAS.DSL `foreach` over frame indices |
| 撮影上がり | COMPOSITING / FINAL OUTPUT | `Asset` with `asset_type: "composite"` | `mcp-2d-pipeline.composite` |
| 透過光効果 | TRANSFORMATION / PERCEPTION | `Recipe.params.effect` | `mcp-2d-pipeline.effects` |
| 特殊効果 | VISUAL TRANSFORMATION | `ParameterPreset.effects[]` | ComfyUI custom nodes |
| カット | CINEMATIC UNIT | `AssetGroup` (sequential frames) | `mcp-db.save_asset_group` |
| カメラアングル | VIEWPOINT STATE | `ParameterPreset.camera` | ControlNet depth/pose |
| カメラワーク | VIEWPOINT TRANSFORMATION | `Workflow` with camera move steps | `mcp-2d-pipeline.camera` |
| 作画枚数制限 | CONSTRAINT → STYLE | `CostLog` + `mcp-cost-manager` | budget-driven generation |

---

## 6. 実装ロードマップ

### Phase 1（理論統合）— 完了
- [x] Change Ontology → AAS.DSL マッピング
- [x] mcp-db スキーマ ↔ USD Prim/Attribute/Relationship 対応
- [x] 4ケース YAML サンプル作成

### Phase 2（実行化）
- [ ] `MorphNode` を AAS.DSL AST に追加（中間状態生成の特化ノード）
- [ ] `PerceptionNode` を AAS.DSL AST に追加（評価→フィードバック統合）
- [ ] `mcp-2d-pipeline.interpolate` を実装（depth-guided inbetweening）
- [ ] `mcp-lms.procedural_behavior` を実装（SDI動的振る舞い）
- [ ] 東映語彙を `Tag` テーブルの初期シードとして投入

### Phase 3（検証）
- [ ] `dots` ケース: 24点の6フレームアニメーションを GIF 出力
- [ ] `anima` ケース: 絵コンテ→原画→中割り→仕上げの4工程実装
- [ ] `montage` ケース: 2ショットの緊張度評価と自動修正
- [ ] `morph` ケース: つぼみ→満開の8中間状態生成
- [ ] 全ケースを `mcp-ojev` で評価・記録

---

## 7. 参考文献連携

| 文献 | 役割 |
|:---|:---|
| `research-animation/README.md` | 本統合の理論的背景（GOAL → Change Ontology → Generation） |
| `research-animation/TAXONOMY.md` | `ENTITY→STATE→...→GENERATION` の分類体系 |
| `research-animation/RQ.md` | 東映動画語彙研究プロトコル（日本語の制作語彙を回収） |
| `research-animation/PRINCIPLES.md` | Phase 1 = 理論先行、Phase 2 = 技術選択原則 |
| `research-animation/ONTOLOGY.md` | オントロジー原語と核心命題 |
| `PAPERS.md` | 8〜10系統の論文マップ（I01=USD, J01-12=ジブリ, P33-P34=AniDoc/AniDepth） |
| `giants-readings.md` | 読書計画 Phase A〜E（理論→実務の5段階） |
| `I01-usd-pipeline.md` | USD Stage ↔ mcp-db マッピング詳細 |
| `J01-ghibli-pipeline.md` | ジブリ工程 ↔ AAS.DSL step 対応詳細 |

---

## 更新履歴

- 2026-10-15: 初版作成。research-animation の Change Ontology を AAS 実装体系に統合。4ケース YAML + SDI + 東映語彙マッピング。
