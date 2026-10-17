# AIアニメ映画制作システム — Reference / Generation / JEV / TPS-Gate

> 生成をお呪いから科学へ、錬金術から工場へ。

AIアニメ映画制作のための再利用可能な設計資料。HTML / SVG / Mermaid / PlantUML / YAML を同じ概念モデルから管理する。

## 中心モデル

- **Reference** — 何を作るか。物語・キャラクター・世界観・絵コンテなどの正本と参照コンテクスト。
- **Generation** — どう生成するか。モデル、条件、レシピ、実行記録、候補を保存し、再現・比較できるようにする。
- **Eval / JEV** — 何を合格とするか。命題・証拠・評価基準・スコア・確信度に基づいて検査し、判断する。
- **Production System / TPS-Gate** — どう完成まで流すか。工程ゲートを管理し、不合格素材を次工程へ流さず、手戻り・待ち・重複生成・廃棄を減らす。

## 成果物

- [HTML overview](./production-system.html)
- [SVG architecture](./production-system.svg)
- [Mermaid diagram](./production-system.mmd)
- [PlantUML diagram](./production-system.puml)
- [Canonical YAML](./production-system.yaml)

## 基本フロー

企画・世界観 → 脚本 → キャラクター／美術設定 → 絵コンテ／アニマティック → ショット生成 → Eval/JEV → 編集／合成 → 音響／音楽 → 最終QC／納品。

不合格時は原因に応じて該当工程へ戻す。毎回すべてを再生成しない。

## GATE

- **Gate A — Spec / Reference readiness:** 仕様・参照資料が制作可能な状態か。
- **Gate B — Asset inspection:** キャラクター一貫性、構図、破綻、意図への適合。
- **Gate C — Shot inspection:** ショット間連続性、タイミング、動き、音声。
- **Gate D — Delivery inspection:** 映像・音声・字幕・形式・権利。

## KPI

- First-pass yield（初回合格率）
- Final yield（最終合格率）
- Rework rate（手戻り率）
- Cost per accepted shot（合格ショットあたりコスト。生成費＋修正工数）
- Canon consistency rate（正本設定との一貫性）

## データ原則

メディア本体とメタデータは分離する。RAG は検索・取得のために使い、正本（canon/source of truth）そのものにはしない。構造化データを正本とし、検索結果は出典・版・確信度を確認して利用する。

## 設計原則

Reference が制作対象を定義し、Generation が候補を作り、JEV/Eval が合否を判断し、TPS/Gate が完成までの流れを管理する。各層を疎結合にし、モデルを交換しても正本・品質基準・工程管理を失わない。
