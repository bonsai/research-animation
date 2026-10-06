"""Generate the static quote viewer from the corpus DB (no external deps).

Server-renders every card so the page works without JavaScript; the search box
and the strength filter are progressive enhancement on top of it.
"""

import sys
import os
import html as _html

here = os.path.dirname(os.path.abspath(__file__))
corpus = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(corpus, "corpus"))

from database import Corpus

OUT = os.path.join(corpus, 'site')

STRENGTHS = ('PRIMARY', 'SECONDARY', 'TERTIARY')


def e(v):
    return _html.escape('' if v is None else str(v))


def top_strength(sources):
    """Best (strongest) source strength recorded for a quote."""
    levels = {s['strength'] for s in sources}
    for lv in STRENGTHS:
        if lv in levels:
            return lv
    return 'NONE'


def source_row(s):
    bits = []
    if s['author']:
        bits.append(e(s['author']))
    if s['year']:
        bits.append(e(s['year']))
    if s['page']:
        bits.append('p.' + e(s['page']))
    meta = ', '.join(bits)
    title = e(s['title'])
    if s['url']:
        title = f'<a href="{e(s["url"])}">{title}</a>'
    return f'''
            <li>
              <span class="badge lv-{e(s['strength'])}">{e(s['strength'])}</span>
              <span class="ref">{e(s['ref'])}</span>
              <span class="src-title">{title}</span>
              <span class="src-meta">{meta}</span>
              <span class="src-conf">{s['confidence']:.2f}</span>
            </li>'''


def quote_card(q):
    sources = q['sources']
    concepts = q['concepts']
    ops = q['operations']
    levels = sorted({s['strength'] for s in sources}) or ['NONE']
    level = next((lv for lv in STRENGTHS if lv in levels), 'NONE')

    search_blob = ' '.join(filter(None, [
        q['quote_key'], q['text_en'], q['text_ja'] or '', q['author'] or '',
        q['theme_tags'] or '', q['context'] or '',
        ' '.join(c['name'] for c in concepts),
        ' '.join(o['op_code'] for o in ops),
        ' '.join(s['ref'] for s in sources),
    ])).lower()

    meta_bits = []
    if q['year']:
        meta_bits.append(f"year {e(q['year'])}")
    if q['context']:
        meta_bits.append(e(q['context']))

    src_html = (
        '<ul class="sources">' + ''.join(source_row(s) for s in sources) + '</ul>'
        if sources else
        '<p class="no-source">No source recorded — attribution unverified. '
        'Hypothesis only; must not be cited as evidence.</p>'
    )
    concept_html = ''.join(
        f'<span class="chip cs-{e(c["strength"])}" title="{e(c["definition"])}">'
        f'{e(c["name"])}<em>{e(c["strength"])}</em></span>'
        for c in concepts
    )
    op_html = ''.join(
        f'<li><code>{e(o["op_code"])}</code> {e(o["description"])}</li>' for o in ops
    )
    tags = [t.strip() for t in (q['theme_tags'] or '').split(',') if t.strip()]
    tags_html = ''.join(f'<span class="tag">{e(t)}</span>' for t in tags)
    note = f'<p class="note">{e(q["notes"])}</p>' if q['notes'] else ''

    return f'''
    <article class="quote-card" data-search="{e(search_blob)}"
             data-levels="{e(' '.join(levels))}"
             data-conf="{q['confidence'] or 0:.2f}" data-key="{e(q['quote_key'])}">
      <h3>
        <span class="qkey">{e(q['quote_key'])}</span>
        <span class="conf">conf {q['confidence'] or 0:.2f}</span>
      </h3>
      <blockquote class="en">&ldquo;{e(q['text_en'])}&rdquo;</blockquote>
      <p class="author">&mdash; {e(q['author'])}</p>
      {f'<p class="meta">{meta_bits[0]} &middot; {meta_bits[1]}</p>' if len(meta_bits) == 2 else (f'<p class="meta">{meta_bits[0]}</p>' if meta_bits else '')}
      {f'<p class="ja">{e(q["text_ja"])}</p>' if q['text_ja'] else ''}
      {note}
      <div class="section">
        <h4>Provenance</h4>
        {src_html}
      </div>
      <div class="section">
        <h4>Concepts</h4>
        <div class="chips">{concept_html}</div>
      </div>
      <div class="section">
        <h4>Operations</h4>
        <ul class="ops">{op_html}</ul>
      </div>
      <div class="tags">{tags_html}</div>
    </article>'''


def catalog_row(q):
    level = top_strength(q['sources'])
    return (f'<tr><td><code>{e(q["quote_key"])}</code></td>'
            f'<td>{e(q["text_en"][:90])}{"&hellip;" if len(q["text_en"]) > 90 else ""}</td>'
            f'<td>{e(q["year"] or "")}</td>'
            f'<td class="lv-cell lv-{e(level)}">{e(level)}</td>'
            f'<td>{q["confidence"] or 0:.2f}</td>'
            f'<td>{e(q["theme_tags"] or "")}</td></tr>')


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(corpus, 'disney-quotes.db')
    db = Corpus(path)
    errors = db.check()
    if errors:
        print("Corpus validation failed; see scripts/validate.py")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    quotes = db.details()
    st = db.stats()

    cards = '\n'.join(quote_card(q) for q in quotes)
    rows = '\n'.join(catalog_row(q) for q in quotes)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DISNEY-QUOTES CORPUS</title>
