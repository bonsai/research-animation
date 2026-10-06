# Provenance Policy — DISNEY-QUOTES CORPUS

## 基本方針

- Walt Disney の言葉には**誤帰属・後世の要約・流通過程での改変**が多数含まれる。
- 本研究では「Disney がこの用語を使った」と主張せず、**観客にどう知覚されるか**という視点のみを
  生成理論のインスピレーションとして利用する。
- 出典が弱い引用は、`confidence` が低く記録され、**強く確からしい証拠が得られるまで仮扱い**とする。

## 誤帰属として特に注意

- **"If you can dream it, you can do it."** — Walt Disney の発言として安易に採用しない。
  誤帰属として知られており、このコーパスには含めない。
- "All our dreams can come true, if we have the courage to pursue them."
  同上の系列として要検証。

## 信頼性の付け方

| strength | confidence | 要件 |
|---|---|---|
| PRIMARY | 0.85–1.00 | 一次記録（インタビュー原稿、録音、自伝の該当ページ指定） |
| SECONDARY | 0.55–0.84 | 信頼できる伝記・研究書、ページ指定あり |
| TERTIARY | 0.25–0.54 | 名言集サイト、ページ未指定の書籍 |
| UNKNOWN | 0.00–0.24 | 出典不明 |

## 追跡優先順位

1. Walt Disney Archives, D23 の一次・準一次資料
2. 学術書・論文（Karal Ann Marling 1991 など）
3. 公式伝記（Bob Thomas 1978 など）
4. 公式名言集（*The Official Walt Disney Quote Book*）
5. ウェブ上の名言集

## 作業手順

収集スクリプトで得た候補は必ず `sources` テーブルに `ref` を作り、
`quote_sources` で `strength` と `confidence` を手動で設定してから採用する。
`strength IS NULL` の行は検証エラーとなる。
