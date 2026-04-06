#!/usr/bin/env python3
"""
enrich_preambles.py — Second-pass preamble enrichment for The Covenant Rendering.

Scans all 1,189 canonical Bible chapters and appends Extended Library
cross-references to each chapter's preamble.connections field wherever
substantive tradition data exists.
"""

import json
import os
import re
from collections import defaultdict

BASE = "/Users/aaronblonquist/The Covenant Rendering"

# ── Canonical book list with directory name and chapter count ──────────
CANON = [
    # Torah
    ("Genesis", "genesis", 50),
    ("Exodus", "exodus", 40),
    ("Leviticus", "leviticus", 27),
    ("Numbers", "numbers", 36),
    ("Deuteronomy", "deuteronomy", 34),
    # History
    ("Joshua", "joshua", 24),
    ("Judges", "judges", 21),
    ("Ruth", "ruth", 4),
    ("1 Samuel", "1-samuel", 31),
    ("2 Samuel", "2-samuel", 24),
    ("1 Kings", "1-kings", 22),
    ("2 Kings", "2-kings", 25),
    ("1 Chronicles", "1-chronicles", 29),
    ("2 Chronicles", "2-chronicles", 36),
    ("Ezra", "ezra", 10),
    ("Nehemiah", "nehemiah", 13),
    ("Esther", "esther", 10),
    # Poetry
    ("Job", "job", 42),
    ("Psalms", "psalms", 150),
    ("Proverbs", "proverbs", 31),
    ("Ecclesiastes", "ecclesiastes", 12),
    ("Song of Songs", "song-of-songs", 8),
    # Major Prophets
    ("Isaiah", "isaiah", 66),
    ("Jeremiah", "jeremiah", 52),
    ("Lamentations", "lamentations", 5),
    ("Ezekiel", "ezekiel", 48),
    ("Daniel", "daniel", 12),
    # Minor Prophets
    ("Hosea", "hosea", 14),
    ("Joel", "joel", 3),
    ("Amos", "amos", 9),
    ("Obadiah", "obadiah", 1),
    ("Jonah", "jonah", 4),
    ("Micah", "micah", 7),
    ("Nahum", "nahum", 3),
    ("Habakkuk", "habakkuk", 3),
    ("Zephaniah", "zephaniah", 3),
    ("Haggai", "haggai", 2),
    ("Zechariah", "zechariah", 14),
    ("Malachi", "malachi", 4),
    # NT — Gospels & Acts
    ("Matthew", "matthew", 28),
    ("Mark", "mark", 16),
    ("Luke", "luke", 24),
    ("John", "john", 21),
    ("Acts", "acts", 28),
    # NT — Pauline
    ("Romans", "romans", 16),
    ("1 Corinthians", "1-corinthians", 16),
    ("2 Corinthians", "2-corinthians", 13),
    ("Galatians", "galatians", 6),
    ("Ephesians", "ephesians", 6),
    ("Philippians", "philippians", 4),
    ("Colossians", "colossians", 4),
    ("1 Thessalonians", "1-thessalonians", 5),
    ("2 Thessalonians", "2-thessalonians", 3),
    ("1 Timothy", "1-timothy", 6),
    ("2 Timothy", "2-timothy", 4),
    ("Titus", "titus", 3),
    ("Philemon", "philemon", 1),
    # NT — General
    ("Hebrews", "hebrews", 13),
    ("James", "james", 5),
    ("1 Peter", "1-peter", 5),
    ("2 Peter", "2-peter", 3),
    ("1 John", "1-john", 5),
    ("2 John", "2-john", 1),
    ("3 John", "3-john", 1),
    ("Jude", "jude", 1),
    ("Revelation", "revelation", 22),
]

PENTATEUCH = {"Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"}
PENTATEUCH_DIRS = {"Genesis": "genesis", "Exodus": "exodus", "Leviticus": "leviticus",
                   "Numbers": "numbers", "Deuteronomy": "deuteronomy"}

