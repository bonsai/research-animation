# P05 Iterative Refinement Improves Compositional Image Generation

## 300字要約

構成画像生成を反復リファインメントで改善する手法。VLM を critic として生成→評価→修正のループに組み込み、compute-matched 並列サンプリングで効率化。ConceptMix all-correct で +16.9%、T2I-CompBench 3D-Spatial で +13.8%、人手選好でも 58.7% vs 41.3% と勝る。生成物をループに入れる根拠となる。
