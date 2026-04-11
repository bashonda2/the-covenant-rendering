# The Covenant Rendering — Auditor Source of Truth

*Everything an auditor agent needs to validate this project, in one document.*

**Owner:** Aaron Blonquist
**Created:** 2026-04-05
**Version:** 2.0

---

## How to Use This Document

This is a **standalone, self-contained** reference for any agent auditing The Covenant Rendering. You should not need to cross-reference other documents to perform a complete audit. If you find yourself reaching for another file, this document needs updating.

**Audit scope:** 66 canonical books (OT + NT), plus 10 Extended Library traditions: DSS Isaiah, 1 Enoch, Jubilees, LXX Jeremiah, LXX Daniel, LXX Esther, JST (3 layers), Samaritan Pentateuch, Targum Onkelos, Targum Jonathan. Every chapter/entry stored as JSON in its tradition directory.

---

## 1. Complete Book Inventory

### Old Testament (39 books, 929 chapters, 23,210 verses)

| Book | Directory | Chapters | Verses | Source Text |
|---|---|---|---|---|
| Genesis | `genesis/` | 50 | 1,534 | WLC (Hebrew) |
| Exodus | `exodus/` | 40 | 1,213 | WLC |
| Leviticus | `leviticus/` | 27 | 859 | WLC |
| Numbers | `numbers/` | 36 | 1,288 | WLC |
| Deuteronomy | `deuteronomy/` | 34 | 956 | WLC |
| Joshua | `joshua/` | 24 | 658 | WLC |
| Judges | `judges/` | 21 | 618 | WLC |
| Ruth | `ruth/` | 4 | 85 | WLC |
| 1 Samuel | `1-samuel/` | 31 | 812 | WLC |
| 2 Samuel | `2-samuel/` | 24 | 695 | WLC |
| 1 Kings | `1-kings/` | 22 | 816 | WLC |
| 2 Kings | `2-kings/` | 25 | 719 | WLC |
| 1 Chronicles | `1-chronicles/` | 29 | 942 | WLC |
| 2 Chronicles | `2-chronicles/` | 36 | 822 | WLC |
| Ezra | `ezra/` | 10 | 280 | WLC |
| Nehemiah | `nehemiah/` | 13 | 406 | WLC |
| Esther | `esther/` | 10 | 167 | WLC |
| Job | `job/` | 42 | 1,070 | WLC |
| Psalms | `psalms/` | 150 | 2,461 | WLC |
| Proverbs | `proverbs/` | 31 | 915 | WLC |
| Ecclesiastes | `ecclesiastes/` | 12 | 222 | WLC |
| Song of Solomon | `song-of-songs/` | 8 | 117 | WLC |
| Isaiah | `isaiah/` | 66 | 1,292 | WLC |
| Jeremiah | `jeremiah/` | 52 | 1,364 | WLC |
| Lamentations | `lamentations/` | 5 | 154 | WLC |
| Ezekiel | `ezekiel/` | 48 | 1,273 | WLC |
| Daniel | `daniel/` | 12 | 357 | WLC |
| Hosea | `hosea/` | 14 | 197 | WLC |
| Joel | `joel/` | 3 | 73 | WLC |
| Amos | `amos/` | 9 | 146 | WLC |
| Obadiah | `obadiah/` | 1 | 21 | WLC |
| Jonah | `jonah/` | 4 | 48 | WLC |
| Micah | `micah/` | 7 | 105 | WLC |
| Nahum | `nahum/` | 3 | 47 | WLC |
| Habakkuk | `habakkuk/` | 3 | 56 | WLC |
| Zephaniah | `zephaniah/` | 3 | 53 | WLC |
| Haggai | `haggai/` | 2 | 38 | WLC |
| Zechariah | `zechariah/` | 14 | 211 | WLC |
| Malachi | `malachi/` | 4 | 55 | WLC |

### New Testament (27 books, 260 chapters, 7,959 verses)

| Book | Directory | Chapters | Verses | Source Text |
|---|---|---|---|---|
| Matthew | `matthew/` | 28 | 1,071 | SBLGNT (Greek) |
| Mark | `mark/` | 16 | 678 | SBLGNT |
| Luke | `luke/` | 24 | 1,151 | SBLGNT |
| John | `john/` | 21 | 880 | SBLGNT |
| Acts | `acts/` | 28 | 1,006 | SBLGNT |
| Romans | `romans/` | 16 | 433 | SBLGNT |
| 1 Corinthians | `1-corinthians/` | 16 | 437 | SBLGNT |
| 2 Corinthians | `2-corinthians/` | 13 | 257 | SBLGNT |
| Galatians | `galatians/` | 6 | 149 | SBLGNT |
| Ephesians | `ephesians/` | 6 | 155 | SBLGNT |
| Philippians | `philippians/` | 4 | 104 | SBLGNT |
| Colossians | `colossians/` | 4 | 95 | SBLGNT |
| 1 Thessalonians | `1-thessalonians/` | 5 | 89 | SBLGNT |
| 2 Thessalonians | `2-thessalonians/` | 3 | 47 | SBLGNT |
| 1 Timothy | `1-timothy/` | 6 | 113 | SBLGNT |
| 2 Timothy | `2-timothy/` | 4 | 83 | SBLGNT |
| Titus | `titus/` | 3 | 46 | SBLGNT |
| Philemon | `philemon/` | 1 | 25 | SBLGNT |
| Hebrews | `hebrews/` | 13 | 303 | SBLGNT |
| James | `james/` | 5 | 108 | SBLGNT |
| 1 Peter | `1-peter/` | 5 | 105 | SBLGNT |
| 2 Peter | `2-peter/` | 3 | 61 | SBLGNT |
| 1 John | `1-john/` | 5 | 105 | SBLGNT |
| 2 John | `2-john/` | 1 | 13 | SBLGNT |
| 3 John | `3-john/` | 1 | 15 | SBLGNT |
| Jude | `jude/` | 1 | 25 | SBLGNT |
| Revelation | `revelation/` | 22 | 405 | SBLGNT |