# ── Helpers ────────────────────────────────────────────────────────────

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def parse_chapter_from_ref(reference, target_book):
    """Extract chapter number from a reference like 'Genesis 22:2' or 'Genesis 9:4-15'."""
    # Normalize target book name for matching
    ref = reference.strip()
    # Handle multi-word book names (1 Samuel, Song of Songs, etc.)
    # Try to match the book name at the start
    if not ref.startswith(target_book):
        return None
    rest = ref[len(target_book):].strip()
    if not rest:
        return None
    # rest should start with chapter number: "22:2" or "9:4-15" or just "22"
    m = re.match(r"(\d+)", rest)
    if m:
        return int(m.group(1))
    return None


def parse_book_chapter_from_ref(reference):
    """Extract (book_name, chapter_int) from a reference string."""
    ref = reference.strip()
    # Handle numbered books like "1 Samuel 16:3"
    m = re.match(r"^(\d\s+\w+|\w+(?:\s+of\s+\w+)?)\s+(\d+)", ref)
    if m:
        return m.group(1).strip(), int(m.group(2))
    # Psalms reference like "Psalm 14:1" -> book="Psalms", ch=14
    m = re.match(r"^Psalm\s+(\d+)", ref)
    if m:
        return "Psalms", int(m.group(1))
    return None, None


def count_variants_by_significance(verses, sig_levels=("theological", "major", "moderate")):
    """Count how many verses have variants at the given significance levels."""
    counts = defaultdict(int)
    for v in verses:
        if v.get("has_variant") and v.get("significance") in sig_levels:
            counts[v["significance"]] += 1
    return dict(counts)


def get_notable_variant_summary(verses, max_items=3):
    """Get a brief summary of the most significant variants in verse data."""
    items = []
    for v in verses:
        if v.get("has_variant") and v.get("significance") in ("theological", "major"):
            notes = v.get("variant_notes", [])
            note_text = notes[0] if notes else ""
            items.append((v["verse"], v.get("significance", ""), note_text))
    return items[:max_items]


# ── Pre-load all Extended Library indexes ──────────────────────────────

print("Loading Extended Library data...")

# 1. DSS Isaiah — per-chapter variant data
dss_data = {}  # ch_num -> {counts, notable_variants_preamble, variant_details}
for ch in range(1, 67):
    path = os.path.join(BASE, "dss-isaiah", f"chapter-{ch:02d}.json")
    if os.path.exists(path):
        d = load_json(path)
        counts = count_variants_by_significance(d.get("verses", []))
        notable = d.get("preamble", {}).get("notable_variants", "")
        details = get_notable_variant_summary(d.get("verses", []))
        dss_data[ch] = {"counts": counts, "notable": notable, "details": details}

# 2. LXX Jeremiah — per-chapter
lxx_jer_data = {}
for ch in range(1, 53):
    path = os.path.join(BASE, "lxx-jeremiah", f"jeremiah_{ch:02d}_lxx.json")
    if os.path.exists(path):
        d = load_json(path)
        counts = count_variants_by_significance(d.get("verses", []))
        preamble = d.get("preamble", {})
        notable = preamble.get("notable_variants", preamble.get("summary", ""))
        struct = preamble.get("structural_notes", "")
        details = get_notable_variant_summary(d.get("verses", []))
        lxx_jer_data[ch] = {"counts": counts, "notable": notable, "structural": struct, "details": details}

# 3. LXX Daniel — per-chapter
lxx_dan_data = {}
for ch in range(1, 13):
    path = os.path.join(BASE, "lxx-daniel", f"chapter-{ch:02d}.json")
    if os.path.exists(path):
        d = load_json(path)
        counts = count_variants_by_significance(d.get("verses", []))
        notable = d.get("preamble", {}).get("notable_variants",
                  d.get("preamble", {}).get("summary", ""))
        details = get_notable_variant_summary(d.get("verses", []))
        lxx_dan_data[ch] = {"counts": counts, "notable": notable, "details": details}

# LXX Daniel additions mapping (which canonical chapter they relate to)
lxx_dan_additions = {
    3: "The LXX inserts the Prayer of Azariah and the Song of the Three Young Men between verses 23 and 24, expanding the furnace scene with liturgical material that became central to Christian worship (the Benedicite).",
    13: "The LXX includes the story of Susanna (chapter 13 in the Greek), which was placed before Daniel 1 in Theodotion's recension, serving as a prelude to Daniel's wisdom.",
    14: "The LXX appends Bel and the Dragon (chapter 14), a polemical narrative against idol worship that provides additional Daniel stories absent from the MT."
}

