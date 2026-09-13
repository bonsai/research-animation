# Research Question

## Main RQ

**アニメ映画の制作現場では、どのような言葉によって「映画を作るための状態・変化・関係・時間」が記述されてきたのか。特に東映動画の資料・文献から特徴的な制作語彙を抽出し、それらの構造からアニメ映画のオントロジーを帰納できるか。**

本研究では、一般的なアニメーション用語を最初から ontology に当てはめない。まず文献資料から実際に使われた言葉を回収し、東映動画／東映アニメーションの制作実践において、その言葉が何を指し、どの工程・役割・判断・変化を接続していたのかを分析する。

## Research Network — 日本アニメーション学会

本研究では、**日本アニメーション学会をアニメーション研究の文献ネットワークへの接続点**として位置づける。

日本アニメーション学会の『アニメーション研究』および関連する研究資料は、東映動画を含む日本のアニメーション制作史・制作技術・制作体制を調査するための重要な文献群である。特に Database for Animation Studies と接続し、学会誌・研究資料・インタビュー等から制作語彙を回収する。

```text
日本アニメーション学会
        ↓
『アニメーション研究』
        ↓
Database for Animation Studies
        ↓
東映動画に関する研究資料・証言・論文
        ↓
制作語彙の抽出
        ↓
アニメ映画 ontology
```

ここで学会は「正解を与える権威」としてではなく、**一次資料・研究資料へ到達するための文献ネットワーク**として扱う。

### Literature Network

```text
日本アニメーション学会
        │
        ├── 『アニメーション研究』
        │
        ├── アニメーション研究資料
        │
        └── Database for Animation Studies
                 │
                 ├── 東映動画
                 ├── 作画・演出
                 ├── 撮影技術
                 ├── 制作体制
                 └── 制作史

        ↓

CiNii / 国立国会図書館 / その他書誌DB
        ↓

文献横断
        ↓

語彙・概念・制作実践の抽出
```

### Research Protocol Extension

文献DBを単なる検索場所ではなく、**制作 ontology を発掘するための観測装置**として扱う。

```text
学会・研究資料
 ↓
文献DB
 ↓
資料群の発見
 ↓
本文・証言の確認
 ↓
TERM
 ↓
CONTEXT
 ↓
PRODUCTION FUNCTION
 ↓
ONTOLOGY CANDIDATE
```

Database for Animation Studies には、東映動画についての研究資料、制作体制、撮影技術、作画枚数制限、演出法などの文献が収録されている。高畑勲による1960年代東映動画の制作体制研究、吉村次郎への撮影部インタビュー、渡部英雄による3500枚制限の研究などを起点とする。

## Sub RQ

### RQ1 — 語彙

東映動画の制作資料・研究文献では、どのような独自または特徴的な言葉が使われていたのか。

候補例：

- 作画監督
- 演出
- 原画
- 動画
- レイアウト
- カメラアングル
- カメラワーク
- シート
- 撮影上がり
- 透過光効果
- 特殊効果
- 作画枚数制限
- 長編製作
- 制作体制

ここでは「日本アニメ一般の用語」と「東映動画で特に意味を持った用語」を区別する。特に「作画監督」は、東映動画が初めて定着させたとされる役職として、制作システム上の重要語彙候補にする。

### RQ2 — 言葉の意味

各語は単なる名称ではなく、制作上のどのような操作・判断・責任を表していたのか。

```text
TERM
 ↓
WHO / WHAT
 ↓
PRODUCTION ROLE
 ↓
DECISION
 ↓
STATE CHANGE
```

ontology 化は研究側の仮説であり、資料上の意味と分離して記録する。

### RQ3 — 制作体制

東映動画の制作体制は、どのような役割分担によってアニメ映画の状態を構成していたのか。

高畑勲の研究では、一人のチーフ・アニメーターの強い指導下で、多数のアニメーターが各シーンを作画し、チーフがレイアウト、カメラアングル、カメラワークを決定する体制が論じられている。

```text
INTENTION
 ↓
DIRECTION
 ↓
LAYOUT
 ↓
DRAWING
 ↓
CAMERA
 ↓
COMPOSITING
 ↓
FILM
```

### RQ4 — 時間

「シート」「原画」「動画」などの語は、動きをどのように時間として記述していたのか。

```text
STATE A
 ↓
KEY STATE
 ↓
INTERMEDIATE STATE
 ↓
STATE B
 ↓
TIME SHEET
```

既存 ontology の `STATE / DIFFERENCE / TRANSFORMATION / TIME / SEQUENCE` が、日本の制作実践にどこまで対応するかを検証する。

### RQ5 — 制約と表現

東映動画における制作上の制約は、単なるコスト削減ではなく、映像表現をどのように変化させたのか。

1984年の3500枚制限についての研究では、作画枚数の制限が日本独自の視覚表現の発展につながったと論じられている。

```text
CONSTRAINT
 ↓
PRODUCTION DECISION
 ↓
REDUCTION / SELECTION
 ↓
VISUAL STRATEGY
 ↓
STYLE
```

### RQ6 — 撮影と言葉

東映動画の撮影部では、マルチプレーン撮影、フィルター、透過光効果など、技術の用途を拡張する実践が行われていた。技術名がどのように映画的操作の言葉へ変わったのかを問う。

```text
DEVICE
 ↓
TECHNIQUE
 ↓
EFFECT
 ↓
PERCEPTION
 ↓
CINEMATIC MEANING
```

