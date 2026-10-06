"""Light DB wrapper for the DISNEY-QUOTES corpus."""

import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'disney-quotes.db')


class Corpus:
    def __init__(self, path=DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def quotes(self, **filt):
        """Return quotes filtered by theme tag or minimum confidence.

        Confidence is the best (max) recorded source confidence for the quote;
        quotes with no recorded source score 0.0.
        """
        where = []
        params = []
        if filt.get('tags'):
            where.append("instr(q.theme_tags, ?) > 0")
            params.append(filt['tags'])
        sql = """
            SELECT q.*,
                   (SELECT ROUND(COALESCE(MAX(qs.confidence), 0.0), 2)
                    FROM quote_sources qs WHERE qs.quote_id = q.id) AS confidence,
                   (SELECT GROUP_CONCAT(x, ', ') FROM (
                        SELECT DISTINCT s.type AS x
                        FROM quote_sources qs JOIN sources s ON qs.source_id = s.id
                        WHERE qs.quote_id = q.id
                    )) AS source_types
            FROM quotes q
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY confidence DESC, q.quote_key"
        self._cur.execute(sql, params)
        rows = self._cur.fetchall()
        if filt.get('min_confidence') is not None:
            rows = [r for r in rows if (r['confidence'] or 0) >= filt['min_confidence']]
        return rows

    def details(self):
        """Return quotes with nested source/concept/operation lists.

        Used by scripts/build-site.py. SQLite rejects `GROUP_CONCAT(DISTINCT expr,
        separator)`, so the aggregates are assembled here instead of in SQL.
        """
        rows = []
        for q in self.quotes():
            qid = q['id']
            d = {k: q[k] for k in q.keys()}
            self._cur.execute(
                "SELECT s.ref, s.type, s.title, s.author, s.year, s.page, s.url, "
                "       qs.strength, qs.confidence "
                "FROM quote_sources qs JOIN sources s ON qs.source_id = s.id "
                "WHERE qs.quote_id = ? ORDER BY qs.confidence DESC",
                (qid,),
            )
            d['sources'] = [dict(r) for r in self._cur.fetchall()]
            self._cur.execute(
                "SELECT c.name, c.definition, qc.strength "
                "FROM quote_concepts qc JOIN concepts c ON qc.concept_id = c.id "
                "WHERE qc.quote_id = ? "
                "ORDER BY CASE qc.strength WHEN 'STRONG' THEN 0 WHEN 'MEDIUM' THEN 1 ELSE 2 END, c.name",
                (qid,),
            )
            d['concepts'] = [dict(r) for r in self._cur.fetchall()]
            self._cur.execute(
                "SELECT o.op_code, o.name, o.description "
                "FROM quote_operations qo JOIN operations o ON qo.op_id = o.id "
                "WHERE qo.quote_id = ? ORDER BY o.op_code",
                (qid,),
            )
            d['operations'] = [dict(r) for r in self._cur.fetchall()]
            rows.append(d)
        return rows

    def stats(self):
        """Return corpus-level counters for the site header."""
        c = self._cur
        c.execute("SELECT COUNT(*) FROM quotes")
        quotes = c.fetchone()[0]
        c.execute("""
            SELECT COUNT(*) FROM quotes q
            WHERE NOT EXISTS (SELECT 1 FROM quote_sources qs WHERE qs.quote_id = q.id)
        """)
        no_source = c.fetchone()[0]
        c.execute("SELECT COUNT(DISTINCT source_id) FROM quote_sources")
        cited = c.fetchone()[0]
        c.execute("SELECT ROUND(AVG(confidence), 3) FROM ("
                  "SELECT MAX(confidence) AS confidence FROM quote_sources GROUP BY quote_id)")
        avg = c.fetchone()[0] or 0.0
        c.execute("SELECT COUNT(*) FROM concepts")
        concepts = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM operations")
        operations = c.fetchone()[0]
        return {
            'quotes': quotes,
            'no_source': no_source,
            'cited_sources': cited,
            'avg_confidence': avg,
            'concepts': concepts,
            'operations': operations,
        }

    def pipeline(self, key=None):
        """Return the full 5-stage pipeline row for a quote key.

        NOTE: SQLite rejects `GROUP_CONCAT(DISTINCT expr, separator)`, so each
        aggregate is a subquery: dedupe with DISTINCT inside, then concatenate.
        """
        sql = """
            SELECT q.quote_key, q.text_en, q.author,
                   (SELECT GROUP_CONCAT(x, '; ') FROM (
                        SELECT DISTINCT s.ref || ':' || qs.strength || '(' || ROUND(qs.confidence, 2) || ')' AS x
                        FROM quote_sources qs JOIN sources s ON qs.source_id = s.id
                        WHERE qs.quote_id = q.id
                    )) AS sources,
                   (SELECT GROUP_CONCAT(x, ', ') FROM (
                        SELECT DISTINCT c.name AS x
                        FROM quote_concepts qc JOIN concepts c ON qc.concept_id = c.id
                        WHERE qc.quote_id = q.id
                    )) AS concepts,
                   (SELECT GROUP_CONCAT(x, ' | ') FROM (
                        SELECT DISTINCT o.op_code || ': ' || o.description AS x
                        FROM quote_operations qo JOIN operations o ON qo.op_id = o.id
                        WHERE qo.quote_id = q.id
                    )) AS operations
            FROM quotes q
        """
        if key:
            sql += " WHERE q.quote_key = ?"
        self._cur.execute(sql, (key,) if key else ())
        return self._cur.fetchone()

    def pipeline_all(self, key=None):
        """Return every quote's 5-stage pipeline rows."""
        sql = """
            SELECT q.quote_key, q.text_en, q.author,
                   (SELECT GROUP_CONCAT(x, '; ') FROM (
                        SELECT DISTINCT s.ref || ':' || qs.strength || '(' || ROUND(qs.confidence, 2) || ')' AS x
                        FROM quote_sources qs JOIN sources s ON qs.source_id = s.id
                        WHERE qs.quote_id = q.id
                    )) AS sources,
                   (SELECT GROUP_CONCAT(x, ', ') FROM (
                        SELECT DISTINCT c.name AS x
                        FROM quote_concepts qc JOIN concepts c ON qc.concept_id = c.id
                        WHERE qc.quote_id = q.id
                    )) AS concepts,
                   (SELECT GROUP_CONCAT(x, ' | ') FROM (
                        SELECT DISTINCT o.op_code || ': ' || o.description AS x
                        FROM quote_operations qo JOIN operations o ON qo.op_id = o.id
                        WHERE qo.quote_id = q.id
                    )) AS operations
            FROM quotes q
        """
        if key:
            sql += " WHERE q.quote_key = ?"
        self._cur.execute(sql, (key,) if key else ())
        return self._cur.fetchall()

    def export_jsonl(self, out):
        """Export all quotes + mappings to JSONL."""
        rows = self.pipeline_all()
        with open(out, 'w', encoding='utf-8') as f:
            for r in rows:
                obj = {
                    'key': r['quote_key'],
                    'en': r['text_en'],
                    'author': r['author'],
                    'sources': [s.strip() for s in (r['sources'] or '').split(';') if s.strip()],
                    'concepts': [c.strip() for c in (r['concepts'] or '').split(',') if c.strip()],
                    'operations': [o.split(':')[0].strip() for o in (r['operations'] or '').split('|')],
                }
                f.write(json.dumps(obj, ensure_ascii=False) + '\n')

    def check(self):
        """Return a list of validation error messages (schema integrity only)."""
        errors = []
        cur = self._cur
        cur.execute("SELECT COUNT(*) FROM quotes")
        if cur.fetchone()[0] == 0:
            errors.append("quotes table is empty")
        cur.execute("""
            SELECT q.quote_key FROM quotes q
            LEFT JOIN quote_concepts qc ON q.id = qc.quote_id
            LEFT JOIN concepts c ON qc.concept_id = c.id
            WHERE c.name IS NULL
        """)
        for (key,) in cur.fetchall():
            errors.append(f"{key}: concept mapping references missing concept")
        cur.execute("""
            SELECT q.quote_key FROM quotes q
            LEFT JOIN quote_operations qo ON q.id = qo.quote_id
            LEFT JOIN operations o ON qo.op_id = o.id
            WHERE o.op_code IS NULL
        """)
        for (key,) in cur.fetchall():
            errors.append(f"{key}: operation mapping references missing operation")
        return errors