# 4. LXX Esther — per-chapter
lxx_est_data = {}
for ch in range(1, 11):
    path = os.path.join(BASE, "lxx-esther", f"chapter-{ch:02d}.json")
    if os.path.exists(path):
        d = load_json(path)
        counts = count_variants_by_significance(d.get("verses", []))
        notable = d.get("preamble", {}).get("notable_variants",
                  d.get("preamble", {}).get("summary", ""))
        details = get_notable_variant_summary(d.get("verses", []))
        lxx_est_data[ch] = {"counts": counts, "notable": notable, "details": details}

# LXX Esther additions mapping to canonical chapters
# A = before ch 1, B = after 3:13, C = after 4:17, D = before 5:1, E = after 8:12, F = after 10:3
lxx_est_additions = {
    1: "Addition A (Mordecai's dream and the conspiracy) is placed before chapter 1 in the LXX, providing a theological and prophetic overture absent from the Hebrew text.",
    3: "Addition B (the king's edict of destruction) is inserted after 3:13 in the LXX, giving the full text of Haman's decree and explicitly invoking divine governance.",
    4: "Addition C (the prayers of Mordecai and Esther) follows 4:17 in the LXX, adding the only direct prayers to God in the book — transforming Esther from a secular narrative into a religious one.",
    5: "Addition D (Esther's audience with the king) replaces 5:1-2 in the LXX with an expanded, emotionally vivid scene emphasizing divine intervention in Esther's courage.",
    8: "Addition E (the king's counter-decree) follows 8:12 in the LXX, providing the full text of the decree reversing Haman's edict and acknowledging God's role.",
    10: "Addition F (interpretation of Mordecai's dream) closes the LXX book after 10:3, interpreting the dream from Addition A and providing explicit theological framing for the entire narrative."
}

# 5. Samaritan Pentateuch — per-book, index by (book, chapter)
sp_index = defaultdict(list)  # (book_name, ch) -> list of variant dicts
for book_name, fname in [("Genesis","genesis"),("Exodus","exodus"),("Leviticus","leviticus"),
                          ("Numbers","numbers"),("Deuteronomy","deuteronomy")]:
    path = os.path.join(BASE, "samaritan-pentateuch", f"{fname}.json")
    if os.path.exists(path):
        d = load_json(path)
        for v in d.get("variants", []):
            ch = parse_chapter_from_ref(v["reference"], book_name)
            if ch is not None:
                sp_index[(book_name, ch)].append(v)

# 6. Targum Onkelos — per-book, index by (book, chapter)
to_index = defaultdict(list)
for book_name, fname in [("Genesis","genesis"),("Exodus","exodus"),("Leviticus","leviticus"),
                          ("Numbers","numbers"),("Deuteronomy","deuteronomy")]:
    path = os.path.join(BASE, "targum-onkelos", f"{fname}.json")
    if os.path.exists(path):
        d = load_json(path)
        for r in d.get("renderings", []):
            ch = parse_chapter_from_ref(r["reference"], book_name)
            if ch is not None:
                to_index[(book_name, ch)].append(r)

# 7. Targum Jonathan — index by (book, chapter)
tj_index = defaultdict(list)
tj_files = {
    "isaiah": ["Isaiah"],
    "jeremiah": ["Jeremiah"],
    "ezekiel": ["Ezekiel"],
    "former-prophets": ["Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings"],
    "minor-prophets": ["Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah",
                        "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"],
}
for fname, books in tj_files.items():
    path = os.path.join(BASE, "targum-jonathan", f"{fname}.json")
    if os.path.exists(path):
        d = load_json(path)
        for r in d.get("renderings", []):
            book, ch = parse_book_chapter_from_ref(r["reference"])
            if book and ch:
                tj_index[(book, ch)].append(r)