### RQ7 — 映画としての最小単位

東映アニメーションの工程説明では、文章を「映像の最小単位であるカット」に置き換え、その積み重ねによって物語を見せるという制作観が示されている。

ここから、既存 ontology の `ENTITY / STATE / SEQUENCE` と、映画固有の `CUT / SHOT / SCENE / SEQUENCE` の関係を再検討する。

```text
SCRIPT
 ↓
CUT
 ↓
SHOT / IMAGE / ACTION
 ↓
SEQUENCE
 ↓
FILM
```

### RQ8 — 東映語彙からアニメ映画 ontology へ

文献から抽出した語彙を、どのような抽象概念へ変換できるか。

```text
DOCUMENTED TERM
 ↓
ORIGINAL CONTEXT
 ↓
FUNCTION
 ↓
RELATION
 ↓
ONTOLOGICAL CANDIDATE
 ↓
GENERATION OPERATION
```

候補例：

```text
作画監督 → ROLE / COORDINATION
レイアウト → SPATIAL STATE / STAGING
シート → TIME / TEMPORAL CONTROL
原画 → KEY STATE
動画 → TRANSITION / INTERMEDIATE STATE
撮影 → COMPOSITING / PERCEPTION
特殊効果 → TRANSFORMATION / PERCEPTION
カット → CINEMATIC UNIT
```

これらは現時点では研究仮説である。

### RQ9 — 独自語彙の発見

「独自」とは何を意味するのかを分解する。

1. 東映動画が新しく作った言葉
2. 東映動画が特定の意味で定着させた言葉
3. 日本アニメ業界に広く存在した言葉
4. 映画・写真・印刷など他産業から移入した言葉
5. 後世の研究者が東映動画を説明するために使った言葉

この区別なしに「東映独自語」と断定しない。

### RQ10 — 文献DBを ontology の発掘装置として使えるか

Database for Animation Studies、CiNii、国立国会図書館等の文献DBから、東映動画に関係する資料を検索し、頻出語・特徴語・役職名・工程名・技術名・演出語を抽出できるか。

一般的なアニメーション用語についても、作品や会社によって独自のルールや用語が使われることが指摘されているため、標準語彙との比較を行う。

## Research Protocol

### 1. 文献回収

優先順位：

```text
東映動画一次資料
 ↓
元スタッフの証言・インタビュー
 ↓
東映動画を対象とする研究論文
 ↓
制作技法書・用語事典
 ↓
一般的なアニメーション研究
```

### 2. 語彙抽出

各資料から以下を抽出する。

```text
TERM
SOURCE
YEAR
AUTHOR / SPEAKER
ORIGINAL CONTEXT
DEFINITION
ROLE
PROCESS
RELATED TERMS
EVIDENCE LEVEL
```

### 3. ontology 候補化

```text
TERM
 ↓
THING / ROLE / STATE / RELATION / TRANSFORMATION / TIME / PERCEPTION
 ↓
GENERATION OPERATION
```

### 4. 比較

東映だけでなく、Disney / Pixar / 日本動画協会の語彙と比較する。

```text
TOEI
DISNEY
PIXAR
JAPANESE ANIME
      ↓
COMMON VOCABULARY
      ↓
DIFFERENT VOCABULARY
      ↓
DIFFERENT PRODUCTION MODELS
      ↓
ANIMATION FILM ONTOLOGY
```

## Working Hypothesis

**アニメ映画の ontology は、作品に登場する「物」だけではなく、制作現場が用いてきた「役割・状態・変化・時間・判断・知覚」の言葉から再構成できる。**

特に東映動画は、長編映画の制作体制、作画監督制度、レイアウト、カメラワーク、撮影技術、作画枚数制限などを通して、映画を組織的に生成するための日本独自の語彙とシステムを研究する重要なケースである。

したがって本研究では、**「アニメーションとは何か」を先に定義するのではなく、「アニメ映画を作る人々が何を区別し、何に名前を付けてきたか」を調べ、その語彙の構造から ontology を帰納する。**

## Case Positioning

- `anima` — 実作品による生成ケース
- `dots` — 状態変化の抽象ケース
- `Disney / Pixar` — 制作原則・システム・ツールの比較ケース
- `Toei Doga` — 日本のアニメ映画制作語彙・制作体制の歴史的ケース
- `research-animation` — これらを比較して ontology を構築する理論本体

```text
anima
  ↓
FRAME / CHANGE

dots
  ↓
STATE / DIFFERENCE

Disney / Pixar
  ↓
PRODUCTION PRINCIPLES / SYSTEM / TOOLS

Toei Doga
  ↓
VOCABULARY / ROLES / PROCESS / CINEMATIC TECHNIQUE

        ↓
CHANGE ONTOLOGY
        ↓
ANIMATED FILM GENERATION THEORY
```

実装は研究本体へ持ち込まず、各ケースのリポジトリで管理する。

## Evidence Rules

1. 東映動画一次資料・元スタッフ証言・インタビューを優先する。
2. Database for Animation Studies、CiNii、国立国会図書館等で書誌と本文の所在を確認する。
3. 引用された言葉と研究者による説明を区別する。
4. 「東映独自語」という主張には比較資料を要求する。
5. 現代の東映アニメーションの用語と、東映動画時代の歴史的用語を分離する。
6. 文献上の語義と、本研究による ontology 化を分離する。
7. `TERM → SOURCE → CONTEXT → FUNCTION → ONTOLOGY → GENERATION OPERATION` の順に記録する。
