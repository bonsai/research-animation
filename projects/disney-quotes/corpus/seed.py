"""DISNEY-QUOTES CORPUS SEED SCRIPT

Reads the seed quotes from `seed_data.json` and initializes the corpus DB,
creating tables, sources, concepts and operation library.
"""

import sqlite3
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(here), 'disney-quotes.db')
SCHEMA_PATH = os.path.join(here, 'schema.sql')

# ---------------------------------------------------------------------------
# Sources (reference database)
# ---------------------------------------------------------------------------

SOURCES = [
    # --- confirmed (cited in seed_data.json) -------------------------------
    ("marling1991", "article", "Disneyland, 1955: Just Take the Santa Ana Freeway to the American Dream",
     "Karal Ann Marling", 1991, None, "American Art 5(3)", "opening-of-dayland, 1955"),
    ("walker1982", "book", "Animated Architecture", "Derek Walker", 1982, None, "p.10",
     "AUDIT2026: 'as quoted in' — 转述であり一次記録ではない。no_genius / fun_impossible の同一段落。"),
    ("disneyland_story_1954", "broadcast", "The Disneyland Story (television program)",
     "Walt Disney", 1954, None, None,
     "one_mouse の最古の記録。放送日 1954-10-27。放送そのものは一次記録 (recording)。"),
    ("richardson2004", "book", "The Story of Disney", "Neal Gabler / Robert B. Sherman ほか", 2004, None, "p.41",
     "one_mouse の変形形を収める。"),
    ("qwd2001", "book", "The Quotable Walt Disney", "Dave Smith (ed.)", 2001, None, None,
     "Disney Book Group。公式編纂集だが一次記録ではない。laughter_export / grow_up / stay_with_idea の出典。"),
    ("kurtti2008", "book", "Walt Disney World: Then, Now, & Forever", "Jeff Kurtti", 2008, None, None,
     "grow_up の延長形の出典。"),
    ("hammond1996", "book", "The Stuff Americans Are Made Of", "Joshua Hammond / James Morrison", 1996, None, None,
     "dreams_collateral の出典。旧記録の bright1987 を置換。"),
    ("zupanic2007", "article", "COSI exhibit explores world of cartoons", "Jeffrey Zupanic", 2007, None,
     "The Review, 2 August 2007", "animation_medium の出典。"),
    ("klein1998", "book", "Seven Minutes: The Life and Death of the American Animated Cartoon",
     "Norman M. Klein", 1998, None, "p.48", "character_personality の出典。"),
    ("rost2006", "book", "OpenGL Shading Language", "Randi J. Rost", 2006, None, "p.411",
     "animation_communication の出典。技術書からの引用。"),
    ("nyt1938", "newspaper", "（記事本文・原文未特定）", "Walt Disney", 1938, None, "The New York Times, March 1938",
     "nyt_personality_1938 の出典。記事タイトルと頁は未特定。"),
    ("pixar_story2008", "book", "The Pixar Story", "Ed Catmull / Amy Collins ほか", 2008, None, None,
     "pixar_child_1938 の出典。録音 statement (1938) の転載。"),
    ("robinson2007", "film", "Meet the Robinsons (end credits)", None, 2007, None, None,
     "curiosity_paths の出典（as quoted in）。"),
    ("imdb_quotes", "website", "IMDb — Walt Disney quotes", None, None, None, "https://www.imdb.com/name/nm0000382/",
     "TERTIARY。引用者不明。"),
    ("disney_meetings2019", "website", "Disney Meetings blog", None, 2019, None, None,
     "TERTIARY。引用者不明。"),
    # --- rejected / unconfirmed (audit trail, no longer cited) ------------
    ("bright1987", "book", "Disneyland: Inside Story", "Randy Bright", 1987, None, "p.103",
     "AUDIT2026: 旧記録が dreams_collateral に割り当てていた出典。p.103 の独立確認に失敗し採用せず。"),
    ("thomas1978", "book", "Walt Disney: An American Original", "Bob Thomas", 1978, None, None,
     "AUDIT2026: 旧記録が no_genius に割り当てていた出典。年報の 1976/1978 2 説あり。Walker 1982 p.10 を採用。"),
    ("tdq", "book", "The Official Walt Disney Quote Book", None, None, None, None,
     "AUDIT2026: 旧記録が one_mouse に割り当てていた出典。公式書（Staff of the Walt Disney Archives, 2023, ISBN 9781368061872）は特定できたが、対象文の収録は未確認。"),
    ("disneyco", "website", "The Walt Disney Company — Walt quote", None, None,
     "https://thewaltdisneycompany.com", None,
     "AUDIT2026: 引用URLが特定できない。one_mouse の出典を disneyland_story_1954 に置換。"),
    ("d23", "website", "D23 — Disney production history", None, None, "https://d23.com", None,
     "保留。具体的引用箇所が必要。"),
]