### Extended Library

#### Manuscript Traditions (variant comparison against MT)

| Text | Directory | Files | Schema | Source Text | Key Audit Points |
|---|---|---|---|---|---|
| DSS Isaiah (1QIsaᵃ) | `dss-isaiah/` | 66 (`chapter-01.json`–`chapter-66.json`) | Variant (§2.3) | 1QIsaiah-a (Qumran Cave 1), c. 125 BCE | 1,292 verses, 590 variants. Every verse must have entry. Significance: none/minor/moderate/major/theological. Column refs required. |
| LXX Jeremiah | `lxx-jeremiah/` | 52 (`jeremiah_01_lxx.json`–`jeremiah_52_lxx.json`) | Variant (§2.3) | Rahlfs' Septuaginta | NOTE: Non-standard filenames (not `chapter-XX.json`). 187 variants. Uses `lxx_reading` not `dss_reading`. Ch 33:14-26 absent from LXX = theological. |
| LXX Daniel | `lxx-daniel/` | 15 (12 variant + 3 standalone) | Mixed | Rahlfs' / Theodotion | `chapter-01.json`–`chapter-12.json` = variant schema. `chapter-13.json` (Susanna, 64v), `chapter-03-additions.json` (Prayer of Azariah, 68v), `chapter-14.json` (Bel and Dragon, 48v) = standalone rendering schema (§2.4). |
| LXX Esther | `lxx-esther/` | 16 (10 variant + 6 standalone) | Mixed | Rahlfs' Septuaginta | `chapter-01.json`–`chapter-10.json` = variant schema. `addition-A.json` through `addition-F.json` = standalone rendering schema. 107 added verses total. |
| Samaritan Pentateuch | `samaritan-pentateuch/` | 5 (`genesis.json`–`deuteronomy.json`) | Per-book variant summary | Critical editions | 156 significant variants. Uses `variants` array (not `verses`). Fields: reference, significance, mt_reading, sp_reading, mt_rendering, sp_rendering, notes. Key: Deut 27:4 Gerizim/Ebal, 10th commandment, "has chosen" formula. |

#### Pre-Nicaea Canon (standalone renderings)

| Text | Directory | Files | Schema | Source Text | Key Audit Points |
|---|---|---|---|---|---|
| 1 Enoch | `1-enoch/` | 108 (`chapter-01.json`–`chapter-108.json`) | Extended Library (§2.4) | Ge'ez (R.H. Charles / Knibb) | 1,054 verses. Uses `text_source`/`text_reference` (not `text_hebrew`). 1:9 must cross-ref Jude 14-15. Watchers (not "angels") for `irin`. |
| Jubilees | `jubilees/` | 50 (`chapter-01.json`–`chapter-50.json`) | Extended Library (§2.4) | Ge'ez (R.H. Charles / VanderKam) | 1,245 verses. Uses `text_source`/`text_reference`. 364-day calendar emphasis. Mastema = adversary figure. |

#### Interpretive Traditions

| Text | Directory | Files | Schema | Source Text | Key Audit Points |
|---|---|---|---|---|---|
| JST — Book of Moses | `jst/` | 8 (`moses-01.json`–`moses-08.json`) | Extended Library (§2.4) | Pearl of Great Price (LDS Church) | 356 verses. Canonized LDS scripture. `text_source` = Moses text, `text_reference` = KJV Genesis parallel. Moses 1 has NO Genesis parallel. |
| JST — JS-Matthew | `jst/` | 1 (`js-matthew.json`) | Extended Library (§2.4) | Pearl of Great Price (LDS Church) | 55 verses. JST revision of Matthew 24. |
| JST — Appendix | `jst/` | 1 (`jst-appendix.json`) | Custom (§2.5) | JST Appendix, LDS Edition KJV | 14 passages. Uses `passages` array. Fields: reference, title, jst_summary, kjv_summary, significance, notes. |
| JST — Footnotes | `jst/` | 1 (`jst-footnotes.json`) | Custom (§2.5) | JST Footnotes, LDS Edition KJV | 111 entries. Uses `footnotes` array. Fields: reference, change_summary, significance, notes. |
| Targum Onkelos | `targum-onkelos/` | 5 (`genesis.json`–`deuteronomy.json`) | Custom (§2.6) | Standard printed edition | 176 renderings across Torah. Uses `renderings` array. Fields: reference, hebrew_text, targum_text, targum_rendering, mt_rendering, category, notes. Categories: anti-anthropomorphism, memra, shekinah, messianic, halakhic, other. |
| Targum Jonathan | `targum-jonathan/` | 5 (`former-prophets.json`, `isaiah.json`, `jeremiah.json`, `ezekiel.json`, `minor-prophets.json`) | Custom (§2.6) | Standard printed edition | 153 renderings across Prophets. Same schema as Onkelos. Isaiah 52:13-53:12 reinterpretation = critical audit target. |