# 8. Vulgate — index by (book, chapter)
vulg_index = defaultdict(list)
vulg_book_map = {
    "genesis": ["Genesis"],
    "isaiah": ["Isaiah"],
    "jeremiah": ["Jeremiah"],
    "daniel": ["Daniel"],
    "psalms": ["Psalms", "Psalm"],
    "gospels": ["Matthew", "Mark", "Luke", "John"],
    "romans": ["Romans"],
    "hebrews": ["Hebrews"],
    "revelation": ["Revelation"],
}
for fname, books in vulg_book_map.items():
    path = os.path.join(BASE, "vulgate", f"{fname}.json")
    if os.path.exists(path):
        d = load_json(path)
        for r in d.get("renderings", []):
            book, ch = parse_book_chapter_from_ref(r["reference"])
            if book == "Psalm":
                book = "Psalms"
            if book and ch:
                vulg_index[(book, ch)].append(r)

# 9. JST — appendix and footnotes, index by (book, chapter)
jst_appendix_index = defaultdict(list)
jst_footnotes_index = defaultdict(list)

path = os.path.join(BASE, "jst", "jst-appendix.json")
if os.path.exists(path):
    d = load_json(path)
    for p in d.get("passages", []):
        book, ch = parse_book_chapter_from_ref(p["reference"])
        if book and ch:
            jst_appendix_index[(book, ch)].append(p)

path = os.path.join(BASE, "jst", "jst-footnotes.json")
if os.path.exists(path):
    d = load_json(path)
    for fn in d.get("footnotes", []):
        book, ch = parse_book_chapter_from_ref(fn["reference"])
        if book and ch:
            jst_footnotes_index[(book, ch)].append(fn)

print(f"  DSS Isaiah: {len(dss_data)} chapters loaded")
print(f"  LXX Jeremiah: {len(lxx_jer_data)} chapters loaded")
print(f"  LXX Daniel: {len(lxx_dan_data)} chapters loaded")
print(f"  LXX Esther: {len(lxx_est_data)} chapters loaded")
print(f"  Samaritan Pentateuch: {len(sp_index)} chapter references")
print(f"  Targum Onkelos: {len(to_index)} chapter references")
print(f"  Targum Jonathan: {len(tj_index)} chapter references")
print(f"  Vulgate: {len(vulg_index)} chapter references")
print(f"  JST Appendix: {len(jst_appendix_index)} chapter references")
print(f"  JST Footnotes: {len(jst_footnotes_index)} chapter references")


# ── Note generation functions ──────────────────────────────────────────

def make_dss_note(ch):
    """Generate a DSS Isaiah note for a given chapter."""
    info = dss_data.get(ch)
    if not info:
        return None
    counts = info["counts"]
    if not counts:
        return None  # No theological/major/moderate variants

    # Build note
    parts = []
    theological = counts.get("theological", 0)
    major = counts.get("major", 0)
    moderate = counts.get("moderate", 0)

    notable_text = info["notable"]

    # Use the notable_variants preamble text if it has substance
    if notable_text and "no theologically significant" not in notable_text.lower() and "no significant" not in notable_text.lower():
        # Clean and use the notable text
        note = notable_text.strip()
        if len(note) > 300:
            note = note[:297] + "..."
        parts.append(f"The Dead Sea Scrolls (1QIsaiah-a) preserve this chapter with notable variants: {note}")
    elif theological > 0 or major > 0:
        parts.append(f"The Dead Sea Scrolls (1QIsaiah-a) contain {theological + major} theologically or textually significant variant(s) in this chapter")
        # Add detail from specific variants
        for verse_num, sig, note_text in info["details"]:
            if note_text:
                snippet = note_text[:150].strip()
                if len(note_text) > 150:
                    snippet += "..."
                parts.append(f"At verse {verse_num}: {snippet}")
                break  # Just one detail
    elif moderate > 0:
        parts.append(f"The Dead Sea Scrolls (1QIsaiah-a) show {moderate} moderate variant(s) in this chapter, mostly orthographic or stylistic")
    else:
        return None

    return " ".join(parts) + f". See the [DSS Isaiah comparison](/dss-isaiah/{ch})."


