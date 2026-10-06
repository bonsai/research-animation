"""Quote harvest stub.

Hook for automated collection from:
  - D23 / official Disney sites (respecting robots.txt + rate limits)
  - quote books metadata (OpenLibrary API)
  - academic citation databases

Currently provides a few EXAMPLE harvest jobs that you extend.
Never scrape without verifying robots.txt and applying a min-delay.
"""

import json
from datetime import datetime, timezone

# --- Example harvest jobs (extend this list) -------------------------------

def harvest_disney_co():
    """Example: candidate quotes from the Walt Disney Company quote page.

    Returns dicts with keys: en, confidence, ref, type, notes.
    """
    return [
        {
            "en": "All our dreams can come true, if we have the courage to pursue them.",
            "confidence": 0.1,
            "ref": "disneyco",
            "type": "website",
            "notes": "candidate - needs attribution verification; 'If you can dream it, you can do it' is a known misattribution.",
        },
    ]


def harvest_openlibrary(query="walt disney quotes"):
    """Example: query OpenLibrary / BookReader for quote-book metadata."""
    # Implement with requests.get('https://openlibrary.org/search.json?...')
    return []


# --- Runner ----------------------------------------------------------------

def main():
    jobs = [harvest_disney_co, harvest_openlibrary]
    out = []
    for job in jobs:
        try:
            rows = job()
        except Exception as exc:
            print(f"harvest {job.__name__} FAILED: {exc}")
            continue
        for r in rows:
            r['harvested_at'] = datetime.now(timezone.utc).isoformat()
        out += rows

    out.sort(key=lambda x: -x.get('confidence', 0))
    print(f"collected {len(out)} candidates")
    for r in out:
        print(f"  [{r.get('confidence')}] {r['en'][:70]} ...")
    with open('corpus/candidates.jsonl', 'w', encoding='utf-8') as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    return out


if __name__ == '__main__':
    main()