### NT Books Set (for testament detection)

```
matthew, mark, luke, john, acts, romans, 1-corinthians, 2-corinthians,
galatians, ephesians, philippians, colossians, 1-thessalonians,
2-thessalonians, 1-timothy, 2-timothy, titus, philemon, hebrews,
james, 1-peter, 2-peter, 1-john, 2-john, 3-john, jude, revelation
```

---

## 2. JSON Schemas

### 2.1 Canonical OT Verse

Every OT verse object must have these fields:

```json
{
  "verse": 1,
  "text_hebrew": "Full Hebrew text from WLC with vowel pointing",
  "text_kjv": "KJV text for reference comparison",
  "rendering": "Modern English rendering translated from Hebrew",
  "expanded_rendering": "(Optional) 1-2 sentence explanation of a specific Hebrew term",
  "translator_notes": ["Array of verse-specific notes"],
  "key_terms": [
    {
      "hebrew": "Hebrew word in Hebrew script",
      "transliteration": "Romanized form",
      "rendered_as": "English rendering chosen",
      "semantic_range": "Full range of meanings",
      "note": "Why this rendering was chosen (2-4 sentences)"
    }
  ],
  "reading_level": "8th grade"
}
```

**Required fields:** `verse`, `text_hebrew`, `text_kjv`, `rendering`, `translator_notes`, `reading_level`
**Conditional fields:** `expanded_rendering` (5-20% of verses), `key_terms` (where theologically significant)

### 2.2 Canonical NT Verse

Same structure as OT, but `text_hebrew` is replaced by `text_greek`:

```json
{
  "verse": 1,
  "text_greek": "Greek text from SBLGNT",
  "text_kjv": "KJV text for reference comparison",
  "rendering": "Modern English rendering translated from Greek",
  "expanded_rendering": "(Optional)",
  "translator_notes": ["Array of verse-specific notes"],
  "key_terms": [
    {
      "greek": "Greek word",
      "transliteration": "Romanized form",
      "rendered_as": "English rendering chosen",
      "semantic_range": "Full range of meanings",
      "note": "Why this rendering was chosen"
    }
  ],
  "reading_level": "8th grade"
}
```

**Required fields:** `verse`, `text_greek`, `text_kjv`, `rendering`, `translator_notes`, `reading_level`
**key_terms source field:** `greek` (not `hebrew`)

### 2.3 DSS / LXX Variant Verse

Variant-tradition texts compare against the Masoretic base text:

```json
{
  "verse": 1,
  "has_variant": true,
  "significance": "minor|moderate|major|theological|none",
  "mt_reading": "Masoretic Hebrew text",
  "dss_reading": "Scroll/LXX reading (field name varies: dss_reading or lxx_reading)",
  "variant_rendering": "English rendering of the variant",
  "mt_rendering": "English rendering of the MT reading",
  "manuscript_reference": "Physical manuscript location reference",
  "variant_notes": ["Array of scholarly notes on the variant"]
}
```

**When `has_variant` is false:** Only `verse`, `has_variant`, `manuscript_reference`, and `variant_notes` are required.

**Significance levels:** `none` (identical), `minor` (orthographic), `moderate` (different word form but similar meaning), `major` (different meaning), `theological` (affects theological interpretation).

### 2.4 Extended Library Verse (1 Enoch, Jubilees)

Non-canonical texts from non-Hebrew/Greek originals:

```json
{
  "verse": 1,
  "text_source": "Source language text or reference",
  "text_reference": "Reference English translation (e.g., Charles 1917)",
  "rendering": "Modern English rendering",
  "translator_notes": ["Array of verse-specific notes"],
  "key_terms": [
    {
      "term": "Term name",
      "note": "Explanation of the term",
      "definition": "(Optional) Term definition"
    }
  ],
  "reading_level": "8th grade"
}
```

**Note:** Extended library `key_terms` may use `term`/`note`/`definition` fields rather than the canonical 5-field schema. This is acceptable — the canonical schema enforces `hebrew` (OT) or `greek` (NT), but extended library texts from Ge'ez, Aramaic, or English sources may use a simplified format. Do not fail extended library files for non-canonical key_terms schemas.

### 2.5 Chapter Wrapper

Every chapter JSON file wraps verses in this structure:

