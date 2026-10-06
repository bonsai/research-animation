"""Validate corpus integrity: schema, mappings, provenance coverage."""

import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
corpus = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(corpus, 'corpus'))

from database import Corpus

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(corpus, 'disney-quotes.db')
    if not os.path.exists(path):
        print(f"ERROR: corpus not found at {path}. Run: python scripts/init.py")
        sys.exit(1)

    db = Corpus(path)
    errors = db.check()

    # provenance summary
    cur = db._cur
    cur.execute("SELECT COUNT(*) FROM quotes")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM quote_sources")
    with_sources = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM quote_concepts")
    with_concepts = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM quote_operations")
    with_ops = cur.fetchone()[0]
    cur.execute("SELECT AVG(confidence) FROM quote_sources")
    avg_conf = cur.fetchone()[0] or 0

    print(f"quotes={total} with_sources={with_sources} with_concepts={with_concepts} "
          f"with_ops={with_ops} avg_confidence={avg_conf:.2f}")

    # no-source quotes are treated as UNKNOWN; report as warning only
    cur.execute("""
            SELECT q.quote_key FROM quotes q
            LEFT JOIN quote_sources qs ON q.id = qs.quote_id
            WHERE qs.strength IS NULL
        """)
    no_source = [k for (k,) in cur.fetchall()]
    if no_source:
        print(f"WARNING: with_no_source={len(no_source)} (no verified source recorded):")
        for k in no_source:
            print(f"  - {k}")
    else:
        print("with_no_source=0")

    if errors:
        print(f"\nVALIDATION FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        db.close()
        sys.exit(1)

    print("\nVALIDATION PASSED")
    db.close()


if __name__ == '__main__':
    main()
