-- DISNEY-QUOTES CORPUS SCHEMA
-- 5-stage pipeline: QUOTE -> SOURCE/CONTEXT -> CONCEPT -> ONTOLOGY -> GENERATION OPERATION

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref TEXT NOT NULL UNIQUE,          -- e.g. "marling1991", "bright1987", "walker1982"
    type TEXT NOT NULL,                -- book / article / website / speech / biography
    title TEXT NOT NULL,
    author TEXT,
    year INTEGER,
    url TEXT,
    page TEXT,                          -- specific page, if any
    notes TEXT
);

CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_key TEXT NOT NULL UNIQUE,     -- slug, e.g. "one_mouse"
    text_en TEXT NOT NULL,              -- original English quote
    text_ja TEXT,                       -- Japanese translation (optional)
    author TEXT NOT NULL,               -- usually "Walt Disney", may vary
    year INTEGER,                       -- estimated utterance year (NULL if unknown)
    context TEXT,                       -- setting / occasion (e.g. "1964 interview")
    theme_tags TEXT,                    -- comma-separated: story,character,animation,...
    notes TEXT                          -- e.g. attribution warnings
);

CREATE TABLE IF NOT EXISTS quote_sources (
    quote_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    strength TEXT NOT NULL,             -- PRIMARY / SECONDARY / TERTIARY / UNKNOWN
    confidence REAL NOT NULL DEFAULT 0.0,  -- 0.0-1.0 provenance confidence
    PRIMARY KEY (quote_id, source_id),
    FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,          -- e.g. ORIGIN, ENTITY, CONTINUITY
    domain TEXT NOT NULL,               -- category of the concept
    definition TEXT,
    related_principle TEXT,             -- mapping to a Disney 12 Principles number/name
    notes TEXT
);

CREATE TABLE IF NOT EXISTS quote_concepts (
    quote_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    strength TEXT NOT NULL,             -- STRONG / WEAK / CONSIDER
    PRIMARY KEY (quote_id, concept_id),
    FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE,
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE TABLE IF NOT EXISTS operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    op_code TEXT NOT NULL UNIQUE,       -- e.g. MAINTAIN_ORIGIN, TRANSFORM_CONSTRAINT
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL              -- DESIGN / GENERATION / EVALUATION / REFINEMENT
);

CREATE TABLE IF NOT EXISTS quote_operations (
    quote_id INTEGER NOT NULL,
    op_id INTEGER NOT NULL,
    rationale TEXT,                     -- why this operation follows from the quote
    PRIMARY KEY (quote_id, op_id),
    FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE,
    FOREIGN KEY (op_id) REFERENCES operations(id)
);

-- Views for the 5-stage pipeline queries
CREATE VIEW v_quote_pipeline AS
SELECT
    q.quote_key,
    q.text_en,
    GROUP_CONCAT(s.ref || ':' || qs.strength, ';') AS sources,
    GROUP_CONCAT(c.name, ',') AS concepts,
    GROUP_CONCAT(o.op_code, ',') AS operations
FROM quotes q
LEFT JOIN quote_sources qs ON q.id = qs.quote_id
LEFT JOIN sources s ON qs.source_id = s.id
LEFT JOIN quote_concepts qc ON q.id = qc.quote_id
LEFT JOIN concepts c ON qc.concept_id = c.id
LEFT JOIN quote_operations qo ON q.id = qo.quote_id
LEFT JOIN operations o ON qo.op_id = o.id
GROUP BY q.id;