# concept: (id, name, domain, definition, related_principle, notes)
CONCEPTS = [
    ("ORIGIN", "origin", "創作の出発点",
     "巨大なシステムになっても、創作の原点となった小さなアイデアを保持する最小の創作単位。"),
    ("ENTITY", "entity", "生成単位",
     "生成系における最小の自律的な出力単位（キャラクター、ショット、シーン）。"),
    ("CONTINUITY", "continuity", "連続性",
     "複数生成物間の整合性を保ちながら進化する性質。"),
    ("CONSTRAINT", "constraint", "制約",
     "表現を制限する条件。制約は排除対象ではなく、創造の触媒。"),
    ("POSSIBILITY", "possibility", "可能性",
     "制約之下で開ける表現の空間。"),
    ("TRANSFORMATION", "transformation", "変換",
     "制約を新しい表現操作へ変える操作。"),
    ("PERCEPTION", "perception", "知覚",
     "生成物の評価を内部的な正しさではなく『観客にどう知覚されるか』で行う基準。"),
    ("AUDIENCE", "audience", "観客",
     "受動的な受け手ではなく、想像力を持つ主体としての観客。"),
    ("EVALUATION", "evaluation", "評価",
     "生成物に対する評価基準とプロセス。"),
    ("COLLABORATION", "collaboration", "協働",
     "個人ではなく役割分担・編集・統合による制作システム。"),
    ("COORDINATION", "coordination", "調整",
     "複数の生成エージェント間の調整。"),
    ("SYSTEM", "system", "システム",
     "万能な一個の天才ではなく、全体として機能する生成アーキテクチャ。"),
    ("EMOTION", "emotion", "感情",
     "情報を介さずに伝達される感情的な意味。"),
    ("COMMUNICATION", "communication", "伝達",
     "感情を介した意味の伝達。"),
    ("CULTURAL TRANSMISSION", "cultural_transmission", "文化伝播",
     "笑いや価値観が文化を越えて伝わる性質。"),
    ("ENTERTAINMENT", "entertainment", "娯楽",
     "楽しみの中での学び。"),
    ("LEARNING", "learning", "学習",
     "意味を直接説明せず、知覚・感情・物語を通して生じさせる学び。"),
    ("STORY", "story", "物語",
     "アニメーションを超えて映画として成立するためのストーリー構造。"),
    ("VISUAL", "visual", "視覚",
     "視覚的エンターテインメントの設計。"),
    ("IMAGINATION", "imagination", "想像",
     "大人になりすぎない想像力を保持する姿勢。"),
    ("PLAY", "play", "遊び",
     "遊び心ある主体性。"),
    ("CHARACTER", "character", "キャラクター",
     "個々のキャラクターの表現。"),
    ("IDENTITY", "identity", "正体・個性",
     "他者との差異を設計することで生まれる個性。"),
    ("DIFFERENCE", "difference", "差異",
     "属性の組み合わせではなく、他との差異を設計する問題。"),
    ("DREAM", "dream", "夢",
     "未形・非実体のアイデア・ビジョン。"),
    ("MATERIALIZATION", "materialization", "実体化",
     "想像したものを状態・構造・工程へ変換して実体化する性質。"),
    ("IMPLEMENTATION", "implementation", "実装",
     "実現に向けた具体的な変換。"),
    ("ITERATION", "iteration", "反復",
     "生成 → 評価 → 修正 → 再生成のループ。"),
    ("REFINEMENT", "refinement", "磨き込み",
     "アイデアを完成形まで追う操作。"),
    ("COMPLETION", "completion", "完了",
     "手を加えすぎないで完成として出す判断。"),
    ("EXPLORATION", "exploration", "探索",
     "最適解の一発探索ではなく、探索空間を広げるプロセス。"),
    ("SEARCH", "search", "探索",
     "探索空間の拡大。"),
]

