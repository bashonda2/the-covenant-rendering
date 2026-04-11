# The Covenant Rendering — Full Project Roadmap (ARCHIVED)

> **ARCHIVED 2026-04-08.** This roadmap was written 2026-03-29 when 232/1,189 chapters (19.5%) were complete. All six phases have since been completed. See `TCR_source_of_truth.md` (v5.3) for the current state: 66-book Bible (1,189 chapters, 31,169 verses), all 8 Extended Library traditions, preamble enrichment, tooling, and PDFs — all deployed. The document below is preserved as a historical planning artifact.

**Current state at time of writing:** 232/1,189 chapters complete (19.5%). 7 books live on thecovenantrendering.com.
**Date:** 2026-03-29
**Purpose:** Comprehensive roadmap from current state to project completion, for QA validation that nothing is missing.

---

## What's Done

| Item | Detail |
|---|---|
| **Genesis** | 50 chapters, 1,534 verses. Complete. On site. |
| **Exodus** | 40 chapters, 1,213 verses. Complete. On site. |
| **Leviticus** | 27 chapters, 859 verses. Complete. On site. |
| **Numbers** | 36 chapters, 1,288 verses. Complete. On site. |
| **Deuteronomy** | 34 chapters, 956 verses. Complete. On site. |
| **Joshua** | 24 chapters, 658 verses. Complete. On site. |
| **Judges** | 21 chapters, 618 verses. Complete. On site. |
| Website architecture | 86 books registered, mega-menu, `/books` Library page, data-driven pages |
| Data model | `BookInfo` with testament/section/tier/order/canons/sourceText/status/alternateEditions |
| Extended Library data model | `AlternateEdition` expanded with tier/date/scope/preNicaea/description/license. `EditionTier` type. Source texts: targum, jst, vulgate, peshitta. Sections: pre-nicaea-canon, interpretive-traditions. `text_aramaic` on Verse interface. |
| Preamble infrastructure | `Preamble` type, optional `preamble` field on `Chapter`, collapsible UI on chapter pages. First-pass preambles generated per-book starting with Ruth. |
| Quality pipeline | Master prompt, quality addendum v1.3, QA agent prompt, automated QA script, two-agent pipeline |
| Briefing addenda | Leviticus, Joshua, Judges |
| Governing documents | SOT (4-doc architecture), Extended Library Direction, Chapter Preamble Spec |
| Infrastructure | SSL, Nginx, rsync deploy pipeline, GitHub repos (data + site) |

**Total complete:** 232 chapters, 7,126 verses, 0 QA failures.

---

## IMMEDIATE NEXT STEP

**Ruth** — 4 chapters, 85 verses. Per-book workflow:

