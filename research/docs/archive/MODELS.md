# モデル台帳 & DL計画

対象テーマ: 文脈駆動Growing画像生成エージェント  
対象領域: アニメ・映画の実制作（Blender MVP / SVG PoC / Houdini further）

基準日: 2026-10-02

---

## ストレージ状況

| 場所 | 容量 | 使用 | 空き | 用途 |
|---|---|---|---|---|
| WSL `/home` | 1007 GB | 79 GB | 877 GB | ComfyUI / 学習 / コード |
| Windows `C:\` | 475 GB | 419 GB | 57 GB | LM Studio モデル |

**注意**: `C:\` は残り 57 GB しかない。LM Studio モデルは厳選する。

---

## 機械可読台帳

`models.jsonl` に同一内容を JSONL 形式で出力済み。

## 現在の所持モデル

### 画像生成（ComfyUI）

| モデル | 場所 | サイズ | 状態 | 用途 |
|---|---|---|---|---|
| `flux1-schnell-fp8.safetensors` | `/home/bons/mcp/comfy/ComfyUI/models/checkpoints/` | 17 GB | ✅ 利用可 | 高速生成ベースモデル |

### VLM / LLM（LM Studio）

| モデル | 場所 | サイズ | 状態 | 用途 |
|---|---|---|---|---|
| `gemma-4-E4B-it-Q4_K_M.gguf` + mmproj | `C:\Users\0501JP\.lmstudio\models\...` | 5.9 GB | ⚠️ 要確認 | テキスト or マルチモーダル |
| `TEMPURA-Qwen2.5-VL-3B-GGUF` | `C:\Users\0501JP\.lmstudio\models\...` | 3.2 GB | ✅ 利用可 | **VLM critic 本命** |

---

## 必要モデル（DL計画）

### Phase 0〜1: 実験設計（必須）

| 優先度 | モデル | 想定サイズ | 置き場 | 理由 |
|---|---|---|---|---|
| 🔴 高 | Qwen2.5-VL-3B-Instruct（標準版） | 3〜4 GB | LM Studio | VLM critic の標準的な選択。TEMPURA 版の代替 |
| 🟡 中 | SVG ベクトル化ツール類 | — | WSL | potrace / vtracer 等。モデルではなくツール |
| 🟡 中 | 線画抽出 / ControlNet | 1〜2 GB | ComfyUI | アニメ調 SVG 化の前段 |

### Phase 3〜4: 実装・評価

| 優先度 | モデル | 想定サイズ | 置き場 | 理由 |
|---|---|---|---|---|
| 🟡 中 | Flux.1 Dev / Anime チューンモデル | 17〜23 GB | WSL | Schnell より高品質。空きがあるので検討可 |
| 🟢 低 | アニメ特化 LoRA（事前学習済み） | 50〜200 MB | ComfyUI | 出力品質向上用 |
| 🟢 低 | 個人別 reward model | 自作 | WSL | RQ4。時間あれば |

### Phase 5: 応用（further）

| 優先度 | モデル | 想定サイズ | 置き場 | 理由 |
|---|---|---|---|---|
| ⚫ 保留 | Houdini 関連 | — | — | further のため現段階では不要 |

---

## DL 優先順位

1. **Qwen2.5-VL-3B-Instruct（標準版）**
   - `mradermacher/Qwen2.5-VL-3B-Instruct-GGUF` の Q4_K_M
   - 理由: VLM critic は実験の核。TEMPURA 版が特殊調整されている可能性があるため、標準版も確保
   - 注意: C: 残り容量を圧迫するため、DL 後に不要モデル削除も検討

2. **線画抽出用 ControlNet / Canny model**
   - ComfyUI 標準対応の Canny/Lineart モデル
   - 理由: SVG PoC の前段処理として必須

3. **Flux Dev / アニメ特化モデル**
   - 理由: Schnell だけでは品質不足の可能性
   - 注意: 17 GB 以上消費。本当に必要か Phase 1 終了時に再判断

---

## 整理すべきこと

- [x] `Qwen2.5-VL-3B-Instruct` の未完了 DL をクリーンアップ
- [ ] `gemma-4-E4B-it` が VLM かテキストモデルか確認
- [ ] ComfyUI venv 再作成完了待ち
- [ ] ベクトル化ツール（potrace / vtrager）を WSL にインストール
- [ ] C: ドライブ空き監視（残り 50 GB を切ったら追加 DL 停止）

---

## 履歴

- 2026-10-02: 初版。所持モデル整理と DL 優先順位を作成