```json
{
  "meta": {
    "project": "The Covenant Rendering",
    "version": "1.0.0",
    "book": "Genesis",
    "chapter": 1,
    "source_text": "Westminster Leningrad Codex (WLC)",
    "reference_text": "KJV",
    "generated_at": "2026-03-04T00:00:00Z",
    "prompt_version": "1.3",
    "license": "CC-BY-4.0"
  },
  "preamble": {
    "summary": "What happens in this chapter.",
    "remarkable": "What makes this chapter distinctive.",
    "friction": "Translation challenges and how we handled them.",
    "connections": "Cross-references to other Scripture."
  },
  "verses": []
}
```

**Meta validation:**
- `meta.book` and `meta.chapter` must match the filename
- `meta.prompt_version` must be ≥ 1.3 for canonical books
- `meta.license` must be `CC-BY-4.0`
- `meta.model` field should NOT be present (AI attribution removed from reader-facing materials)

**Preamble validation:** All 4 fields required (`summary`, `remarkable`, `friction`, `connections`). No field may be empty.

**Extended library meta** may also include: `tradition`, `tradition_label`, `tier`, `base_text`, `date`, `manuscript_location`, `attribution`.

### 2.5 JST Appendix/Footnotes Schema

The JST appendix and footnotes use collection schemas (not per-verse):

**Appendix** (`jst-appendix.json`):
```json
{
  "passages": [
    {
      "reference": "Genesis 14:25-40",
      "title": "Melchizedek expansion",
      "jst_summary": "Description of what the JST adds/changes",
      "kjv_summary": "What the KJV says",
      "significance": "theological",
      "notes": ["Scholarly explanation"]
    }
  ]
}
```

**Footnotes** (`jst-footnotes.json`):
```json
{
  "footnotes": [
    {
      "reference": "Matthew 4:1",
      "change_summary": "What the JST changes",
      "significance": "theological",
      "notes": ["Explanation"]
    }
  ]
}
```

### 2.6 Targum Schema

Targum files use a `renderings` array showing how the Aramaic tradition interprets specific passages:

```json
{
  "renderings": [
    {
      "reference": "Genesis 3:8",
      "hebrew_text": "Hebrew from MT",
      "targum_text": "Aramaic transliteration",
      "targum_rendering": "English translation of Targum",
      "mt_rendering": "TCR rendering of MT",
      "category": "anti-anthropomorphism|memra|shekinah|messianic|halakhic|aqedah|eschatological|other",
      "notes": ["Explanation of how and why the Targum differs"]
    }
  ]
}
```

**Category audit:** Every Targum rendering must have a valid category. The Memra (Word) renderings are critical for NT studies (John 1:1 background).

### 2.7 Samaritan Pentateuch Schema

Per-book files with a `variants` array:

```json
{
  "variants": [
    {
      "reference": "Deuteronomy 27:4",
      "has_variant": true,
      "significance": "theological",
      "mt_reading": "Hebrew from MT",
      "sp_reading": "Hebrew from SP",
      "mt_rendering": "TCR rendering",
      "sp_rendering": "How SP reads",
      "notes": ["Explanation"]
    }
  ]
}
```

---

## 3. Automated Validation Checks (10 checks)

These are binary pass/fail. Run via `python3 scripts/qa_validate.py <file_or_dir>`.

### Check 1: JSON integrity
The file parses without errors.

### Check 2: Verse count
Number of verses matches the expected chapter length.

### Check 3: Verse numbering
Verses are sequential (1, 2, 3...) with no gaps or duplicates.

**Known exceptions:**
- **John 8 (Pericope Adulterae):** 7:53–8:11 is prepended to the chapter as a textual note. Main chapter starts at verse 12. Apparent duplicates in 1-11 are expected.
- **Textual-critical omissions (NT):** Certain verses are absent from SBLGNT but present in KJV/Textus Receptus. These gaps are expected and should not fail validation. Full list in Section 8.

### Check 4: Required fields present
Every verse must have all required fields for its testament:
- **OT:** `verse`, `text_hebrew`, `text_kjv`, `rendering`, `translator_notes`, `reading_level`
- **NT:** `verse`, `text_greek`, `text_kjv`, `rendering`, `translator_notes`, `reading_level`

Skip textual-critical omissions (they intentionally lack text/rendering).

### Check 5: No KJV pass-through
No verse may have a `rendering` field that is ≥92% similar to its `text_kjv` field (measured by SequenceMatcher ratio).

**Exception:** Name-only lists (e.g., "Reuben, Simeon, Levi, and Judah") where any translation produces identical text. A verse is considered a name list if >60% of its words match the pattern of proper nouns, conjunctions, and relational words.

### Check 6: No boilerplate notes
No `translator_notes` entry may contain these banned strings (case-insensitive):
- "the narrative advances the confrontation"
- "the narrative advances the conflict"
- "full verse-specific note to be completed"
- "numbers narrative/census detail"
- "to be completed in quality pass"

No identical note may appear across 3+ verses in the same chapter.

### Check 7: No archaic language in renderings
The `rendering` field must not contain (case-insensitive, whole-word matching):

