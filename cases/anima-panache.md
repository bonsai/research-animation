# Case Study: anima / PANACHE

## Position

`anima` は、research-animation における **絵コンテ駆動型アニメーション** の実践事例として位置づける。

研究対象は「生成AIで動画を直接生成すること」ではなく、**静止画の連続を状態変化として設計し、固定FPSで時間軸へ変換する方法**。

## 実例

2026/09/13 の PANACHE 告知用ローファイアニメーション。

- 1〜16コマ: りんごが小さい状態から徐々に巨大化
- 17〜32コマ: 巨大なりんごが少しずつ齧られる
- 32コマ × 4fps = 8秒
- 480×360 / H.264 / yuv420p
- ストーリーボード上のフレーム番号は動画化時に除去

## 方法

画像生成側には「動きそのもの」を要求せず、複数コマの絵コンテを作る。
その後、コマを読み順に切り出し、固定FPSで連結してMP4化する。

つまり、

`storyboard → frame extraction → temporal assembly → video`

という小さなパイプラインである。

## 研究上の意味

`research-animation` の dots PoC が「状態遷移を最小単位から研究する」なら、`anima` は「実際の映像作品を状態変化として組み立てる」側のケースである。

| 軸 | anima / PANACHE | dots PoC |
|---|---|---|
| 入力 | 絵コンテPNG | 状態パラメータ |
| 変化 | 人間が設計したコマ列 | awによる状態遷移 |
| 描画 | storyboard frame | Pillow |
| 時間 | 固定FPS | frame sequence |
| 出力 | MP4 / GIF | GIF |
| 目的 | 作品化 | 変化の原理研究 |

## 重要な発見

アニメーションを「動画生成」と捉えず、**変化の設計 + 時間への配置**として扱える。

この考え方は、今後 `random / rule / Markov / LLM` などで変化を生成する research-animation の実験へ接続できる。

## Source

実装本体: https://github.com/bonsai/anima

元README: https://github.com/bonsai/anima/blob/main/README.md

関連スクリプト: `scripts/make_panache_8s.py`
