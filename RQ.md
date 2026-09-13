# Research Question

## Main RQ

Pixar における映画制作のシステムとツールは、アイデア・物語・キャラクター・ショット・時間・編集を、どのように表現し、接続し、反復的に変化させているのか。そして、その構造をアニメ映画生成の理論としてどこまで抽象化できるのか。

## Research Focus

本研究では Pixar の個別ソフトウェアを単なる「便利な制作ツール」として調査するのではなく、**ツールが映画制作の思考をどのようなデータ・状態・関係・操作として表現しているか**を調べる。

```text
IDEA
 ↓
STORY
 ↓
CHARACTER / WORLD
 ↓
SHOT / SCENE
 ↓
BLOCKING / ANIMATION
 ↓
LIGHT / CAMERA / SIMULATION
 ↓
EDIT / REVIEW
 ↓
ITERATION
 ↓
FILM
```

## Sub RQ

### RQ1 — 制作システム

Pixar の制作工程は、どのような役割・工程・データの受け渡しによって構成されているか。

### RQ2 — デジタル表現

Pixar の制作ツールは、キャラクター・環境・カメラ・光・運動・ショットなどを、どのような状態として表現しているか。

### RQ3 — ツールと言語

Pixar のツール名・制作概念・専門用語には、映画を設計するためのどのような「言葉」が埋め込まれているか。

### RQ4 — 状態と差分

制作工程における修正・レビュー・バージョン・反復は、状態 A と状態 B の差分、およびその差分を生む操作として記述できるか。

### RQ5 — ショット

Pixar の制作システムにおいて、ショットは単なる画像や動画ファイルではなく、時間・カメラ・演技・音・編集などが関係する生成単位として扱われているか。

### RQ6 — 編集とフィードバック

Story Reel、Editorial、レビューなどの工程は、生成した映像を評価し、次の状態を決めるフィードバックループとして記述できるか。

### RQ7 — ツール間連携

異なる制作ツールが共有するデータ構造・シーン表現・アセット表現・時間表現は何か。それらは映画生成の共通中間表現として抽象化できるか。

### RQ8 — 人間とシステム

Pixar の制作システムでは、人間の判断とツールによる計算・生成・可視化がどのように分担されているか。

### RQ9 — 生成

Pixar の制作システムを参照することで、アニメ映画生成を「画像を生成する問題」から「映画の状態・関係・変化を構成し、評価し、反復する問題」へ再定義できるか。

## Tool Research Targets

調査対象は、確認できる一次・準一次資料を優先する。

- RenderMan — レンダリング
- Presto — アニメーション制作システム
- USD / Universal Scene Description — シーン・アセット・データ交換
- OpenUSD ecosystem — 複雑な3D制作データの構造化
- Marionette — キャラクター／リギング等の技術的基盤
- Ringmaster / パイプライン関連システム — 制作工程の管理・自動化
- Editorial / Story Reel — ショットを時間軸上で評価・再構成する仕組み
- Pixar の production pipeline に関する公開資料

※ ツール名・用途・年代は資料ごとに検証し、現在のPixar内部システムと過去の研究開発システムを混同しない。

## System Research Axes

### 1. Data

何がデータとして存在するか。

```text
ASSET
SCENE
SHOT
FRAME
CAMERA
CHARACTER
ANIMATION
LIGHT
SIMULATION
AUDIO
EDIT
```

### 2. State

各工程で何が「状態」として保存されるか。

### 3. Relation

アセット・ショット・キャラクター・カメラ・時間・編集の間にどのような関係があるか。

### 4. Transformation

制作中に、どの操作が状態を別の状態へ変換するか。

### 5. Time

フレーム、ショット、シークエンス、編集点、タイミングをどのように表現するか。

### 6. Perception

制作システムの内部表現が、最終的な観客の知覚・感情・意味へどう接続されるか。

### 7. Iteration

生成 → レビュー → 修正 → 再生成のループが、どのようにシステム化されているか。

## Ontology Bridge

Pixar の実際の用語と本研究の ontology を混同しない。

```text
PIXAR TERM / SYSTEM
        ↓
DOCUMENTED MEANING
        ↓
PRODUCTION FUNCTION
        ↓
STATE / RELATION / DIFFERENCE / TRANSFORMATION / TIME
        ↓
CANDIDATE ONTOLOGY
        ↓
GENERATION OPERATION
```

例：

```text
SHOT
 ↓
映画上の時間的・知覚的単位
 ↓
STATE + TIME + RELATION
 ↓
bounded cinematic event
```

```text
EDITORIAL
 ↓
ショットを時間軸上で構成・評価・変更
 ↓
SEQUENCE + TIME + PERCEPTION
 ↓
reorder / trim / compare / evaluate
```

```text
USD
 ↓
シーン・アセット・関係を記述する共通表現
 ↓
ENTITY + STATE + RELATION
 ↓
compose / reference / transform
```

```text
ITERATION
 ↓
状態を評価して次の状態を生成
 ↓
DIFFERENCE + TRANSFORMATION + FEEDBACK
 ↓
generate → evaluate → modify → regenerate
```

これらは現時点では**研究仮説**であり、Pixar がこの ontology を採用しているという意味ではない。

## Case Positioning

`anima` は、静止画からフレーム列を生成する具体的ケース。

`dots` は、抽象的な状態と差分を扱うケース。

Pixar research は、両者をより大きな**映画制作システム**へ接続するための実務・技術ドメイン研究として位置付ける。

```text
anima
  ↓
FRAME / CHANGE

 dots
  ↓
STATE / DIFFERENCE

Pixar systems
  ↓
ASSET / SHOT / TIME / RELATION / ITERATION

        ↓
CHANGE ONTOLOGY
        ↓
ANIMATED FILM GENERATION THEORY
```

## Research Principle

Pixar の「すごいツール」を列挙することが目的ではない。

重要なのは、**映画を作るために何を記述可能にし、何を変更可能にし、何を比較可能にし、何を再利用可能にしているのか**を明らかにすることである。

最終的な問いは、

> 映画生成エージェントに必要なのは、画像生成器だけなのか。それとも、Pixar の制作システムが扱ってきたような「状態・関係・時間・編集・評価・反復」を扱う制作システムそのものなのか。

である。

## Evidence Rules

1. Pixar 公式資料・Pixar Research・技術論文・SIGGRAPH 等の一次資料を優先する。
2. 現行ツールと歴史的ツールを分離する。
3. Pixar が公開している事実と、本研究による理論的解釈を分離する。
4. ツール名だけで ontology primitive を決めない。
5. 技術機能だけでなく、制作工程上の役割を記録する。
6. 同じ概念が複数ツールにまたがる場合は、共通する抽象構造を調べる。
7. 「ツール → データ → 操作 → 映画上の意味」の4層で記述する。