`thou`, `thee`, `thy`, `thine`, `hath`, `doth`, `saith`, `goest`, `takest`, `dealest`, `killedst`, `ye`, `to wit`, `wherefore`, `unto`, `separateth`, `sodden`, `heave shoulder`

**Exception:** "LORD" (all caps) is not archaic — it is the standard YHWH rendering.

### Check 8: Meta fields correct
- `meta.book` present
- `meta.chapter` present
- `meta.prompt_version` ≥ 1.3
- `meta.license` == "CC-BY-4.0"

### Check 9: key_terms schema
For canonical books:
- `key_terms` must be a list of dicts (not bare strings, not a single dict)
- Each entry must have exactly 5 fields:
  - **OT:** `hebrew`, `transliteration`, `rendered_as`, `semantic_range`, `note`
  - **NT:** `greek`, `transliteration`, `rendered_as`, `semantic_range`, `note`
- No field may be empty
- Wrong field names (`register_translation` instead of `rendered_as`, `gloss` instead of `semantic_range`) must be caught

### Check 10: expanded_rendering schema
- Must be a string (not an object like `{"text": "...", "note": "..."}`)
- Must not be empty
- Must appear after `rendering` and before `translator_notes` in field order

---

## 4. Quality Checks (Judgment-Based, 8 checks)

These require understanding the content. They supplement the automated checks.

### Check 11: Translator notes are verse-specific
Every note must reference something specific to its verse. A note that could be copy-pasted to a different verse and still make sense is too generic.

### Check 12: Translator notes match their verse
The content of each note must correspond to the verse it's attached to, not to a neighboring verse.

### Check 13: Renderings are modern English
Renderings should sound like clean, natural English written in 2026. Near-KJV renderings that differ by only 1-2 words but retain KJV syntax and vocabulary should be flagged.

### Check 14: Theologically Rich Terms handled
If the chapter contains any register terms in a theologically significant context, verify that `expanded_rendering` and/or `key_terms` are present:

| Hebrew | Transliteration | When ER Required |
|---|---|---|
| חֶסֶד | chesed | Always |
| בְּרִית | berit | In significant contexts |
| כִּפֶּר / כַּפֹּרֶת | kippur / kapporet | In significant contexts |
| קָדוֹשׁ | qadosh | In significant contexts |
| תְּשׁוּבָה | teshuvah | In significant contexts |
| גָּאַל / גֹּאֵל | ga'al / go'el | In significant contexts |
| שָׁלוֹם | shalom | When carrying full weight |
| צֶדֶק / צְדָקָה | tsedeq / tsedaqah | In significant contexts |
| עוֹלָם | olam | In significant contexts |
| אֱמוּנָה | emunah | Always |
| כָּבוֹד | kavod | In theophanies, temple, divine presence |
| שְׁכִינָה | Shekhinah | Note in translator_notes only (concept, not in text) |

### Check 15: Poetry rendered as poetry
If the chapter contains poetry (blessings, songs, oracles, prophetic speech), verify that the rendering preserves line breaks and parallelism. Poetry must not be flattened into prose.

### Check 16: Sacrificial vocabulary consistent (Leviticus/Numbers)
If the chapter discusses offerings, verify: olah (burnt offering), minchah (grain offering), shelamim (peace offering), chata't (sin offering), asham (guilt offering).

### Check 17: Purity vocabulary correct (Leviticus)
If the chapter discusses clean/unclean, verify tamei/tahor language is rendered correctly and notes explain ritual fitness, not hygiene.

### Check 18: Qere/Ketiv notation correct
If `text_hebrew` contains a qere/ketiv variant, verify notation follows WLC/BHS convention: **Ketiv (written text) in square brackets `[...]`**, **Qere (read text) in parentheses `(...)`**. Ketiv first, then Qere. Example: `[ישגלנה] (יִשְׁכָּבֶ֔נָּה)`.

---

## 5. Term Consistency Register

### 5.1 Default Term Register

Same word + same type of context = same rendering. Departures from the default must be documented in `translator_notes`.

