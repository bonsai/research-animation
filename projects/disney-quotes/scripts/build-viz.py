"""Build the network viewer by injecting network.json into the viz template.

Idempotent: always reads viz/template.html and writes viz/index.html.
"""

import os

here = os.path.dirname(os.path.abspath(__file__))
corpus = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
viz = os.path.join(corpus, 'viz')

tpl_path = os.path.join(viz, 'template.html')
out_path = os.path.join(viz, 'index.html')
net_path = os.path.join(viz, 'network.json')

if not os.path.exists(net_path):
    raise SystemExit(f"ERROR: {net_path} not found. Run: python scripts/graph-builder.py")

with open(tpl_path, 'r', encoding='utf-8') as f:
    tpl = f.read()
with open(net_path, 'r', encoding='utf-8') as f:
    net = f.read().strip()

if 'NETWORK_DATA' not in tpl:
    raise SystemExit(f"ERROR: placeholder NETWORK_DATA missing from {tpl_path}")

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(tpl.replace('NETWORK_DATA', net))
print(f"Built {out_path} from {net_path}")