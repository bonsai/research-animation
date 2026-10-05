# J01 — Studio Ghibli Hand-Drawn Pipeline

## ソース情報

| 項目 | 内容 |
|---|---|
| **文献タイプ** | Production Documentation + SIGGRAPH Talks + 学術論文 |
| **参考文献** | 「スタジオジブリの現場」（2005）、宮崎駿『出発点・折り返し点』（1996/2008） |
| **公開年** | 1996-2020年代 |
| **URL** | [Ghibli Museum Archive](https://www.ghibli-museum.jp/) / 宮崎駿インタビュー集 |
| **venue** | N/A（制作ドキュメント）/ SIGGRAPH Asia（技術発表として） |

---

## ジブリの制作パイプライン（学術的に学ぶべき構造）

### 1. 制作フロー：「絵コンテ → レイアウト → 原画 → 動画 → 仕上げ」

```
Storyboard (絵コンテ — 宮崎駿・演出)
    ↓
Layout (レイアウト — 背景とキャラの位置関係)
    ↓
Key Animation (原画 — 動きの設計図)
    ↓
In-between (動画 — 中割り)
    ↓
Color Design (色指定 — 色彩設計)
    ↓
Digital Paint (仕上げ — デジタル彩色)
    ↓
Background Art (背景美術 — 男鹿和雄など)
    ↓
Composition (撮影効果 — コンポジット)
```

**卒制への接点**: このパイプラインはAAS.DSLのstep graphと完全に同型。各工程 = `StepNode`。差し戻し（layout → storyboard修正）は`IfNode`で表現。

### 2. 色指定（Color Design）— 色彩のパラメトリック化

ジブリの色指定は、原画に**色番号**で指示を与えるシステム。

| 要素 | ジブリの手法 | 卒制の対応 |
|---|---|---|
| キャラクター色 | キャラクターシート（固定palette） | `ParameterPreset` with `char_id` |
| 時間帯変化 | 指定時間帯でpalette全体をシフト | LoRA weight切り替え |
| 感情変化 | 色彩の彩度・明度変化（「千と千尋」湯屋の場面） | `saturation` / `brightness` param |
| 光源変化 | 朝昼晩での陰影パターン | ControlNet illumination condition |

**学術的洞察**: 「色指定」は実質的に**制約付きpalette回帰**。指定された色番号の集合から、線画領域への最適割り当てを行う問題。これはAutoColorizationの制約版。

### 3. 線画と彩色の分離：ジブリの"見えない線"

ジブリの特徴的な技法：

- **輪郭線の太さ変化**: 遠景は細線、近景は太線、強調したい部分はbold
- **線色の変化**: 肌は茶色線、影は青紫線、光は黄線（「もののけ姫」）
- **線の"消失"**: 髪の毛先や服のシワで線がフェード（线描の限界を超える）

**卒制への接点**: ControlNet line-art + color hintの2段生成。ただし、単なるcolorizationではなく、「線の性質（色・太さ・フェード）」も生成対象とする必要がある。これはP30 Chat2SVGの2段構成（template → detail）と同型。

### 4. 背景美術：「グラデーションの魔術師」男鹿和雄

男鹿和雄の技法：
- **航空写真を参考にした俯瞰構図**
- **色の階層**: 近景 → 中景 → 遠景 で hue shift（近い緑 → 遠い青緑）
- **ノイズとテクスチャ**: 水彩のにじみ、紙の目、乾いた筆の擦れ

**学術的対応**: 
- Depth-aware background generation（遠景ぼかし）
- Style transfer with texture synthesis（ watercolor texture ）
- Hierarchical color palette extraction from reference

---

## アカデミック研究としてのジブリパイプライン

### Colorization研究との接続

| 論文 | venue | ジブリ手法との対応 |
|---|---|---|
| P33 AniDoc | arXiv 2024 | Sparse sketch → full colorization（端2枚指定） |
| P34 AniDepth | SIGGRAPH 2025 | Depth-guided inbetweening（動画の中割り） |
| "Reference-based Sketch Colorization" | CVPR系列 | キャラシート（数枚の参照）から線画を彩色 |
| "Manga Colorization" | SIGGRAPH Asia | 漫画→カラー。制約（screentone分離）が似ている |
| "Anime Shadow Detection" | ECCV | 陰影パターンの自動抽出（色指定の補助） |

### ジブリ特有の「美学」を機械化するための研究

| 美学要素 | 研究課題 | 既存論文 |
|---|---|---|
| **空気感**（大気遠近法） | Depth-aware haze + color temperature shift | MiDaZo / Depth Anything |
| **食べ物の光沢** | Specular highlight modeling on food | Neural Rendering |
| **水の表現** | Procedural water + reflection（「千と千尋」の湯） | Fluid simulation + style transfer |
| **風の演出** | Motion field + line distortion | Optical flow + edge warp |
| **光の帯**（ゴッドレイ） | Volumetric light shafts | Volumetric rendering |

---

## 卒制システムへの統合設計

### J系統論文群（ジブリパイプライン制御）

```yaml
# AAS.DSL: ジブリ風制作ワークフロー
workflow:
  name: "ghibli_style_cut_001"
  
  steps:
    # 1. Storyboard (絵コンテ)
    - name: storyboard
      tool: mcp-storyboard.generate
      params:
        script: "girl walking through sunflower field, golden hour"
        aspect_ratio: "16:9"
        
    # 2. Layout (レイアウト)
    - name: layout
      tool: mcp-2d-pipeline.layout
      params:
        storyboard: "{{storyboard.output}}"
        depth_layers: [foreground, midground, background]
        
    # 3. Key Animation (原画)
    - name: keyframes
      tool: mcp-comfyui.generate
      foreach: "{{layout.key_frames}}"
      params:
        prompt: "{{item.description}}, ghibli anime style, key animation frame"
        controlnet: lineart
        lora: ghibli_v3
        
    # 4. Color Design (色指定)
    - name: color_design
      tool: mcp-lms.auto_color
      params:
        keyframes: "{{keyframes.outputs}}"
        palette_reference: "ghibli_sunflower_palette"
        
    # 5. In-between (中割り)
    - name: inbetween
      tool: mcp-2d-pipeline.interpolate
      params:
        frames: "{{keyframes.outputs}}"
        method: "depth_guided"  # AniDepth方式
        
    # 6. Background (背景美術)
    - name: background
      tool: mcp-2d-pipeline.background
      params:
        layout: "{{layout.background_region}}"
        style: "ghibli_watercolor"
        atmosphere: "golden_hour"
        
    # 7. Composition (撮影効果)
    - name: composite
      tool: mcp-2d-pipeline.composite
      params:
        animation: "{{inbetween.output}}"
        background: "{{background.output}}"
        effects: ["godray", "dust_particles", "warm_grade"]
        
    # 8. Quality Check (検査)
    - name: verify
      tool: mcp-ojev.verify_temporal_consistency
      params:
        asset_ids: "{{composite.frame_ids}}"
        
    - name: evaluate_final
      tool: mcp-ojev.verify_asset_quality
      params:
        asset_id: "{{composite.output}}"
        criterion: "ghibli_aesthetic"
```

---

## 新規に追加すべき研究論文（J系統）

| ID | 論文 | 検索キーワード | 重要性 |
|---|---|---|---|
| J01 | "Anime Sketch Colorization with Limited References" | sketch colorization, few-shot | ⭐⭐⭐ |
| J02 | "Style-Aware Color Transfer for Animation" | style transfer, color palette | ⭐⭐⭐ |
| J03 | "Procedural Cloud Rendering in Anime Style" | cloud, procedural, anime | ⭐⭐ |
| J04 | "Temporal Consistency in Anime Style Transfer" | temporal, style transfer, video | ⭐⭐⭐ |
| J05 | "Learning from Ghibli: Artistic Style Transfer with Hierarchical Palette" | ghibli, palette, hierarchical | ⭐⭐ |
| J06 | "Automatic ScreenTone Classification for Manga" | screentone, manga, classification | ⭐⭐ |
| J07 | "Depth-aware Background Generation for Animation" | depth, background, anime | ⭐⭐⭐ |
| J08 | "Neural Inbetweening with Line Art Preservation" | inbetweening, line art | ⭐⭐⭐ |

---

## 詳細ソース

### 一次ソース（制作ドキュメント側）
1. 宮崎駿『出発点 1979〜1996』（講談社, 1996）— 絵コンテの考え方
2. 宮崎駿『折り返し点 1997〜2008』（岩波書店, 2008）— 色彩と光の哲学
3. 「スタジオジブリの現場 〜アニメ制作の秘密〜」（NHK, 2005）— 制作フロー
4. 高畑勲『映画を作りながら考えたこと』（徳間書店, 1991）— レイアウト論

### 技術発表
1. [SIGGRAPH Asia 2023 — Anime Production Techniques](https://asia.siggraph.org/)
2. [CVF — Anime Colorization Papers](https://openaccess.thecvf.com/)

### 学術論文（推定）
| タイトル | 推定venue | 推定arXiv |
|---|---|---|
| "Paints-Undo: Understanding Realistic Painting Behaviors" | arXiv 2024 | 2501.--- |
| "AnimeRun: 2DAnimation Visual Correspondence" | CVPR | 2403.--- |
| "ToonCrafter: Generative Cartoon Interpolation" | arXiv 2024 | 2405.--- |
| "DiffSketching: Sketch Control in Diffusion" | SIGGRAPH | 2311.--- |

---

## 照合状態
- [x] 制作ドキュメント・インタビュー確認
- [ ] AniDoc (P33) の一次ソース精読
- [ ] AniDepth (P34) のSIGGRAPH論文入手
- [ ] J01-J08 のarXiv検索実行（ユーザーのGoogle Scholar検索推奨）
- [ ] 男鹿和雄画集から色彩パターン抽出（手動）

---

## 卒制との最大的接合点

**「ジブリパイプラインは、人間の『判断』が各工程に入る構造。A2Aエージェントはその判断をモデル化する」**

- 色指定 → `mcp-lms` の palette recommendation
- 原画チェック → `mcp-ojev` の quality verification
- レイアウト差し戻し → `IfNode` + `feedback_to_director`
- 背景美術 → `mcp-2d-pipeline` の style-conditioned generation

この接合が、既存のP01 AniMEやP33 AniDocには存在しない**「人間の美学的判断の自律化」**というnoveltyを生む。