| Hebrew | Transliteration | Default Rendering | When to Vary |
|---|---|---|---|
| חֶסֶד | chesed | **faithful love** | Non-covenantal contexts (e.g., political allies: "kindness") |
| בְּרִית | berit | **covenant** | Rarely varies |
| גֹּאֵל | go'el | **kinsman-redeemer** | When applied to God: "Redeemer" (capitalized) |
| גָּאַל | ga'al | **redeem** | Rarely varies |
| נָגִיד | nagid | **leader** | When military/administrative sense dominates |
| מָשִׁיחַ | mashiach | **anointed** / **anointed one** | Rarely varies |
| מְשִׁיחַ יְהוָה | meshiach YHWH | **the LORD's anointed** | Rarely varies |
| רוּחַ יְהוָה | ruach YHWH | **Spirit of the LORD** | Always capitalize Spirit |
| רוּחַ אֱלֹהִים | ruach Elohim | **Spirit of God** | Always capitalize Spirit |
| נָבִיא | navi | **prophet** | When text uses older synonym (1 Sam 9:9: ro'eh = "seer") |
| כָּבוֹד | kavod | **glory** | When physical "weight/heaviness" is primary |
| שָׁלוֹם | shalom | **peace** | "Well-being" or "wholeness" in context |
| קָדוֹשׁ | qadosh | **holy** | Rarely varies |
| חֵרֶם | cherem | **devoted to destruction** | Rarely varies in conquest/ban contexts |
| סַרְנֵי | sarnei | **tyrants** | Never varies — this is a Philistine title |

### 5.2 Locked Narrative Formulas

These recur across books and must be rendered identically every time:

| Formula | Hebrew | Locked Rendering |
|---|---|---|
| Regnal death | vayyishkav im avotav | **"X slept with his fathers"** |
| Succession | vayyimlokh tachtav | **"X reigned in his place"** |
| Prophetic messenger | ko amar YHWH | **"This is what the LORD says"** |
| Temple inner sanctuary | qodesh ha-qodashim | **"Holy of Holies"** |
| Judges refrain | — | **"In those days there was no king in Israel; everyone did what was right in his own eyes"** (word-for-word identical in Judges 17:6, 18:1, 19:1, 21:25) |

### 5.3 expanded_rendering Density Rules

- **Target:** 5-20% of verses in a chapter should have `expanded_rendering`
- A chapter with 25 verses should have roughly 2-5 expanded_renderings
- If >25% of verses have ER, the field is being used as commentary — audit for violations
- Every ER must name a specific Hebrew/Greek term and explain its theological depth
- ERs that are narrative summary, plot analysis, or literary criticism belong in `translator_notes`

### 5.4 Standing Terminology Decisions

| Decision | Standard |
|---|---|
| YHWH | LORD (all caps) |
| Elohim | God |
| torah (common noun) | "the Law" or "instruction" (never transliterated "Torah" in rendering) |
| torat Mosheh | "the Law of Moses" |
| sefer ha-torah | "the Book of the Law" |
| hevel (Ecclesiastes) | "vapor" (not "vanity") |

---

## 6. Three Non-Negotiable Quality Rules

These were established during Exodus generation and apply universally:

**Rule 1: No KJV pass-through.** Every rendering must be independently translated from the source language. The rendering must never be a copy or near-copy of `text_kjv`. Only exception: name-only verses where any translation produces identical text.

**Rule 2: No boilerplate translator notes.** Every note must be specific to its verse — explaining what is happening in *that verse*, what Hebrew/Greek features are present, what translation decisions were made. Generic notes are prohibited.

**Rule 3: Consistent modernization.** No archaic pronouns (thou, thee, thy, ye), no archaic verb forms (hast, hath, goest, saith), no archaic vocabulary (unto, behold reflexively, wherefore) in the `rendering` field.

---

## 7. Cross-Testament Coherence

With both testaments complete, auditors should verify:

### 7.1 OT Quotations in the NT
When the NT quotes the OT, the rendering should be recognizably similar (unless the NT author is following the LXX rather than the MT, in which case the difference should be noted).

### 7.2 Shared Theological Terms
| Concept | OT Term | NT Term | Expected Consistency |
|---|---|---|---|
| Covenant | berit → "covenant" | diathēkē → "covenant" | Same English word |
| Faith/Faithfulness | emunah → "faithfulness/faith" | pistis → "faith/faithfulness" | Same semantic field |
| Righteousness/Justice | tsedeq/tsedaqah | dikaiosynē | Same semantic field |
| Redeem/Redeemer | ga'al/go'el | lytrōsis/lytrōtēs | Related renderings |
| Holy | qadosh | hagios | Same English word |
| Glory | kavod | doxa | Same English word |
| Peace | shalom | eirēnē | Same English word |
| Spirit of the LORD | ruach YHWH | pneuma kyriou | Same pattern |

### 7.3 Key Cross-Testament Passages
These passages have direct NT-OT connections that should be audited for coherence:
- Isaiah 7:14 (almah → "young woman") ↔ Matthew 1:23 (parthenos)
- Isaiah 53 (Suffering Servant) ↔ Acts 8:32-35, 1 Peter 2:22-25
- Psalm 22 ↔ Matthew 27:46, John 19:24
- Psalm 110 ↔ Hebrews 5-7 (Melchizedek)
- Jeremiah 31:31-34 (New Covenant) ↔ Hebrews 8:8-12
- Daniel 7:13-14 (Son of Man/bar enash) ↔ Mark 14:62
- Habakkuk 2:4 ↔ Romans 1:17, Galatians 3:11
- Joel 2:28-29 ↔ Acts 2:17-21
- 1 Enoch 1:9 ↔ Jude 14-15

---

## 8. Known Exceptions and Special Cases

### 8.1 Textual-Critical Omissions (NT)

These verses are absent from the SBLGNT critical text but present in KJV / Textus Receptus. They may have empty text_greek/rendering with an explanatory translator_note, or may be omitted entirely. Both treatments are correct. Do not flag these as missing verses.

| Book | Chapter | Verse(s) | Treatment |
|---|---|---|---|
| Matthew | 17 | 21 | Omission note |
| Matthew | 18 | 11 | Omission note |
| Matthew | 23 | 14 | Omission note |
| Mark | 7 | 16 | Omission note |
| Mark | 9 | 44 | Omission note |
| Mark | 9 | 46 | Omission note |
| Mark | 11 | 26 | Omission note |
| Mark | 15 | 28 | Omission note |
| Luke | 23 | 17 | Omission note |
| John | 5 | 4 | Omitted entirely |
| Acts | 8 | 37 | Omitted entirely |
| Acts | 15 | 34 | Omission note |
| Acts | 24 | 7 | Omission note |
| Acts | 28 | 29 | Omission note |

### 8.2 John 7:53–8:11 (Pericope Adulterae)

The Pericope Adulterae is included in the John 8 chapter file with full textual-critical apparatus. Verses 7:53 and 8:1-11 are prepended before the main chapter (which starts at 8:12). This means verse numbers 1-11 may appear to be duplicated. This is expected — the PA section is a textual-critical note, not a duplication error.

### 8.3 Mark 16:9-20 (Longer Ending)

The longer ending is included with a textual note. This is a deliberate editorial decision.

### 8.4 Hebrew/English Versification Differences

Several books have verse numbering that differs between Hebrew (WLC) and English (KJV) conventions. The project follows Hebrew versification as primary. Known offsets:
- Psalms (many chapters have title verses numbered differently)
- Joel (Hebrew ch 3-4 = English ch 2:28-3:21)
- Malachi (Hebrew 3:19-24 = English 4:1-6)
- Song of Solomon ch 7 (Hebrew versification)
- Zechariah ch 1-2 (corrected to English convention)
- Numbers ch 16-17, 29-30 (verse offsets handled)
- Deuteronomy ch 5, 12-13, 22-23, 28-29 (verse offsets handled)

### 8.5 Bilingual Books

Daniel: Hebrew (ch 1:1–2:4a, 8-12) and Aramaic (ch 2:4b–7:28). Language transitions must be documented.

### 8.6 Known KJV-Proximity Flags (Accepted)

54 OT chapters in later Prophets flag KJV-proximity in automated QA but renderings are verified as accurate from the Hebrew. Proximity is acceptable when the source text warrants the same English. These are tracked but not considered failures.

---

## 9. Audit Scripts

### 9.1 Automated QA Validation

```bash
# Single chapter
python3 scripts/qa_validate.py genesis/chapter-01.json

# Entire book
python3 scripts/qa_validate.py genesis/

# Scaffold report (Pentateuch only — legacy)
python3 scripts/qa_validate.py --scaffold-report
```

Returns PASS/FAIL with detailed check results and issue list.

### 9.2 ER Density and Preamble Audit

```bash
python3 scripts/audit_books.py
```

**Warning:** As of 2026-04-05, this script only covers 22 OT books. It needs updating to cover all 66 canonical books + extended library. The book list is hardcoded in the `BOOKS` variable.

### 9.3 Full Bible Audit (Recommended Procedure)

To audit the entire Bible:

1. **Run automated QA on every book directory:**
   ```bash
   for dir in genesis exodus leviticus numbers deuteronomy joshua judges ruth \
     1-samuel 2-samuel 1-kings 2-kings 1-chronicles 2-chronicles \
     ezra nehemiah esther job psalms proverbs ecclesiastes song-of-songs \
     isaiah jeremiah lamentations ezekiel daniel \
     hosea joel amos obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi \
     matthew mark luke john acts romans 1-corinthians 2-corinthians \
     galatians ephesians philippians colossians 1-thessalonians 2-thessalonians \
     1-timothy 2-timothy titus philemon hebrews james \
     1-peter 2-peter 1-john 2-john 3-john jude revelation; do
     echo "=== $dir ==="
     python3 scripts/qa_validate.py "$dir/"
   done
   ```

2. **Check chapter counts match expected (Section 1 tables above)**

3. **Spot-check term consistency across books** (pick 3-5 terms from the Default Term Register and grep across rendered text)

4. **Verify preamble completeness** (every chapter should have all 4 preamble fields)

5. **Cross-testament coherence spot checks** (Section 7.3 passages)

6. **Extended Library structural audit:**
   ```bash
   # Verify file counts match expected
   echo "DSS Isaiah: $(ls dss-isaiah/chapter-*.json | wc -l) / 66 expected"
   echo "1 Enoch: $(ls 1-enoch/chapter-*.json | wc -l) / 108 expected"
   echo "Jubilees: $(ls jubilees/chapter-*.json | wc -l) / 50 expected"
   echo "LXX Jeremiah: $(ls lxx-jeremiah/*.json | wc -l) / 52 expected"
   echo "LXX Daniel: $(ls lxx-daniel/*.json | wc -l) / 15 expected"
   echo "LXX Esther: $(ls lxx-esther/*.json | wc -l) / 16 expected"
   echo "JST: $(ls jst/*.json | wc -l) / 11 expected"
   echo "Samaritan: $(ls samaritan-pentateuch/*.json | wc -l) / 5 expected"
   echo "Targum Onkelos: $(ls targum-onkelos/*.json | wc -l) / 5 expected"
   echo "Targum Jonathan: $(ls targum-jonathan/*.json | wc -l) / 5 expected"
   ```

7. **Extended Library content audit (judgment-based):**
   - **DSS Isaiah:** Spot-check 5 chapters. Every verse must have an entry. Theological variants must have substantive notes. Isaiah 7:14 (almah) and 53:11 ("he shall see light") are mandatory audit targets.
   - **1 Enoch:** Verify 1:9 cross-references Jude 14-15. Verify ch 14 throne vision notes Ezekiel 1 parallels. Verify ch 46 Son of Man notes Daniel 7:13.
   - **Jubilees:** Verify ch 15 (circumcision) notes the eternal covenant claim. Verify ch 30 (Dinah) notes the contradiction with Genesis 49:5-7.
   - **LXX Jeremiah:** Verify ch 33 documents the absent vv 14-26. Verify ch 25 documents the OAN relocation. Verify 4QJerb is mentioned.
   - **LXX Daniel:** Verify ch 7:13 Son of Man variant is documented. Verify Susanna, Prayer of Azariah, and Bel/Dragon use standalone schema.
   - **LXX Esther:** Verify Addition C (prayers) documents the theological silence of MT Esther. Verify 4:14 "from another place" variant.
   - **JST:** Verify Moses 1 has no Genesis parallel (text_reference should be empty/noted). Verify appendix does NOT reproduce full copyrighted text. Verify footnotes summarize changes without full JST text.
   - **Samaritan Pentateuch:** Verify Deut 27:4 Gerizim/Ebal variant is documented as theological. Verify 10th commandment (Ex 20 / Deut 5) is present.
   - **Targum Onkelos:** Verify Memra renderings documented (Gen 3:8 minimum). Verify Poem of Four Nights (Ex 12:42).
   - **Targum Jonathan:** Verify Isaiah 52:13 "my servant the Messiah" is documented. Verify Isaiah 53 reinterpretation is thoroughly noted.

---

## 10. Audit Verdict Format

When reporting audit results, use this format:

```
## AUDIT VERDICT: [PASS / FAIL / ISSUES FOUND]

### Scope
[What was audited — e.g., "Full Bible (66 books, 1,189 chapters)"]

### Automated QA Results
- Total chapters scanned: X
- Chapters passing: X
- Chapters failing: X
- Failing chapters: [list with reasons]

### Structural Checks
- [ ] All expected book directories present
- [ ] Chapter counts match inventory
- [ ] No missing or extra chapter files
- [ ] Preambles complete on all chapters

### Term Consistency
- [ ] Default Term Register terms consistent
- [ ] Locked narrative formulas consistent
- [ ] ER density within 5-20% target

### Cross-Testament Coherence (if applicable)
- [ ] Key OT-NT passages checked
- [ ] Shared theological terms aligned

### Extended Library (if applicable)
- [ ] File counts match inventory for all 10 traditions
- [ ] DSS Isaiah: Isaiah 7:14 and 53:11 audit targets verified
- [ ] 1 Enoch: 1:9 → Jude cross-reference present
- [ ] LXX Jeremiah: ch 33:14-26 absence documented
- [ ] JST: No full copyrighted text reproduced in appendix/footnotes
- [ ] Targum Jonathan: Isaiah 52:13-53:12 reinterpretation documented
- [ ] Samaritan Pentateuch: Deut 27:4 Gerizim variant documented

### Known Issues (accepted)
[List any items from Section 8 that fired during the audit]

### New Issues Found
[List any genuine problems discovered]

### Recommendation
[CLEAN / REMEDIATE SPECIFIC CHAPTERS / REQUIRES FULL REVIEW]
```

---

## 11. Document Relationships

This auditor SOT consolidates information from these source documents (listed here for provenance, not because you need to read them):

| Source Document | What Was Consolidated |
|---|---|
| `TCR_source_of_truth.md` | Project status, progress tracker, Extended Library roadmap, change log |
| `TCR_quality_contract.md` | 3 non-negotiable rules, standing decisions, scaffold policy, two-agent pipeline |
| `TCR_data_reference.md` | JSON schemas, field rules, file structure, source texts |
| `prompts/qa_agent_prompt.md` | 18 validation checks, verdict format, pipeline architecture |
| `prompts/quality-correction-addendum-v1.3.md` | Detailed non-negotiable rules with examples |
| `prompts/multi-agent-consistency-rules.md` | Term register, ER density, key_terms schema, locked formulas |
| `prompts/dss-isaiah-generation-prompt.md` | DSS variant schema, significance levels, manuscript references |
| `prompts/extended-library-direction.md` | Tradition tiers, stacking UI, variant verse schema, implementation priorities |
| `scripts/qa_validate.py` | Automated check implementation, NT support, textual-critical omissions |
| `scripts/audit_books.py` | ER density audit, preamble completeness audit |
| `scripts/nt_ot_crossref.py` | NT→OT cross-reference injection logic |
| `tcr-search-api/server.js` | AI search API — Claude-powered semantic search, tiered context strategy, query classification, deployed on VPS |

---

*Version 2.1 — 2026-04-11*
