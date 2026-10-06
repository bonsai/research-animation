# PROVENANCE AUDIT (2026-10-06)

出典追跡の結果。旧 seed の誤りを訂正し、16 quotes / 20 sources に更新した。
一次記録が見つからないものは `PRIMARY` にしない。

## Strength 定義

| level | 意味 |
|---|---|
| `PRIMARY` | 同時代の記録（放送・インタビュー・録音・公文） |
| `SECONDARY` | 後の出版物が発言を引用 |
| `TERTIARY` | 中間出典を追跡できない名言語集 |
| `NONE` | 帰属未確認。仮説としてのみ保持 |

## 1. テキストの訂正

| key | 旧 seed | 訂正後 | 根拠 |
|---|---|---|---|
| `grow_up` | "Too many people grow up. That's the real trouble with the world." | "That's the real trouble with the world, too many people grow up. They forget. They don't remember what it's like to be twelve years old. They patronize; they treat children as inferiors. I won't do that. I'll temper a story, yes. But I won't play down, and I won't patronize." | `qwd2001` / `kurtti2008` |
| `animation_medium` | 末尾 `...` で切断 | 全文 "…visual entertainment which can bring pleasure and information to people of all ages everywhere in the world." | `zupanic2007` |
| `curiosity_paths` | "because we're curious and curiosity keeps…" | "Around here, however, we don't look backwards for very long. … because we're curious… and curiosity keeps leading us down new paths." | `robinson2007` |
| `one_mouse` | "I only hope that we don't lose sight of one thing—that it was all started by a mouse."（2004 年の変体） | "Our only hope is we never lose sight of one thing: that it was all started by a mouse."（1954 年の放送） | `disneyland_story_1954` |

`grow_up` は旧来、語順が反転し後半が落ちていた。復元によって **patronize（見下すこと）を明確に拒む**という、
観客主体性の直接的な根拠が生まれた。

## 2. 出典の訂正と格下げ

| key | 旧 | 新 | 理由 |
|---|---|---|---|
| `fun_impossible` | `walker1982` **PRIMARY** | `walker1982` SECONDARY | Walker (1982) は "as quoted in" の転述であり一次記録ではない |
| `no_genius` | `thomas1978` SECONDARY | `walker1982` SECONDARY | 旧記録は Thomas (1978) を割り当てていた。Walker 1982 p.10 で `fun_impossible` と同一段落 |
| `dreams_collateral` | `bright1987` p.103, 0.85 | `hammond1996` 0.60 | Bright 1987 p.103 の独立確認に失敗。Wikiquote は *The Stuff Americans Are Made Of* (1996) を挙げる |
| `one_mouse` | `disneyco`（URL 不特定） | `disneyland_story_1954` | 引用 URL が特定できない。1954 年のテレビ番組が最古の記録 |
| `entertain_learn` | `tdq` | `imdb_quotes` / `disney_meetings2019` TERTIARY | 語順が二種流通。Wikiquote の一覧に収録されていない |

## 3. 未確認だった 6 件の現状

| key | 結果 | strength | confidence |
|---|---|---|---|
| `laughter_export` | *The Quotable Walt Disney* (2001, Dave Smith 編) まで確定。一次記録は未発見 | SECONDARY | 0.50 |
| `grow_up` | 同上と Kurtti (2008)。テキストも訂正済み | SECONDARY | 0.60 |
| `animation_medium` | Zupanic, *The Review*, 2007-08-02 | SECONDARY | 0.70 |
| `curiosity_paths` | *Meet the Robinsons* (2007) エンディングクレジット経由 | TERTIARY | 0.55 |
| `entertain_learn` | 追跡不能。語順が二種 | TERTIARY | 0.30 |
| `uniqueness` | **Wikiquote の一覧に存在しない**。語集サイト間の相互参照のみ | NONE | 0.20 |

`laughter_export` は、流通する長い版本が "Times and conditions change so rapidly that we must keep our aim
constantly focused on the future." で始まることから、原文はより長い可能性が高い。

## 4. 追跡の副産物として追加した 4 quotes

キャラクター生成理論に直接効くものを選んだ。

| key | 出所 | 価値 |
|---|---|---|
| `character_personality` | Klein, *Seven Minutes* (1998) p.48 | 「人格にならなければ、物語は観客に可信として響かない」＝ キャラクター生成の中核条件 |
| `nyt_personality_1938` | *The New York Times*, 1938-03 | 「動くだけの影は、公衆の感情応答を誘発しない」＝ 実体性の条件 |
| `animation_communication` | Rost, *OpenGL Shading Language* (2006) p.411 | アニメーションを伝達手段として扱う証拠 |
| `pixar_child_1938` | 録音 statement (1938)、*The Pixar Story* (2008) 経由 | 観客は年齢ではなく、全員に共通する「中の子供」 |

## 5. 誤帰属の記録

"If you can dream it, you can do it." は **Tom Fitzgerald**（Disney Imagineer）的 Words of Wisdom における言葉と、
*Ask Dave* (Dave Smith) 経由で流通している。この語句は corpus に**入れていない**。

## 6. 残る不安

- `disney_meetings2019` の URL と記事タイトルが未確定（TERTIARY なので許容）。
- `nyt1938` は記事タイトルと頁が未特定（「本文・原文未特定」として保持）。
- 6 件とも一次記録に到達していない。研究上の結論としては **hypothesis のまま**。

## 7. 検証手順

```
wsl.exe bash /home/bons/research-animation/projects/disney-quotes/run.sh --init
```

閲覧: `site/index.html`（検索・出典強度フィルタ付き）、`viz/index.html`（D3 ネットワーク）。
