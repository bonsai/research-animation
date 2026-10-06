# Generation Operations — DISNEY-QUOTES CORPUS

5 段階ピラミッドの最下層。各名言が示唆する、**アニメ映画生成パイプラインでの具体操作**のライブラリ。

## カテゴリ

- `DESIGN` — 生成アーキテクチャの設計方針
- `GENERATION` — フレーム・ショット生成の実行操作
- `EVALUATION` — 生成物の評価基準
- `REFINEMENT` — 生成結果の修正・反復

## 操作一覧

| code | name | category | 内容 |
|---|---|---|---|
| MAINTAIN_ORIGIN | Origin の保持 | DESIGN | 大規模生成系でも作品を成立させた最小の核（origin）を明示的に保持・参照する |
| TRANSFORM_CONSTRAINT | 制約の変換 | DESIGN | 制約を排除せず、制約から新しい表現操作を創出する |
| OPEN_POSSIBILITY | 可能性空間の開放 | DESIGN | `'不可能'`を可能とする操作空間を先に設計する |
| PERCEPTION_EVAL | 知覚基準評価 | EVALUATION | 生成物の評価を『観客にどう知覚されるか』で行う |
| AUDIENCE_SUBJ | 観客の主体化 | DESIGN | 観客を受動的受け手から想像的主体へ設計し直す |
| SYSTEM_DESIGN | システム設計 | DESIGN | 万能な一個の天才ではなく役割分担・統合による生成系として設計する |
| EMOTION_BRIDGE | 感情ブリッジ | GENERATION | 意味を感情を介して伝達する操作を設計する |
| ENTERTAIN_LEARN | 娯楽を通じた学び | GENERATION | 直接説明せず、知覚・感情・物語を通して意味を生じさせる |
| IMAGINE_FREE | 想像の解放 | DESIGN | 成人化した既成観念を排し、想像力を主体として扱う |
| DESIGN_DIFFERENCE | 差異の設計 | DESIGN | 属性の組み合わせではなく、他者との差異を設計対象にする |
| MATERIALIZE | 実体化 | GENERATION | イメージを状態・構造・工程へ変換して実体化する |
| ITERATE | 反復 | REFINEMENT | 生成 → 評価 → 修正 → 再生成のループを設計・実行する |
| EXPAND_SEARCH | 探索空間の拡大 | DESIGN | 最適解の一発探索ではなく探索空間を広げる |

## 運用

- 操作は `operations` テーブルで管理。新しい名言が既存操作に帰着しない場合、
  新規操作を `operations` に追加し、`quote_operations` で紐付ける。
- 操作の分類・記述は本ドキュメントと DB の両方で整合を取る。
