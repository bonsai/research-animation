"""Build nodes/edges for the D3 force graph: QUOTE <-> CONCEPT <-> OPERATION."""

import sys
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
corpus = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(corpus, "corpus"))

from database import Corpus

OUT = os.path.join(corpus, 'viz', 'network.json')


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(corpus, 'disney-quotes.db')
    db = Corpus(path)
    nodes, edges = [], []
    seen_nodes, seen_edges = set(), set()

    for r in db.pipeline_all():
        key, en, author = r['quote_key'], r['text_en'], r['author']
        # quote node (label: key, full text truncated)
        nid = f"quote:{key}"
        if nid not in seen_nodes:
            nodes.append({
                "id": nid,
                "group": "quote",
                "label": key,
                "text": en[:80] + ("..." if len(en) > 80 else ""),
                "author": author,
            })
            seen_nodes.add(nid)
        # concept nodes & quote->concept edges
        for c in (r['concepts'] or '').split(','):
            if not c:
                continue
            cid = f"concept:{c}"
            if cid not in seen_nodes:
                nodes.append({"id": cid, "group": "concept", "label": c})
                seen_nodes.add(cid)
            e = (nid, cid)
            if e not in seen_edges:
                edges.append({"source": e[0], "target": e[1], "type": "quote_concept"})
                seen_edges.add(e)
        # operation nodes & quote->operation edges
        for op in (r['operations'] or '').split('|'):
            if not op.strip():
                continue
            opc = op.split(':')[0].strip()
            onid = f"op:{opc}"
            if onid not in seen_nodes:
                nodes.append({"id": onid, "group": "operation", "label": opc})
                seen_nodes.add(onid)
            e = (nid, onid)
            if e not in seen_edges:
                edges.append({"source": e[0], "target": e[1], "type": "quote_op"})
                seen_edges.add(e)

    out = {"nodes": nodes, "edges": edges, "summary": {
        "quotes": len([n for n in nodes if n['group'] == 'quote']),
        "concepts": len([n for n in nodes if n['group'] == 'concept']),
        "operations": len([n for n in nodes if n['group'] == 'operation']),
        "edges": len(edges),
    }}
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Wrote {OUT}: {out['summary']}")
    db.close()


if __name__ == '__main__':
    main()