1. Create `prompts/ruth-briefing-addendum.md` — go'el (kinsman-redeemer) theology, chesed, threshing floor scene, Moabite identity, genealogy as theology
2. Generate chapters 1-4 with full verse content
3. Run automated QA script
4. Two-agent pipeline review (all 4 chapters are watch chapters — the book is short and dense)
5. Cross-book consistency check (go'el against Leviticus 25, chesed against existing usage in Pentateuch/Judges)
6. Generate first-pass preambles for all 4 chapters
7. Copy to site repo, update `tcr.ts` status to `'complete'`, rebuild, deploy
8. Update SOT progress tracker
9. Commit and push both repos

**After Ruth:** 1 Samuel (31 chapters, 810 verses) — monarchy transition, Samuel/Saul/David.

---

## Phase 1: Complete the Old Testament

**Goal:** Finish all 39 OT books from the WLC.
**Remaining:** 33 books, 697 chapters, ~16,017 verses.
**Source text:** Westminster Leningrad Codex (WLC) — same as current books.

### Per-book workflow (unchanged from current process)
1. Create briefing addendum (`prompts/{book}-briefing-addendum.md`) — vocabulary, watch chapters, tone
2. Generate chapters with full verse content (Hebrew, KJV, rendering, translator_notes, key_terms, expanded_rendering)
3. Run automated QA script — zero tolerance for KJV pass-through, boilerplate notes, archaisms
4. Two-agent pipeline review on watch chapters
5. **Cross-book consistency check** — verify register term renderings match across all completed books in the same testament (see Quality Gates)
6. **Generate first-pass preambles** for all chapters in the book (see Phase 5)
7. Copy to site repo, update `tcr.ts` status to `'complete'`, rebuild, deploy
8. Update SOT progress tracker
9. Commit and push both repos

### EVM alignment

TCR generation priority within Phase 1 should stay at or ahead of EVM's (EveryVerseMatters.com) Come Follow Me study calendar. EVM is the primary downstream consumer of this rendering — TCR is the house translation. **If EVM reaches a book that TCR hasn't rendered, that book jumps to the front of the queue.** Canonical order naturally aligns with EVM's pace — the Pentateuch is complete, and EVM won't reach the historical books until mid-2026 at the earliest.

### Aramaic handling decision

Ezra (4:8–6:18, 7:12–26) and Daniel (2:4b–7:28) contain Aramaic text, not Hebrew. The Aramaic uses the same block script as Hebrew, but the field name must be honest about the source language.

**Decision:** Add an optional `text_aramaic` field to the `Verse` interface. For Aramaic verses:
- `text_aramaic` is populated with the Aramaic source text
- `text_hebrew` is omitted (empty string or absent)
- The chapter `meta.source_text` notes "Westminster Leningrad Codex (WLC) — Aramaic section"
- Translator notes acknowledge the language transition

This applies to ~67 verses in Ezra and ~200 verses in Daniel. The site template conditionally displays whichever source text field is present.

### 1A. Historical Books (10 books, 204 chapters)

| Book | Chapters | Verses | Key Challenges | Briefing Needed? |
|---|---|---|---|---|
| **Ruth** | 4 | 85 | go'el theology, chesed, threshing floor scene, genealogy as theology | Yes |
| **1 Samuel** | 31 | 810 | Monarchy transition, Samuel/Saul/David, poetry (Hannah's Song), ruach YHWH on Saul | Yes |
| **2 Samuel** | 24 | 695 | Davidic covenant (ch 7), Bathsheba, succession narrative, poetry (David's lament) | Yes |
| **1 Kings** | 22 | 816 | Temple construction vocabulary, Elijah cycle, prophetic speech formulas, divided kingdom | Yes |
| **2 Kings** | 25 | 719 | Elisha cycle, fall of Samaria/Jerusalem, exile theology | Yes |
| **1 Chronicles** | 29 | 942 | Genealogies (ch 1-9), parallel to Samuel/Kings with theological reframing | Yes |
| **2 Chronicles** | 36 | 822 | Temple focus, Levitical theology, exile and return | Yes |
| **Ezra** | 10 | 280 | Aramaic sections (4:8-6:18, 7:12-26), post-exilic vocabulary, mixed marriages | Yes |
| **Nehemiah** | 13 | 406 | First-person memoir, wall-building, covenant renewal, lists | Yes |
| **Esther** | 10 | 167 | No mention of God, purim etymology, court vocabulary, irony | Yes |

**Notable challenges:**
- Ezra contains Aramaic text (not Hebrew) in chapters 4-6 and 7 — requires Aramaic source handling
- 1-2 Chronicles parallels 1-2 Samuel/Kings — renderings must be consistent where the Hebrew is identical, and divergent where the Chronicler's text differs
- 1 Chronicles 1-9 is dense genealogy — needs honest preamble acknowledgment per preamble spec

### 1B. Wisdom & Poetry (5 books, 243 chapters)

| Book | Chapters | Verses | Key Challenges | Briefing Needed? |
|---|---|---|---|---|
| **Job** | 42 | 1,070 | Sustained poetry (ch 3-41), rare vocabulary (~100 hapax legomena), divine speeches, prose frame | Yes |
| **Psalms** | 150 | 2,461 | Full poetry — parallelism, superscriptions, acrostics, lament/praise/royal/wisdom types, Selah | Yes |
| **Proverbs** | 31 | 915 | Proverbial poetry, personified Wisdom (ch 1-9), numerical sayings, Agur/Lemuel sections | Yes |
| **Ecclesiastes** | 12 | 222 | Qohelet's voice, hebel theology, cyclical structure, disputed interpretive frame | Yes |
| **Song of Solomon** | 8 | 117 | Full poetry, erotic imagery, dramatic voices (bride/groom/chorus), allegory debate | Yes |

**Notable challenges:**
- Psalms is the largest single book (150 chapters, 2,461 verses) — will require extensive parallelization
- Job has the highest concentration of rare Hebrew words in the Bible — many translator_notes will acknowledge genuine uncertainty
- Poetry rendering must preserve parallelism and line breaks throughout — no flattening to prose
- Psalm superscriptions have technical music terms (maskil, miktam, selah) with debated meanings

### 1C. Major Prophets (5 books, 183 chapters)

| Book | Chapters | Verses | Key Challenges | Briefing Needed? |
|---|---|---|---|---|
| **Isaiah** | 66 | 1,292 | Servant Songs, messianic passages, First/Second/Third Isaiah debate, poetry throughout | Yes |
| **Jeremiah** | 52 | 1,364 | Longest book by word count, confessions, prose/poetry alternation, LXX divergence | Yes |
| **Lamentations** | 5 | 154 | Acrostic poetry (4 of 5 chapters), qinah meter, intense emotional register | Yes |
| **Ezekiel** | 48 | 1,273 | Visionary language, temple measurements (ch 40-48), symbolic actions, merkabah | Yes |
| **Daniel** | 12 | 357 | Aramaic sections (2:4-7:28), apocalyptic imagery, court tales, LXX additions | Yes |

**Notable challenges:**
- Isaiah will be the first book with a direct DSS parallel (Great Isaiah Scroll) — rendering choices here set the baseline for future stacking
- Jeremiah's MT is ~1/8 longer than the LXX — rendering notes should acknowledge this for future stacking
- Daniel contains Aramaic (like Ezra) — same source language handling needed
- Ezekiel 40-48 is dense architectural measurement — needs specialized vocabulary handling

### 1D. Minor Prophets (12 books, 67 chapters)

| Book | Chapters | Verses | Key Challenges | Briefing Needed? |
|---|---|---|---|---|
| **Hosea** | 14 | 197 | Marriage metaphor, difficult Hebrew, covenant lawsuit | Yes |
| **Joel** | 3 | 73 | Day of the LORD, locust plague, Spirit outpouring | Yes |
| **Amos** | 9 | 146 | Social justice, visions, shepherd vocabulary | Yes |
| **Obadiah** | 1 | 21 | Shortest OT book, Edom judgment | Yes |
| **Jonah** | 4 | 48 | Narrative (not oracle), psalm in ch 2, irony/humor | Yes |
| **Micah** | 7 | 105 | Bethlehem prophecy, covenant lawsuit, chesed | Yes |
| **Nahum** | 3 | 47 | Acrostic fragment, Nineveh's fall, vivid war imagery | Yes |
| **Habakkuk** | 3 | 56 | Theodicy dialogue, "the righteous shall live by faith," psalm in ch 3 | Yes |
| **Zephaniah** | 3 | 53 | Day of the LORD, remnant theology | Yes |
| **Haggai** | 2 | 38 | Post-exilic temple rebuilding, date formulas | Yes |
| **Zechariah** | 14 | 211 | Night visions (ch 1-8), apocalyptic (ch 9-14), messianic imagery | Yes |
| **Malachi** | 4 | 55 | Dialogue format, tithing, final OT prophet | Yes |

**Notable challenges:**
- Hosea has some of the most difficult Hebrew in the Bible (rivaling Judges 5)
- The Minor Prophets are treated as a single scroll (The Twelve) in the Hebrew tradition — cross-references within The Twelve should be noted
- Several books are very short (Obadiah 1 chapter, Haggai 2 chapters) — quick wins that add up

### Phase 1 totals

| Section | Books | Chapters | Verses |
|---|---|---|---|
| Historical | 10 | 204 | 5,742 |
| Wisdom & Poetry | 5 | 243 | 4,785 |
| Major Prophets | 5 | 183 | 4,440 |
| Minor Prophets | 12 | 67 | 1,050 |
| **Phase 1 total** | **33** | **697** | **16,017** |

**After Phase 1:** 929/1,189 chapters (78.1%). Full Old Testament complete. 39 books on site.

---

## Phase 2: New Testament

**Goal:** Render all 27 NT books from the SBLGNT.
**Volume:** 27 books, 260 chapters, ~7,956 verses.
**Source text:** SBL Greek New Testament (SBLGNT) — new source language.

### Prerequisites (before first NT chapter)
1. **Greek Theologically Rich Terms Register** — parallel to the Hebrew register in addendum v1.2. Key terms: logos, pistis, charis, agape, dikaiosyne, soteria, ekklesia, parakletos, etc.
2. **NT generation prompt addendum** — adapted from master prompt for Koine Greek. Covers:
   - `text_greek` field alongside `text_hebrew` in verse schema (or replacing it for NT)
   - Greek textual variant handling (SBLGNT apparatus notes)
   - Synoptic parallel awareness (Matthew/Mark/Luke shared material)
   - OT quotation identification (where NT quotes LXX vs. Hebrew)
3. **Data model update** — `text_greek` field on `Verse` interface
4. **Site template update** — chapter pages display Greek text for NT books

### 2A. Gospels & Acts (5 books, 117 chapters)

| Book | Chapters | Verses | Key Challenges |
|---|---|---|---|
| **Matthew** | 28 | 1,071 | Sermon on the Mount, OT fulfillment formulas, Synoptic parallels |
| **Mark** | 16 | 678 | Shorter ending vs. longer ending (16:9-20), Markan priority, sandwiching technique |
| **Luke** | 24 | 1,151 | Birth narratives, parables unique to Luke, literary Greek |
| **John** | 21 | 879 | Logos prologue, "I AM" statements, Johannine vocabulary, Pericope Adulterae (7:53-8:11) |
| **Acts** | 28 | 1,007 | Western text variants, speeches, travel narrative, Greek/Aramaic name forms |

### 2B. Pauline Epistles (13 books, 87 chapters)

| Book | Chapters | Verses | Key Challenges |
|---|---|---|---|
| **Romans** | 16 | 433 | Justification theology, dense argumentation, doxology placement debate |
| **1 Corinthians** | 16 | 437 | Spiritual gifts, love chapter (13), resurrection argument (15) |
| **2 Corinthians** | 13 | 257 | Composite letter theory, "thorn in the flesh," divine comfort vocabulary |
| **Galatians** | 6 | 149 | Faith vs. works, allegory of Sarah/Hagar, freedom vocabulary |
| **Ephesians** | 6 | 155 | Cosmic Christology, household codes, armor metaphor |
| **Philippians** | 4 | 104 | Christ hymn (2:5-11), joy vocabulary, kenosis theology |
| **Colossians** | 4 | 95 | Supremacy of Christ (1:15-20), Colossian heresy |
| **1 Thessalonians** | 5 | 89 | Earliest Pauline letter, parousia expectation |
| **2 Thessalonians** | 3 | 47 | Man of lawlessness, eschatological correction |
| **1 Timothy** | 6 | 113 | Pastoral vocabulary, church order, "faithful sayings" |
| **2 Timothy** | 4 | 83 | Paul's farewell, Scripture as theopneustos |
| **Titus** | 3 | 46 | Cretan context, good works emphasis |
| **Philemon** | 1 | 25 | Single-chapter letter, slavery vocabulary, social ethics |

### 2C. General Epistles & Revelation (9 books, 56 chapters)

| Book | Chapters | Verses | Key Challenges |
|---|---|---|---|
| **Hebrews** | 13 | 303 | High priesthood typology, OT quotations (mostly LXX), authorship question |
| **James** | 5 | 108 | Faith and works, wisdom tradition, social justice |
| **1 Peter** | 5 | 105 | Suffering theology, "spirits in prison," diaspora language |
| **2 Peter** | 3 | 61 | Jude parallel, delayed parousia, pseudepigraphy debate |
| **1 John** | 5 | 105 | Johannine vocabulary, antichrist, love/light/truth |
| **2 John** | 1 | 13 | Shortest NT book by verse count |
| **3 John** | 1 | 15 | Personal letter, Diotrephes conflict |
| **Jude** | 1 | 25 | 1 Enoch quotation (vv. 14-15), angelic rebellion, 2 Peter parallel |
| **Revelation** | 22 | 404 | Apocalyptic imagery, OT allusions (no direct quotes), textual variants, 666/616 |

### Phase 2 totals

| Section | Books | Chapters | Verses |
|---|---|---|---|
| Gospels & Acts | 5 | 117 | ~4,786 |
| Pauline Epistles | 13 | 87 | ~1,793 |
| General Epistles & Revelation | 9 | 56 | ~1,139 |
| **Phase 2 total** | **27** | **260** | **~7,718** |

**After Phase 2:** 1,189/1,189 chapters (100%). Full 66-book Bible complete. All books on site.

---

## Phase 3: Extended Library — Standalone Books

**Goal:** Render books outside the Protestant canon that are canonical in other traditions or historically significant pre-Nicaea texts.
**Volume:** 20 books, ~504 chapters.
**Governing doc:** [`prompts/extended-library-direction.md`](prompts/extended-library-direction.md)

### Prerequisites
1. **Per-tradition generation prompts** — adapted from master prompt for each source language:
   - Ge'ez (Ethiopic) for 1 Enoch and Jubilees — rendered from scholarly English translations (Charles, Knibb, VanderKam) with disclosure
   - Greek (LXX) for Deuterocanonical and Orthodox additions
   - Hebrew/Aramaic (DSS editions) for Dead Sea Scrolls standalone texts
2. **Extended Library site sections** — already registered in data model; need content to populate

### 3A. Pre-Nicaea Canon (Priority 2 & 6)

| Book | Chapters | Source | Priority | Why |
|---|---|---|---|---|
| **1 Enoch** | 108 | Ge'ez (Knibb/Charles) | **2** | Quoted in Jude 14-15. Found at Qumran. Shaped early Christian angelology. Ethiopian canon. |
| **Jubilees** | 50 | Ge'ez (VanderKam/Charles) | **6** | Retells Genesis-Exodus. Multiple Qumran copies. Ethiopian canon. Solar calendar theology. |

### 3B. Deuterocanonical / Apocrypha

| Book | Chapters | Source | Canon |
|---|---|---|---|
| Tobit | 14 | LXX | Catholic, Orthodox, Ethiopian |
| Judith | 16 | LXX | Catholic, Orthodox, Ethiopian |
| Wisdom of Solomon | 19 | LXX | Catholic, Orthodox, Ethiopian |
| Sirach | 51 | LXX | Catholic, Orthodox, Ethiopian |
| Baruch | 6 | LXX | Catholic, Orthodox, Ethiopian |
| 1 Maccabees | 16 | LXX | Catholic, Orthodox, Ethiopian |
| 2 Maccabees | 15 | LXX | Catholic, Orthodox, Ethiopian |

### 3C. Orthodox Additions

| Book | Chapters | Source | Canon |
|---|---|---|---|
| 1 Esdras | 9 | LXX | Orthodox, Ethiopian |
| 2 Esdras | 16 | LXX | Orthodox, Ethiopian |
| Prayer of Manasseh | 1 | LXX | Orthodox, Ethiopian |
| Psalm 151 | 1 | LXX | Orthodox, Ethiopian |
| 3 Maccabees | 7 | LXX | Orthodox |
| 4 Maccabees | 18 | LXX | Orthodox |

### 3D. Dead Sea Scrolls — Standalone Texts

| Book | Chapters | Designation | Content |
|---|---|---|---|
| Community Rule | 11 | 1QS | Rule of the Qumran community |
| War Scroll | 19 | 1QM | Eschatological battle: Sons of Light vs. Sons of Darkness |
| Temple Scroll | 67 | 11QT | Idealized temple and Torah rewriting |
| Damascus Document | 20 | CD | Laws and history of the Damascus covenant community |

**Note:** The Great Isaiah Scroll (1QIsaiah-a) is handled in Phase 4 as a stacked alternate edition on Isaiah, not as a standalone book — though it also exists as a standalone entry in the data model for browsing purposes.

---

## Phase 4: Manuscript Stacking

**Goal:** Render alternate manuscript traditions and layer them onto completed base books using the stacking comparison UI.
**Governing doc:** [`prompts/extended-library-direction.md`](prompts/extended-library-direction.md)

### Prerequisites
1. **Variant verse schema** — per-verse structure for manuscript comparisons:
   ```json
   {
     "verse": 3,
     "tradition": "dss-1qisaiah-a",
     "has_variant": true,
     "variant_rendering": "...",
     "variant_notes": ["..."],
     "significance": "minor|moderate|major|theological",
     "manuscript_reference": "1QIsaiah-a, col. XXXIII, line 3"
   }
   ```
2. **Stacking UI** — version tabs / comparison view on chapter pages
3. **Base books must be complete** for meaningful comparison

### 4A. Dead Sea Scrolls — Isaiah (Priority 1)

| Item | Detail |
|---|---|
| Source | 1QIsaiah-a (Great Isaiah Scroll), DJD editions, Leon Levy Digital Library |
| Scope | All 66 chapters — complete manuscript |
| Date | 150–100 BCE |
| Output | Variant annotations on all 66 Isaiah chapters |
| Why first | Highest academic impact. Oldest complete biblical manuscript. Most variant readings. |

### 4B. Septuagint (Priority 3)

| Book | Divergence Level | What's Different |
|---|---|---|
| **Jeremiah** | Major | ~1/8 shorter than MT, different chapter arrangement |
| **Daniel** | Major | Additions: Prayer of Azariah, Susanna, Bel and the Dragon |
| **Esther** | Major | 107 added verses not in Hebrew |
| **Psalms** | Moderate | Psalm 151, different numbering system |
| **Pentateuch** | Minor-moderate | Chronological differences, expansions |
| **Isaiah** | Minor-moderate | Textual variants, interpretive differences |

### 4C. Joseph Smith Translation (Priority 4)

| Scope | Source | Blocking Issue |
|---|---|---|
| Genesis 1-24 (Book of Moses) | Pearl of Great Price | **Copyright research required** — verify Intellectual Reserve status |
| Matthew 24 (JS-Matthew) | Pearl of Great Price | Same copyright question |
| Selected verse revisions (OT + NT) | JST footnotes/appendix in LDS Bible | May have separate restrictions |

**Critical:** JST is categorically different from other traditions — it is a revelatory revision of the KJV English text, not a translation from original languages. UI must communicate this clearly through tier labeling ("Interpretive Traditions: How traditions read this passage").

**Do NOT use:** Community of Christ "Inspired Version."

### 4D. Samaritan Pentateuch (Priority 5)

| Scope | Detail |
|---|---|
| Books | Genesis–Deuteronomy only |
| Variants | ~6,000 readings differ from MT |
| Key theological variant | 10th commandment designates Mt. Gerizim |
| Date | 4th c. BCE divergence from proto-MT |

### 4E. Targumim (Priority 7)

| Targum | Scope | Content |
|---|---|---|
| Targum Onkelos | Torah (Genesis–Deuteronomy) | Closest to literal; standard synagogue Aramaic |
| Targum Jonathan | Prophets (Joshua–Malachi) | More interpretive; messianic expansions |

### 4F. Latin Vulgate (Priority 8 — future consideration)

| Item | Detail |
|---|---|
| Source | Jerome's Latin translation (~400 CE), critical editions (Stuttgart Vulgate) |
| Scope | Full Bible (OT translated from Hebrew, not LXX — making Jerome's choices independently significant) |
| Tier | Interpretive Traditions ("How traditions read this passage") |
| Significance | The Bible of Western Christianity for 1,000+ years. Council of Trent declared it authentic. Still the official Latin Bible of the Catholic Church. |
| Pre-Nicaea? | No (Jerome died 420 CE) — but earlier than any other interpretive tradition in the list except earliest Targum layers |
| New source language | Latin — requires Latin competency in generation prompt |

**Note:** The Peshitta (Syriac, 2nd–5th century CE) is a future consideration beyond Priority 8. Used by Eastern Christian traditions, it represents an independent early translation witness.

### 4G. Stacking UI Build

| Feature | Description |
|---|---|
| Version tabs | Toggle between TCR base and alternate traditions on chapter pages |
| Side-by-side comparison | View two traditions simultaneously |
| Variant significance indicators | Color-coded: minor, moderate, major, theological |
| Tradition metadata | Date, source text, scope, license displayed per tradition |
| Canon filter on `/books` | Protestant / Catholic / Orthodox / Ethiopian / All |

---

## Phase 5: Chapter Preambles (two-pass approach)

**Goal:** Add translator introductions to every chapter across all completed content.
**Governing doc:** [`prompts/chapter-preamble-specification.md`](prompts/chapter-preamble-specification.md)
**Volume:** Every chapter in the project (1,189+ standard Bible chapters plus Extended Library).

### Two-pass strategy

Preambles are generated in two passes to balance timeliness with depth:

**First pass (during Phases 1–3):** Generated as part of the per-book workflow immediately after a book's chapters pass QA. Covers all four preamble sections using what's available at the time:
- **Summary** — always complete (requires only the chapter itself)
- **Remarkable** — always complete (requires only the chapter itself)
- **Friction** — covers Hebrew/Greek resistance based on translator notes and key terms already in the chapter data. References variant readings only if stacked traditions exist at the time of writing.
- **Connections** — links to other Scripture that exists in the rendering at the time. Forward references to unrendered books use general biblical knowledge but cannot cite specific TCR renderings.

**Second pass (after Phase 4):** Enrichment sweep across all preambles once stacking is substantially complete. Updates:
- **Friction** sections gain specific references to variant readings ("The DSS reads this differently — see the comparison view")
- **Connections** sections gain precise cross-references to later books that now exist in the rendering
- Forward references from Phase 1 books to Prophets/NT are verified and sharpened

This means the site has preambles from the moment Ruth goes live, and they get richer as stacking content arrives.

### Per-chapter preamble structure (150-300 words total)

| Section | Purpose |
|---|---|
| **Summary** | 1-2 sentences. Orient the reader. |
| **Remarkable** | The hook — why this chapter is worth reading carefully. |
| **Friction** | Where the Hebrew/Greek resisted English. Name the word, describe the problem, explain the choice. |
| **Connections** | Specific links to other Scripture the reader might miss. |

### Infrastructure (already in place)
- `Preamble` type in data model
- Optional `preamble` field on `Chapter` interface
- Collapsible "Translator's Introduction" UI on chapter pages
- 5 sample preambles in the spec (Genesis 1, Exodus 14, Leviticus 16, Judges 5, Numbers 24:17)

---

## Phase 6: Tooling & Platform Features

These can be built incrementally as the content base grows. No strict ordering required.

| Feature | Description | When Warranted |
|---|---|---|
| **Site search** | Full-text search across all renderings (Pagefind or equivalent) | After ~15+ books |
| **Verse permalinks** | Individual verse URLs (`/genesis/1/1`) for SEO and sharing | After Phase 1 |
| **Concordance** | Cross-book term frequency and usage tracking | After full OT |
| **Cross-reference database** | Machine-readable links between related passages | After full Bible |
| **PDF/print generation** | Formatted output for offline reading | After full Bible |
| **Canon filter UI** | Filter `/books` by Protestant / Catholic / Orthodox / Ethiopian / All | After Phase 3 |
| **DSS fragment viewer** | Partial-chapter rendering for fragmentary manuscripts | During Phase 4 |
| **API** | Public REST or GraphQL endpoint for developer access | After full Bible |

---

## Quality Gates (apply to every phase)

### Per-book quality gate
1. Briefing addendum created with vocabulary, watch chapters, tone guidance
2. All chapters generated with complete verse content
3. Automated QA script passes — zero tolerance:
   - No KJV pass-through (rendering must be independently produced)
   - No boilerplate translator_notes (every note must be chapter-specific)
   - No archaic English (thee/thou/hast/doth/etc.)
   - `key_terms` schema validated (hebrew, transliteration, rendered_as, semantic_range, note)
4. Two-agent pipeline review on watch chapters (judgment-based quality checks)
5. **Cross-book terminology consistency check** — verify register term renderings match across all completed books in the same testament. Reference: Theologically Rich Terms Register (addendum v1.2 for OT; Greek Terms Register for NT). Key terms to verify include but are not limited to: ruach YHWH, berit, chesed, mashiach, navi, go'el, kaphar, shalom, kavod, teshuvah (OT); logos, pistis, charis, agape, dikaiosyne, soteria, ekklesia, parakletos (NT).
6. Poetry rendered as poetry (parallelism, line breaks preserved)
7. `expanded_rendering` on theologically rich terms
8. First-pass preambles generated for all chapters in the book
9. Site builds successfully with new content
10. Deployed and live on thecovenantrendering.com
11. SOT progress tracker updated
12. Both repos committed and pushed

### Per-phase quality gate
- Data model consistent across all books in the phase
- No regressions in previously completed books
- Site navigation and pages render correctly for all content
- README and SOT reflect current state

### Cross-cutting quality standards
- Terminology consistency across entire canon (LORD for YHWH, God for Elohim, covenant for berit, etc.)
- Where books have parallel passages (Chronicles/Samuel-Kings, Synoptic Gospels), renderings are consistent where Hebrew/Greek is identical and appropriately divergent where source text differs
- Ecumenical tone — no denominational bias in translator notes

---

## Dependencies & Blockers

| Item | Depends On | Blocks |
|---|---|---|
| NT generation | Greek Terms Register, NT prompt addendum, `text_greek` schema | Phase 2 |
| 1 Enoch / Jubilees generation | Ge'ez source handling prompt | Phase 3A |
| Deuterocanonical generation | LXX Greek generation prompt | Phase 3B |
| DSS standalone generation | DSS-specific generation prompt | Phase 3D |
| DSS Isaiah stacking | Isaiah base rendering (Phase 1C) complete | Phase 4A |
| LXX stacking | Relevant base books complete + variant verse schema | Phase 4B |
| **JST implementation** | **Copyright research on Intellectual Reserve status** | **Phase 4C — BLOCKED until resolved** |
| Samaritan stacking | Pentateuch complete (done) + variant verse schema | Phase 4D |
| Targumim stacking | Torah + Prophets complete + variant verse schema | Phase 4E |
| Vulgate stacking | Relevant base books complete + Latin generation prompt | Phase 4F |
| Stacking UI | At least one stacked tradition ready | Phase 4G |
| Aramaic verse handling | `text_aramaic` field on Verse interface | Ezra, Daniel generation |
| First-pass preambles | Book's chapters pass QA | Per-book (Phases 1–3) |
| Preamble enrichment (second pass) | Stacking substantially complete | Phase 5 |
| Cross-book consistency | Theologically Rich Terms Register (OT) / Greek Terms Register (NT) | Every book after the first in each testament |

---

## Volume Summary

| Phase | Books | Chapters | Verses (approx) | New Infrastructure |
|---|---|---|---|---|
| Done | 7 | 232 | 7,126 | Website, data model, QA pipeline, deploy pipeline |
| **1: OT Completion** | 33 | 697 | 16,017 | Aramaic handling (Ezra, Daniel), first-pass preambles |
| **2: NT** | 27 | 260 | ~7,718 | Greek terms register, NT prompt, text_greek field, first-pass preambles |
| **3: Extended Library** | 20 | ~504 | TBD | Per-tradition generation prompts, first-pass preambles |
| **4: Manuscript Stacking** | — | — | — | Variant verse schema, stacking UI, canon filter, Vulgate (P8) |
| **5: Preamble Enrichment** | — | — | — | Second-pass update to friction/connections with variant readings |
| **6: Tooling** | — | — | — | Search, permalinks, concordance, PDF, API |

---

## What Could Be Missing (QA Checklist)

Use this checklist to validate completeness:

- [ ] Are all 39 OT books accounted for in Phase 1?
- [ ] Are all 27 NT books accounted for in Phase 2?
- [ ] Are all Extended Library books in the data model accounted for in Phase 3?
- [ ] Is the Aramaic handling for Ezra and Daniel called out with a specific data model decision (`text_aramaic` field)?
- [ ] Is the Greek source text transition documented with prerequisites?
- [ ] Are Synoptic parallel consistency requirements documented?
- [ ] Are Chronicles/Samuel-Kings parallel consistency requirements documented?
- [ ] Is the JST copyright blocker flagged?
- [ ] Are all 7+ tradition priorities from the Extended Library Direction included (DSS, 1 Enoch, LXX, JST, Samaritan, Jubilees, Targumim, Vulgate)?
- [ ] Is the variant verse schema specified for Phase 4?
- [ ] Are preambles two-pass (first pass per-book, second pass after stacking)?
- [ ] Is every per-book quality gate step listed, including cross-book consistency?
- [ ] Are the governing documents all referenced?
- [ ] Is EVM alignment explicitly stated (TCR stays ahead of EVM's Come Follow Me study calendar)?
- [ ] Is the poetry rendering requirement called out for Psalms, Job, Song of Solomon, Lamentations, and prophetic poetry?
- [ ] Are textual variant hotspots flagged? (Mark 16:9-20, John 7:53-8:11, 1 John 5:7-8, etc.)
- [ ] Is the `expanded_rendering` requirement carried forward for all phases?
- [ ] Is the Vulgate listed as a future consideration (Priority 8)?
- [ ] Is the Peshitta noted as a beyond-roadmap possibility?

---

*"Every tradition that shaped how people read the Bible — from the Dead Sea caves to the Restoration — in one place, side by side, for free."*