def make_lxx_jer_note(ch):
    """Generate an LXX Jeremiah note."""
    info = lxx_jer_data.get(ch)
    if not info:
        return None
    counts = info["counts"]

    parts = []
    structural = info.get("structural", "")
    notable = info.get("notable", "")

    if structural:
        parts.append(structural.strip())

    major_count = counts.get("major", 0) + counts.get("theological", 0)
    if major_count > 0:
        if notable and "no significant" not in notable.lower():
            snippet = notable.strip()
            if len(snippet) > 250:
                snippet = snippet[:247] + "..."
            parts.append(snippet)
        else:
            parts.append(f"The LXX preserves {major_count} major variant(s) in this chapter")
    elif counts.get("moderate", 0) > 0:
        parts.append(f"The LXX shows moderate differences in this chapter")

    if not parts:
        return None

    return "The Septuagint preserves a significantly different text tradition for Jeremiah. " + " ".join(parts) + f" See the [LXX Jeremiah comparison](/lxx-jeremiah/{ch})."


def make_lxx_dan_note(ch):
    """Generate an LXX Daniel note."""
    parts = []

    info = lxx_dan_data.get(ch)
    if info:
        counts = info["counts"]
        theological = counts.get("theological", 0)
        major = counts.get("major", 0)
        moderate = counts.get("moderate", 0)

        if theological > 0 or major > 0:
            notable = info["notable"]
            if notable:
                snippet = notable.strip()
                if len(snippet) > 250:
                    snippet = snippet[:247] + "..."
                parts.append(f"The LXX (Old Greek) Daniel differs from the MT here: {snippet}")
            else:
                parts.append(f"The LXX Daniel contains {theological + major} significant variant(s) in this chapter")
        elif moderate > 0:
            parts.append(f"The LXX Daniel shows {moderate} moderate difference(s) from the MT in this chapter")

    # Check for additions that relate to this chapter
    if ch in lxx_dan_additions:
        parts.append(lxx_dan_additions[ch])

    if not parts:
        return None

    return " ".join(parts) + f" See the [LXX Daniel comparison](/lxx-daniel/{ch})."


def make_lxx_est_note(ch):
    """Generate an LXX Esther note."""
    parts = []

    info = lxx_est_data.get(ch)
    if info:
        counts = info["counts"]
        theological = counts.get("theological", 0)
        major = counts.get("major", 0)
        moderate = counts.get("moderate", 0)

        if theological > 0 or major > 0 or moderate > 0:
            notable = info["notable"]
            if notable:
                snippet = notable.strip()
                if len(snippet) > 250:
                    snippet = snippet[:247] + "..."
                parts.append(f"The LXX Esther adds theological content absent from the Hebrew: {snippet}")
            else:
                parts.append(f"The LXX Esther contains {theological + major + moderate} variant(s) in this chapter")

    if ch in lxx_est_additions:
        parts.append(lxx_est_additions[ch])

    if not parts:
        return None

    return " ".join(parts) + f" See the [LXX Esther comparison](/lxx-esther/{ch})."


def make_sp_note(book_name, ch):
    """Generate a Samaritan Pentateuch note."""
    variants = sp_index.get((book_name, ch), [])
    if not variants:
        return None

    high = [v for v in variants if v.get("significance") == "high"]
    moderate = [v for v in variants if v.get("significance") == "moderate"]

    if not high and not moderate:
        return None

    parts = []
    if high:
        # Pick the most interesting high variant
        best = high[0]
        notes = best.get("notes", [])
        if notes:
            snippet = notes[0][:200].strip()
            if len(notes[0]) > 200:
                snippet += "..."
            parts.append(f"The Samaritan Pentateuch differs significantly here: {snippet}")
        else:
            mt_r = best.get("mt_rendering", "")
            sp_r = best.get("sp_rendering", "")
            if mt_r and sp_r and mt_r != sp_r:
                parts.append(f"The Samaritan Pentateuch reads '{sp_r}' where the MT has '{mt_r}' at {best['reference']}")
            else:
                parts.append(f"The Samaritan Pentateuch contains a significant variant at {best['reference']}")
        if len(high) > 1:
            parts.append(f"({len(high)} high-significance variants total in this chapter)")
    elif moderate:
        parts.append(f"The Samaritan Pentateuch shows {len(moderate)} moderate variant(s) in this chapter")

    book_lower = book_name.lower()
    return " ".join(parts) + f". See the [Samaritan Pentateuch](/samaritan-pentateuch/{book_lower})."


