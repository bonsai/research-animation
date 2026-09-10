# research-animation

SD 1.5で大量の小さな静止画を生成し、再生時にランダムなテンポを与えてコマドリアニメーションを研究する。

## Local SD

既存のローカルSD環境を利用する。想定モデルルートは `/home/bons/.sd`。
生成器はSD WebUI互換の `POST /sdapi/v1/txt2img` を利用するため、WebUI側のモデル配置をそのまま使える。

SD 1.5は512×512を中心に学習されたモデルなので、PoCでは128×128の極小画像を狙う。小サイズは研究用の速度優先であり、画質を目的にしない。 citeturn0search3

## PoC

### 1. Frame Poolを生成

```bash
python research/generate_frames.py \
  --prompt "a tiny hand-drawn animation frame" \
  --count 100 \
  --width 128 \
  --height 128
```

出力:

```text
frames/
├── 000001.png
├── 000002.png
├── ...
├── frames.csv
└── frames.json
```

`frames.csv` は素材DB、`frames.json` は生成条件・seed等の詳細なprovenance。

### 2. 再生レシピを作る

```bash
python research/playback.py \
  --frames frames/frames.csv \
  --count 30 \
  --seed 42 \
  --min-fps 2 \
  --max-fps 7
```

出力:

```text
playback/playback.json
```

生成時にはFPSを決めない。同じFrame Poolから `playback_seed` を変えることで別のアニメーションを作れる。

## Architecture

```text
local SD 1.5
    ↓
Frame Pool
    ├── PNG
    ├── frames.csv
    └── frames.json
          ↓
    playback.py
          ↓
playback.json
  frame + random 2–7 fps
          ↓
     renderer
          ↓
      animation
```

次段階で `playback.json` をMP4/GIFへレンダリングする。