<link rel="stylesheet" href="static/style.css">
</head>
<body>
<header>
<div class="hero" aria-hidden="true"></div>
<div class="hero-text">
<h1>DISNEY-QUOTES CORPUS</h1>
<p>ディズニー名言を、アニメ映画生成の理論に接続する研究用コーパス。<br>
QUOTE &rarr; SOURCE/CONTEXT &rarr; DOMAIN CONCEPT &rarr; ONTOLOGICAL CANDIDATE &rarr; GENERATION OPERATION</p>
<ul class="stats">
  <li><b>{st['quotes']}</b> quotes</li>
  <li><b>{st['cited_sources']}</b> sources cited</li>
  <li><b>{st['concepts']}</b> concepts</li>
  <li><b>{st['operations']}</b> operations</li>
  <li>avg confidence <b>{st['avg_confidence']:.2f}</b></li>
  <li class="warn"><b>{st['no_source']}</b> without source</li>
</ul>
<p><a href="../viz/index.html">&rarr; network graph (quote &harr; concept &harr; operation)</a></p>
</div>
</header>

<div class="controls">
  <input id="q" type="search" placeholder="search text / key / tag / concept&hellip;" autocomplete="off">
  <select id="level">
    <option value="">all sources</option>
    <option value="PRIMARY">has PRIMARY</option>
    <option value="SECONDARY">has SECONDARY</option>
    <option value="TERTIARY">has TERTIARY</option>
    <option value="NONE">no source</option>
  </select>
  <select id="sort">
    <option value="conf">sort: confidence</option>
    <option value="key">sort: key</option>
    <option value="year">sort: year</option>
  </select>
  <span id="count">{len(quotes)} / {len(quotes)}</span>
  <button id="reset" type="button">reset</button>
</div>

<main>
<h2 id="quotes">Quotes</h2>
<div id="cards">
{cards}
</div>

<h2 id="catalog">Catalog</h2>
<table>
<thead><tr><th>key</th><th>quote</th><th>year</th><th>best source</th><th>conf</th><th>tags</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>

<h2 id="legend">Provenance legend</h2>
<table class="legend">
<thead><tr><th>level</th><th>meaning</th></tr></thead>
<tbody>
<tr><td class="lv-cell lv-PRIMARY">PRIMARY</td><td>contemporaneous record (interview, broadcast, transcript).</td></tr>
<tr><td class="lv-cell lv-SECONDARY">SECONDARY</td><td>later publication quoting the statement.</td></tr>
<tr><td class="lv-cell lv-TERTIARY">TERTIARY</td><td>quote aggregator with no traceable intermediary.</td></tr>
<tr><td class="lv-cell lv-NONE">NONE</td><td>attribution unverified &mdash; hypothesis only.</td></tr>
</tbody>
</table>
</main>

<footer>DISNEY-QUOTES CORPUS &mdash; quotes are hypotheses, not attributed theory.
See <code>docs/PROVENANCE.md</code> and <code>docs/PROVENANCE-AUDIT.md</code>.</footer>

<script>
(function () {{
  var cards = Array.prototype.slice.call(document.querySelectorAll('.quote-card'));
  var box = document.getElementById('q');
  var level = document.getElementById('level');
  var sort = document.getElementById('sort');
  var count = document.getElementById('count');
  var wrap = document.getElementById('cards');

  function apply() {{
    var needle = box.value.trim().toLowerCase();
    var want = level.value;
    var shown = 0;
    cards.forEach(function (c) {{
      var okText = !needle || c.dataset.search.indexOf(needle) !== -1;
      var levels = (c.dataset.levels || '').split(/\\s+/);
      var okLevel = !want || levels.indexOf(want) !== -1;
      var vis = okText && okLevel;
      c.style.display = vis ? '' : 'none';
      if (vis) shown++;
    }});
    count.textContent = shown + ' / ' + cards.length;
  }}

  function resort() {{
    var mode = sort.value;
    cards.sort(function (a, b) {{
      if (mode === 'key') return a.dataset.key < b.dataset.key ? -1 : 1;
      if (mode === 'year') {{
        var ay = a.querySelector('.meta'), by = b.querySelector('.meta');
        var av = ay ? ay.textContent : '', bv = by ? by.textContent : '';
        return av < bv ? -1 : (av > bv ? 1 : 0);
      }}
      return parseFloat(b.dataset.conf) - parseFloat(a.dataset.conf);
    }});
    cards.forEach(function (c) {{ wrap.appendChild(c); }});
  }}

  box.addEventListener('input', apply);
  level.addEventListener('change', apply);
  sort.addEventListener('change', function () {{ resort(); apply(); }});
  document.getElementById('reset').addEventListener('click', function () {{
    box.value = ''; level.value = ''; sort.value = 'conf'; resort(); apply();
  }});
}})();
</script>
</body>
</html>'''

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {os.path.join(OUT, 'index.html')} ({len(quotes)} quotes, "
          f"{st['no_source']} without source)")
    db.close()


if __name__ == '__main__':
    main()