# operation: (id, op_code, name, description, category)
OPERATIONS = [
    ("MAINTAIN_ORIGIN", "MAINTAIN_ORIGIN", "Origin の保持",
     "大規模生成系でも作品を成立させた最小の核（origin）を明示的に保持・参照する。"),
    ("TRANSFORM_CONSTRAINT", "TRANSFORM_CONSTRAINT", "制約の変換",
     "制約を排除せず、制約から新しい表現操作を創出する。"),
    ("OPEN_POSSIBILITY", "OPEN_POSSIBILITY", "可能性空間の開放",
     "'不可能'を可能とする操作空間を先に設計する。"),
    ("PERCEPTION_EVAL", "PERCEPTION_EVAL", "知覚基準評価",
     "生成物の評価を『観客にどう知覚されるか』で行う。"),
    ("AUDIENCE_SUBJ", "AUDIENCE_SUBJ", "観客の主体化",
     "観客を受動的受け手から想像的主体へ設計し直す。"),
    ("SYSTEM_DESIGN", "SYSTEM_DESIGN", "システム設計",
     "万能な一個の天才ではなく役割分担・統合による生成系として設計する。"),
    ("EMOTION_BRIDGE", "EMOTION_BRIDGE", "感情ブリッジ",
     "意味を感情を介して伝達する操作を設計する。"),
    ("ENTERTAIN_LEARN", "ENTERTAIN_LEARN", "娯楽を通じた学び",
     "直接説明せず、知覚・感情・物語を通して意味を生じさせる。"),
    ("IMAGINE_FREE", "IMAGINE_FREE", "想像の解放",
     "成人化した既成観念を排し、想像力を主体として扱う。"),
    ("DESIGN_DIFFERENCE", "DESIGN_DIFFERENCE", "差異の設計",
     "属性の組み合わせではなく、他者との差異を設計対象にする。"),
    ("MATERIALIZE", "MATERIALIZE", "実体化",
     "イメージを状態・構造・工程へ変換して実体化する。"),
    ("ITERATE", "ITERATE", "反復",
     "生成 → 評価 → 修正 → 再生成のループを設計・実行する。"),
    ("EXPAND_SEARCH", "EXPAND_SEARCH", "探索空間の拡大",
     "最適解の一発探索ではなく探索空間を広げる。"),
]


def main():
    if os.path.exists(DB_PATH):
        print(f"Database already exists at {DB_PATH}. Remove it to re-seed.")
        return

    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    # --- sources
    for s in SOURCES:
        cur.execute(
            "INSERT INTO sources (ref, type, title, author, year, url, page, notes) VALUES (?,?,?,?,?,?,?,?)",
            s,
        )

    # --- concepts
    for c in CONCEPTS:
        cur.execute(
            "INSERT INTO concepts (name, domain, definition, related_principle, notes) VALUES (?,?,?,?,?)",
            (c[0], c[1], c[2], None, c[3]),
        )

    # --- operations
    for o in OPERATIONS:
        cur.execute(
            "INSERT INTO operations (op_code, name, description, category) VALUES (?,?,?,?)",
            (o[0], o[1], o[2], o[3]),
        )

    # --- seed quotes with their mappings
    seed = json.load(open(os.path.join(here, 'seed_data.json'), encoding='utf-8'))
    for q in seed:
        cur.execute(
            "INSERT INTO quotes (quote_key, text_en, text_ja, author, year, context, theme_tags, notes) VALUES (?,?,?,?,?,?,?,?)",
            (q['key'], q['en'], q.get('ja'), q['author'], q.get('year'), q.get('context'), q.get('tags'), q.get('notes')),
        )
        qid = cur.lastrowid
        for ref, strength in q.get('sources', []):
            cur.execute(
                "INSERT INTO quote_sources (quote_id, source_id, strength, confidence) "
                "SELECT ?, s.id, ?, ? FROM sources s WHERE s.ref = ?",
                (qid, strength, q.get('confidence', 0.5), ref),
            )
        for code, strength in q.get('concepts', []):
            cur.execute(
                "INSERT INTO quote_concepts (quote_id, concept_id, strength) "
                "SELECT ?, c.id, ? FROM concepts c WHERE c.name = ?",
                (qid, strength, code),
            )
        for op_code in q.get('operations', []):
            cur.execute(
                "INSERT INTO quote_operations (quote_id, op_id) "
                "SELECT ?, o.id FROM operations o WHERE o.op_code = ?",
                (qid, op_code),
            )

    conn.commit()
    print(f"Seeded {len(seed)} quotes into {DB_PATH}")


if __name__ == '__main__':
    main()