def make_to_note(book_name, ch):
    """Generate a Targum Onkelos note."""
    renderings = to_index.get((book_name, ch), [])
    if not renderings:
        return None

    # Pick the most interesting rendering
    best = renderings[0]
    notes = best.get("notes", [])
    category = best.get("category", "")

    parts = []
    if notes:
        snippet = notes[0][:200].strip()
        if len(notes[0]) > 200:
            snippet += "..."
        parts.append(f"Targum Onkelos interprets this chapter with notable Aramaic renderings: {snippet}")
    else:
        targ_r = best.get("targum_rendering", "")
        mt_r = best.get("mt_rendering", "")
        if targ_r and mt_r and targ_r != mt_r:
            parts.append(f"Targum Onkelos renders '{mt_r}' as '{targ_r}' ({best['reference']})")
        else:
            parts.append(f"Targum Onkelos provides interpretive Aramaic renderings for this chapter")

    if len(renderings) > 1:
        parts.append(f"({len(renderings)} notable renderings in this chapter)")

    book_lower = book_name.lower()
    return " ".join(parts) + f" See the [Targum Onkelos on {book_name}](/targum/{book_lower})."


def make_tj_note(book_name, ch):
    """Generate a Targum Jonathan note."""
    renderings = tj_index.get((book_name, ch), [])
    if not renderings:
        return None

    best = renderings[0]
    notes = best.get("notes", [])
    category = best.get("category", "")

    parts = []
    if notes:
        snippet = notes[0][:200].strip()
        if len(notes[0]) > 200:
            snippet += "..."
        parts.append(f"Targum Jonathan provides interpretive renderings: {snippet}")
    else:
        targ_r = best.get("targum_rendering", "")
        mt_r = best.get("mt_rendering", "")
        if targ_r and mt_r and targ_r != mt_r:
            parts.append(f"Targum Jonathan renders '{mt_r}' as '{targ_r}' ({best['reference']})")
        else:
            parts.append(f"Targum Jonathan provides Aramaic paraphrase for this chapter")

    if len(renderings) > 1:
        parts.append(f"({len(renderings)} notable renderings in this chapter)")

    # Determine URL based on book
    if book_name == "Isaiah":
        url_book = "isaiah"
    elif book_name == "Jeremiah":
        url_book = "jeremiah"
    elif book_name == "Ezekiel":
        url_book = "ezekiel"
    elif book_name in ("Joshua","Judges","1 Samuel","2 Samuel","1 Kings","2 Kings"):
        url_book = book_name.lower().replace(" ", "-")
    else:
        url_book = book_name.lower().replace(" ", "-")

    return " ".join(parts) + f" See [Targum Jonathan on {book_name}](/targum/{url_book})."


def make_vulgate_note(book_name, ch):
    """Generate a Vulgate note."""
    renderings = vulg_index.get((book_name, ch), [])
    if not renderings:
        return None

    best = renderings[0]
    legacy = best.get("theological_legacy", "")
    notes = best.get("notes", [])

    parts = []
    if legacy:
        snippet = legacy[:200].strip()
        if len(legacy) > 200:
            snippet += "..."
        parts.append(f"The Latin Vulgate shaped Western theology here: {snippet}")
    elif notes:
        note_text = notes[0] if isinstance(notes, list) else notes
        snippet = str(note_text)[:200].strip()
        if len(str(note_text)) > 200:
            snippet += "..."
        parts.append(f"The Latin Vulgate renders this passage with notable choices: {snippet}")
    else:
        vulg_r = best.get("vulgate_rendering", "")
        if vulg_r:
            parts.append(f"Jerome's Vulgate renders key terms distinctively in this chapter ({best['reference']})")
        else:
            parts.append(f"The Latin Vulgate provides notable renderings for this chapter")

    if len(renderings) > 1:
        parts.append(f"({len(renderings)} notable Vulgate renderings in this chapter)")

    book_lower = book_name.lower()
    return " ".join(parts) + f" See the [Vulgate {book_name}](/vulgate/{book_lower})."


