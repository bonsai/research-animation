# Experiments — 実験記録ガイドライン

本ディレクトリは `RQ.md` に定義された研究質問を検証する実験の定義・記録・成果物を置く。

## 命名規則

```
EXP-{EVAL|LOOP|COLLAPSE|PREF}-{NNN}.md   実験定義書
{RNNN}-RUN-{NNNN}/                       実験実行ディレクトリ
  ├── manifest.json                       実験条件と結果
  ├── images/                             生成画像
  ├── observations.md                     観察記録
  └── evaluation.json                     評価スコア
```

## 実験定義書のテンプレート

各実験は以下の項目を含む Markdown で定義する。

```markdown
# EXP-XXX-NNN — 実験タイトル

## 対象RQ
## 統制群
## 仮説
## 方法
## 使用モデル・ツール
## インプット設定
## 出力指標
## 判定基準（成功/失敗）
## 結果（実行後に記入）
## 次の実験への示唆
```

## 規約

1. **Observation ≠ Interpretation**
2. **Evidence は source と分離して記録**
3. **マニフェストは JSON で機械可読に**
4. **再現性を最優先**（シード、バージョン、パラメータの完全記録）

## 既存実験

- `archive/EXP-ARCH-001.md` — 建築アニメーション（PyVista）。本テーマの直接対象外だが、プロシージャル評価の参考。

---
*EXP 一覧は本ファイルに追記していく。*