def make_jst_note(book_name, ch):
    """Generate a JST note combining appendix and footnotes."""
    appendix = jst_appendix_index.get((book_name, ch), [])
    footnotes = jst_footnotes_index.get((book_name, ch), [])

    if not appendix and not footnotes:
        return None

    parts = []

    if appendix:
        best = appendix[0]
        title = best.get("title", "")
        summary = best.get("jst_summary", "")
        if title:
            parts.append(f"The Joseph Smith Translation includes a significant revision for this chapter: {title}")
        if summary:
            snippet = summary[:200].strip()
            if len(summary) > 200:
                snippet += "..."
            parts.append(snippet)

    if footnotes:
        theological = [f for f in footnotes if f.get("significance") in
                       ("theological", "christological", "covenantal", "soteriological",
                        "eschatological", "doctrinal", "pneumatological")]
        if theological:
            best = theological[0]
            change = best.get("change_summary", "")
            if change:
                parts.append(f"JST footnote at {best['reference']}: {change}")
        elif footnotes:
            best = footnotes[0]
            change = best.get("change_summary", "")
            if change:
                parts.append(f"The JST modifies this chapter ({best['reference']}): {change}")

    if not parts:
        return None

    book_lower = book_name.lower().replace(" ", "-")
    return " ".join(parts) + f" See the [JST notes](/jst/{book_lower})."


# ── Main enrichment loop ──────────────────────────────────────────────

enriched_count = 0
enriched_books = set()
skipped_missing = 0

print("\nEnriching preambles...\n")

for book_name, book_dir, ch_count in CANON:
    book_enriched = 0
    for ch in range(1, ch_count + 1):
        ch_path = os.path.join(BASE, book_dir, f"chapter-{ch:02d}.json")
        if not os.path.exists(ch_path):
            skipped_missing += 1
            continue

        data = load_json(ch_path)
        preamble = data.get("preamble", {})
        existing_connections = preamble.get("connections", "")

        # Collect all applicable tradition notes
        tradition_notes = []
        see_links = []

        # --- DSS Isaiah ---
        if book_name == "Isaiah":
            note = make_dss_note(ch)
            if note:
                tradition_notes.append(note)

        # --- LXX Jeremiah ---
        if book_name == "Jeremiah":
            note = make_lxx_jer_note(ch)
            if note:
                tradition_notes.append(note)

        # --- LXX Daniel ---
        if book_name == "Daniel":
            note = make_lxx_dan_note(ch)
            if note:
                tradition_notes.append(note)

        # --- LXX Esther ---
        if book_name == "Esther":
            note = make_lxx_est_note(ch)
            if note:
                tradition_notes.append(note)

        # --- Samaritan Pentateuch ---
        if book_name in PENTATEUCH:
            note = make_sp_note(book_name, ch)
            if note:
                tradition_notes.append(note)

        # --- Targum Onkelos ---
        if book_name in PENTATEUCH:
            note = make_to_note(book_name, ch)
            if note:
                tradition_notes.append(note)

        # --- Targum Jonathan ---
        note = make_tj_note(book_name, ch)
        if note:
            tradition_notes.append(note)

        # --- Vulgate ---
        note = make_vulgate_note(book_name, ch)
        if note:
            tradition_notes.append(note)

        # --- JST ---
        note = make_jst_note(book_name, ch)
        if note:
            tradition_notes.append(note)

        # If no tradition notes, skip
        if not tradition_notes:
            continue

        # Build the appended paragraph
        combined = " ".join(tradition_notes)
        enrichment = f"\n\n**Tradition comparisons:** {combined}"

        # Append to existing connections
        if existing_connections:
            new_connections = existing_connections + enrichment
        else:
            new_connections = enrichment.strip()

        preamble["connections"] = new_connections
        data["preamble"] = preamble

        save_json(ch_path, data)
        enriched_count += 1
        book_enriched += 1

    if book_enriched > 0:
        enriched_books.add(book_name)
        print(f"  {book_name}: {book_enriched} chapter(s) enriched")

print(f"\n{'='*60}")
print(f"Enrichment complete.")
print(f"  Chapters enriched: {enriched_count}")
print(f"  Books touched: {len(enriched_books)}")
print(f"  Chapters skipped (file missing): {skipped_missing}")
print(f"  Books: {', '.join(sorted(enriched_books))}")
