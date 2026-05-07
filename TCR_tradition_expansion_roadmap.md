# The Covenant Rendering — Full Tradition Expansion Roadmap

**Goal:** Every verse in TCR shows all available ancient tradition readings side by side. Every tradition is also browsable standalone in the Library index.

**Owner:** Aaron Blonquist
**Created:** 2026-04-19
**Status:** Planning

---

## Table of Contents

1. [What Exists Today](#1-what-exists-today)
2. [What's Missing](#2-whats-missing)
3. [Schema Decision: Does the Verse Format Need to Change?](#3-schema-decision)
4. [Phase 1: Complete JST Footnotes](#phase-1)
5. [Phase 2: Expand Vulgate to All 73 Books](#phase-2)
6. [Phase 3: Expand LXX to Full OT Coverage](#phase-3)
7. [Phase 4: Expand DSS Beyond Isaiah](#phase-4)
8. [Phase 5: Expand Targumim to Comprehensive Coverage](#phase-5)
9. [Phase 6: Samaritan Pentateuch Gap Check](#phase-6)
10. [Phase 7: Website — Generalize Stacking UI](#phase-7)
11. [Phase 8: AI Search API — Index Tradition Data](#phase-8)
12. [Phase 9: Preamble & Summary Audit](#phase-9)
13. [Phase 10: Full QA & Cross-Tradition Consistency Audit](#phase-10)
14. [Execution Order & Dependencies](#execution-order)
15. [Risk Register](#risk-register)

---

## 1. What Exists Today

### Standard Bible (complete)
- 66 books, 1,189 chapters, 31,169 verses
- All passing automated QA
- Deployed at thecovenantrendering.com

### Extended Library Traditions (all deployed, all partial)

| Tradition | Files | Entries | Coverage | Format |
|---|---|---|---|---|
| **DSS Isaiah** | 66 chapter files | 590 variants | Isaiah only (1 of ~30 books with DSS fragments) | Per-chapter |
| **LXX Jeremiah** | 52 chapter files | Verse-level variants | Jeremiah only (1 of 39 OT books with LXX text) | Per-chapter |
| **LXX Daniel** | 15 files (12 ch + 3 additions) | Verse-level variants | Daniel only | Per-chapter |
| **LXX Esther** | 16 files (10 ch + 6 additions) | Verse-level variants | Esther only | Per-chapter |
| **Samaritan Pentateuch** | 5 book files | 156 variants | All 5 Pentateuch books | Per-book |
| **Targum Onkelos** | 5 book files | 176 renderings | All 5 Pentateuch books | Per-book |
| **Targum Jonathan** | 5 book files | 153 renderings | 5 prophetic groupings | Per-book |
| **Vulgate** | 9 book files | 184 renderings | 9 of 73 books | Per-book |
| **JST Footnotes** | 1 file | 111 entries | ~18% of published footnotes | Single file |
| **JST Appendix** | 1 file | 14 passages | ~93% of published appendix | Single file |
| **JST Book of Moses** | 8 chapter files | 356 verses | Complete | Per-chapter |
| **JST JS-Matthew** | 1 file | 55 verses | Complete | Single file |
| **1 Enoch** | 108 chapter files | 1,054 verses | Complete (standalone) | Per-chapter |
| **Jubilees** | 50 chapter files | 1,245 verses | Complete (standalone) | Per-chapter |

### Website Stacking Infrastructure
- `getStackedTraditions()` function exists in `tcr.ts` (lines 1158-1434)
- `TraditionStack.astro` component renders verse-level tradition data
- Color-coded by tradition type (amber=manuscript, purple=Targum, blue=Vulgate, green=JST)
- Book routing is **hardcoded** — each book has manually specified tradition lookups
- Works today for the 9 Vulgate books, DSS Isaiah, LXX 3 books, SP 5 books, Targumim 10 books, JST scattered

### AI Search API
- Indexes 66 canonical + 11 extended book directories
- Does NOT index tradition variant data (Vulgate renderings, Targum renderings, DSS variants, JST footnotes)
- Claude gets base chapter data only — no tradition context in answers

---

## 2. What's Missing

### Data Gaps

| Tradition | Have | Need | Gap |
|---|---|---|---|
| **Vulgate** | 9 books, 184 renderings | 73 books (all Vulgate canon incl. 7 deuterocanonical) | 64 books |
| **LXX** | 3 divergent books (Jer, Dan, Esther) | All 39 OT books where LXX meaningfully diverges from MT | ~36 books |
| **DSS** | Isaiah only | All books with significant DSS fragments (Psalms, Deuteronomy, Samuel, Exodus, Leviticus, Numbers, Genesis, Jeremiah, Ezekiel, Daniel, Minor Prophets) | ~15-20 books |
| **Targum Onkelos** | 176 renderings across 5 books | Comprehensive: every verse where Onkelos meaningfully departs from MT literal | Hundreds more renderings |
| **Targum Jonathan** | 153 renderings across 5 groupings | Comprehensive: all Prophets (Former + Latter) with meaningful departures | Hundreds more renderings |
| **JST Footnotes** | 111 entries | All ~600+ published LDS Bible JST footnotes | ~500 entries |
| **JST Appendix** | 14 passages | Verify completeness against published LDS Bible appendix | Small gap if any |
| **Samaritan Pentateuch** | 156 variants | Verify — may already be substantially complete for significant variants | Audit needed |

### Website Gaps
- `getStackedTraditions()` is hardcoded per-book — won't scale to 73 Vulgate books or 39 LXX books
- No tradition data appears for most Bible books (e.g., Exodus has no Vulgate, no LXX, limited Targum)
- No canon filter UI on `/books` page

### AI Search Gaps
- Tradition data not indexed — Claude can't answer "How does Jerome translate Genesis 3:15?" or "What does the Targum say about the Suffering Servant?"

---

## 3. Schema Decision: Does the Verse Format Need to Change?

**Answer: No. The current architecture scales.**

The two-layer model works:
- **Base chapter files** (`genesis/genesis-01.json`) contain the TCR rendering with Hebrew/Greek, KJV, notes, key_terms
- **Tradition files** (`vulgate/genesis.json`, `targum-onkelos/genesis.json`) contain variant/rendering data keyed by reference string
- **Website merges them at render time** via `getStackedTraditions()`

This is the right architecture because:
1. Base chapters don't bloat as traditions are added
2. Each tradition can be generated, validated, and deployed independently
3. The website already has the merge logic and UI components
4. New traditions just need files + routing entries

**One format change needed:** For traditions that grow to comprehensive coverage (hundreds of renderings per book), the per-book JSON files may become unwieldy. The solution is to **split large per-book files into per-chapter files** when a tradition has >50 renderings per book. This matches what DSS Isaiah and LXX already do.

**Decision matrix:**

| Tradition | Current Format | Keep or Change? |
|---|---|---|
| DSS Isaiah | Per-chapter | Keep |
| LXX (Jer, Dan, Esther) | Per-chapter | Keep |
| LXX (new books) | N/A | Use per-chapter |
| Samaritan Pentateuch | Per-book | Keep (manageable size) |
| Targum Onkelos | Per-book | **Split to per-chapter** when expanded |
| Targum Jonathan | Per-book | **Split to per-chapter** when expanded |
| Vulgate (existing 9) | Per-book | Keep (manageable size per book) |
| Vulgate (new books) | N/A | Per-book (most will be <50 renderings) |
| JST Footnotes | Single file | **Split to per-testament** (OT + NT) when expanded to 600+ |
| JST Appendix | Single file | Keep (small) |

---

## Phase 1: Complete JST Footnotes {#phase-1}

**Why first:** This is the most straightforward gap. The published LDS Bible has ~600+ JST footnotes. We have 111. The schema already exists. The data source is well-documented and publicly available in every LDS edition of the King James Bible.

### 1.1 Inventory

Audit the current 111 entries against the complete published LDS Bible JST footnote list:
1. Obtain or reconstruct the complete list of JST footnotes from the LDS edition
2. Mark which are already in `jst-footnotes.json`
3. Identify all missing entries by book and verse

**Expected result:** A checklist of ~500 missing entries organized by Bible book.

### 1.2 Generation Approach

Generate missing entries in batches by Bible book, using the existing schema:

```json
{
  "reference": "Genesis 6:6",
  "change_summary": "God's regret over making man reframed: divine grief removed or qualified",
  "significance": "theological",
  "notes": [
    "Explanation of what the JST changes and why it matters..."
  ]
}
```

**Significance categories** (match existing): `theological`, `covenantal`, `character`, `clarification`, `christological`, `eschatological`

**Generation rules:**
- Source: Official LDS edition of the KJV (footnotes marked "JST")
- Do NOT use the Community of Christ "Inspired Version"
- Every entry must state what the KJV says, what the JST changes, and why it matters
- Notes must be scholarly and ecumenical — present the JST reading as a tradition, not as the "correct" reading
- No AI attribution in the data

### 1.3 File Structure After Expansion

Split from single file to per-testament for manageability:

```
jst/
├── moses-01.json through moses-08.json  (keep — complete)
├── js-matthew.json                       (keep — complete)
├── jst-appendix.json                     (keep — verify completeness)
├── jst-footnotes-ot.json                 (NEW — all OT footnotes)
└── jst-footnotes-nt.json                 (NEW — all NT footnotes)
```

**Website impact:** Update `loadPerBookTradition()` calls in `getStackedTraditions()` to load from the new split files.

### 1.4 Validation

- Every entry has: `reference`, `change_summary`, `significance`, `notes[]`
- Every `reference` parses correctly (book chapter:verse format)
- No duplicate references
- Cross-check count against published LDS Bible footnote count
- Spot-check 20 random entries against physical LDS Bible

### 1.5 Deliverables

- [ ] Complete inventory of all published JST footnotes
- [ ] ~500 new entries generated
- [ ] `jst-footnotes-ot.json` and `jst-footnotes-nt.json` created
- [ ] Old `jst-footnotes.json` archived (not deleted — verify migration first)
- [ ] Website `getStackedTraditions()` updated to load new files
- [ ] `jst-appendix.json` verified complete against published LDS Bible appendix
- [ ] AI search index updated

---

## Phase 2: Expand Vulgate to All 73 Books {#phase-2}

**Why:** Jerome's Latin Vulgate was the Bible of Western Christianity for over 1,000 years. Every significant Jerome rendering choice shaped theology, liturgy, art, and law. Currently we have 9 books (184 renderings). The full Vulgate covers 73 books — the 66 Protestant books plus 7 deuterocanonical books (Tobit, Judith, Wisdom of Solomon, Sirach, Baruch, 1 Maccabees, 2 Maccabees).

### 2.1 Scope & Approach

The Vulgate tradition files are NOT verse-by-verse translations of the entire Latin text. They document **where Jerome's Latin rendering meaningfully diverges from the Hebrew/Greek in ways that shaped theology, liturgy, or Western Christian tradition.** This is a variant-comparison model, not a parallel Bible.

**Per-book target:** 15-40 renderings for most books. More for theologically dense books (Psalms, Isaiah, Romans, John). Fewer for short or straightforward books (Obadiah, Philemon, 3 John).

**Deuterocanonical books are different:** For Tobit, Judith, Wisdom, Sirach, Baruch, 1-2 Maccabees, the Vulgate IS the primary accessible text (these books don't exist in the Hebrew Bible). These need a different format — closer to TCR's standard chapter rendering (rendering + notes) since there's no MT to compare against. They should be full renderings from Jerome's Latin, not variant comparisons.

### 2.2 Book List

**OT books to add (30 books):**

| Book | Expected Renderings | Key Jerome Choices to Document |
|---|---|---|
| Exodus | 20-25 | Creation of "tabernaculum" terminology, legal vocabulary |
| Leviticus | 15-20 | Sacrificial vocabulary, purity language |
| Numbers | 10-15 | Census/military vocabulary |
| Deuteronomy | 20-25 | "Testamentum" for covenant, legal terms |
| Joshua | 10-15 | Conquest vocabulary |
| Judges | 10-15 | "Salvator" for deliverer |
| Ruth | 5-8 | Propinquus (kinsman) for go'el |
| 1 Samuel | 15-20 | Christus Domini for mashiach YHWH |
| 2 Samuel | 15-20 | Davidic covenant vocabulary |
| 1 Kings | 15-20 | Temple terminology |
| 2 Kings | 10-15 | Prophetic formulas |
| 1 Chronicles | 10-15 | Liturgical vocabulary |
| 2 Chronicles | 10-15 | Temple and worship terms |
| Ezra | 8-12 | Aramaic section handling |
| Nehemiah | 8-12 | Post-exilic vocabulary |
| Esther | 8-10 | Court vocabulary (no deuterocanonical additions — those are LXX Esther) |
| Job | 20-25 | Famous cruxes (19:25 "redemptor"), rare vocabulary |
| Proverbs | 15-20 | Wisdom vocabulary, "sapientia" |
| Ecclesiastes | 10-15 | "Vanitas vanitatum" for hevel |
| Song of Solomon | 10-12 | Love/body vocabulary, allegorical tradition |
| Lamentations | 8-10 | Dirge vocabulary |
| Ezekiel | 15-20 | Vision vocabulary, temple measurements |
| Hosea | 8-10 | Marriage metaphor vocabulary |
| Joel | 5-8 | Eschatological vocabulary |
| Amos | 8-10 | Justice vocabulary |
| Obadiah | 3-5 | Shortest book |
| Jonah | 5-8 | Sea/fish vocabulary |
| Micah | 8-10 | Justice/mercy vocabulary |
| Nahum–Malachi (8 books) | 3-8 each | Prophetic formulas, eschatology |

**NT books to add (20 books):**

| Book | Expected Renderings | Key Jerome Choices |
|---|---|---|
| Mark | 15-20 | Textual ending handling, Latinisms |
| Luke | 20-25 | Birth narratives, magnificat/benedictus |
| John | 25-30 | Logos/Verbum, "I am" statements, Paraclete |
| Acts | 15-20 | Ecclesia, apostolus, Western text notes |
| 1 Corinthians | 15-20 | Caritas (love), spiritual gifts vocabulary |
| 2 Corinthians | 10-15 | Ministry/reconciliation vocabulary |
| Galatians | 10-12 | Justificatio, libertas |
| Ephesians | 10-12 | Cosmic vocabulary, "sacramentum" for mysterion |
| Philippians | 8-10 | Kenosis hymn rendering |
| Colossians | 8-10 | Primogenitus, plenitudo |
| 1-2 Thessalonians | 5-8 each | Parousia vocabulary |
| 1-2 Timothy | 8-10 each | Pastoral/ecclesiastical vocabulary |
| Titus | 5-8 | Grace vocabulary |
| Philemon | 3-5 | Shortest epistle |
| James | 8-10 | Faith/works vocabulary |
| 1-2 Peter | 8-10 each | Suffering, eschatology |
| 1-3 John | 5-10 | Love/truth vocabulary |
| Jude | 5-8 | Enoch quotation handling |

**Deuterocanonical books (7 books — NEW standalone renderings):**

| Book | Chapters | Expected Format |
|---|---|---|
| Tobit | 14 | Full chapter renderings from Latin (narrative) |
| Judith | 16 | Full chapter renderings from Latin (narrative) |
| Wisdom of Solomon | 19 | Full chapter renderings from Latin (wisdom poetry) |
| Sirach (Ecclesiasticus) | 51 | Full chapter renderings from Latin (wisdom) |
| Baruch | 6 | Full chapter renderings from Latin (prophecy + Letter of Jeremiah) |
| 1 Maccabees | 16 | Full chapter renderings from Latin (history) |
| 2 Maccabees | 15 | Full chapter renderings from Latin (history) |

### 2.3 Schema for Existing-Canon Vulgate Books

Same as current (per-book JSON with `renderings[]` array):

```json
{
  "meta": {
    "project": "The Covenant Rendering",
    "version": "1.0.0",
    "book": "Exodus",
    "tradition": "vulgate",
    "tradition_label": "Latin Vulgate",
    "source_text": "Biblia Sacra Vulgata (Stuttgart critical edition)",
    "base_text": "Westminster Leningrad Codex (WLC)",
    "translator": "Jerome (Eusebius Sophronius Hieronymus)",
    "date": "382-405 CE",
    "generated_at": "2026-...",
    "prompt_version": "2.0",
    "license": "CC-BY-4.0"
  },
  "preamble": {
    "summary": "...",
    "notable_renderings": "...",
    "theological_legacy": "..."
  },
  "renderings": [
    {
      "reference": "Exodus 3:14",
      "source_text": "אֶהְיֶה אֲשֶׁר אֶהְיֶה",
      "vulgate_text": "ego sum qui sum",
      "vulgate_rendering": "I am who I am",
      "tcr_rendering": "I AM WHO I AM",
      "theological_legacy": "...",
      "notes": ["..."]
    }
  ]
}
```

### 2.4 Schema for Deuterocanonical Books

These need a NEW schema — they're standalone renderings from Latin, not variant comparisons:

```json
{
  "meta": {
    "project": "The Covenant Rendering",
    "version": "1.0.0",
    "book": "Tobit",
    "tradition": "vulgate",
    "tradition_label": "Latin Vulgate",
    "source_text": "Biblia Sacra Vulgata (Stuttgart critical edition)",
    "translator": "Jerome",
    "date": "382-405 CE",
    "canon": ["catholic", "orthodox", "ethiopian"],
    "not_in": ["protestant"],
    "generated_at": "2026-...",
    "prompt_version": "2.0",
    "license": "CC-BY-4.0"
  },
  "preamble": {
    "summary": "...",
    "remarkable": "...",
    "friction": "...",
    "connections": "..."
  },
  "verses": [
    {
      "verse": 1,
      "text_latin": "Tobias ex tribu et civitate Nephthali...",
      "rendering": "Tobit, of the tribe and city of Naphtali...",
      "translator_notes": ["..."],
      "key_terms": [
        {
          "latin": "Nephthali",
          "rendered_as": "Naphtali",
          "note": "..."
        }
      ]
    }
  ]
}
```

**File structure:**
```
vulgate/
├── genesis.json          (existing — keep)
├── exodus.json           (NEW)
├── leviticus.json        (NEW)
├── ... (all 66 Protestant canon books)
├── psalms.json           (existing — keep)
├── tobit/                (NEW — deuterocanonical, per-chapter)
│   ├── chapter-01.json
│   └── ...
├── judith/               (NEW)
├── wisdom/               (NEW)
├── sirach/               (NEW)
├── baruch/               (NEW)
├── 1-maccabees/          (NEW)
└── 2-maccabees/          (NEW)
```

### 2.5 Generation Rules

- **Source:** Stuttgart Vulgate (Biblia Sacra Vulgata, 5th edition) — the critical text
- **For Protestant canon books:** Document Jerome's Latin where it meaningfully diverges from Hebrew (OT) or Greek (NT). "Meaningfully" means: shaped theology, liturgy, art, law, or created a lasting English word (e.g., "firmament" from firmamentum)
- **For deuterocanonical books:** Full rendering from the Latin into modern English. Same quality standard as TCR base text — clear, modern, documented
- **Every rendering must include:** `vulgate_text` (Latin), `vulgate_rendering` (English of the Latin), `tcr_rendering` (TCR's Hebrew/Greek-based rendering for comparison), `theological_legacy` (why this choice mattered), `notes[]`
- **Do not include trivial differences** (word order, conjunctions, articles) unless they shaped theology
- **Preamble required** for every book file — summary of Jerome's approach to that book, notable renderings, theological legacy

### 2.6 Website Registration

Each deuterocanonical book needs:
1. Entry in `BOOKS` array in `tcr.ts` with `tier: 'extended'`, `section: 'deuterocanonical'`, `sourceText: 'vulgate'`
2. Chapter page routing
3. Entry on `/books` Library page under "Deuterocanonical" section

Each Protestant-canon Vulgate file needs:
1. `alternateEditions` entry on the corresponding book in `BOOKS` array (most already have this)
2. Routing in `getStackedTraditions()` (currently hardcoded — will be generalized in Phase 7)

### 2.7 Validation

- Every rendering has all required fields
- Every `reference` parses correctly
- Latin text verified against Stuttgart Vulgate where possible
- Deuterocanonical chapter files pass same structural QA as standard Bible chapters
- No duplicate references within a book file
- Spot-check 10 renderings per book against scholarly sources

### 2.8 Deliverables

- [ ] 57 new Vulgate per-book files for Protestant canon (30 OT + 20 NT + 7 existing = 57 new)
- [ ] 7 deuterocanonical books as per-chapter rendering files (~137 chapters total)
- [ ] All existing 9 Vulgate files reviewed for consistency with new generation standards
- [ ] Website book registration for 7 deuterocanonical books
- [ ] Website stacking routing updated for all 66 Protestant canon books

---

## Phase 3: Expand LXX to Full OT Coverage {#phase-3}

**Why:** The Septuagint was the Bible of the early church. The New Testament quotes the OT from the LXX more often than from the Hebrew. Currently we cover only the 3 most divergent books (Jeremiah, Daniel, Esther). Every OT book has an LXX text, and many have theologically significant variants.

### 3.1 Scope

**High-divergence books (per-chapter variant files):**

| Book | Divergence | Key Differences |
|---|---|---|
| Jeremiah | Major | DONE — 52 chapters |
| Daniel | Major | DONE — 15 files |
| Esther | Major | DONE — 16 files |
| Psalms | Moderate-High | Different numbering (Ps 9-10 = LXX Ps 9; Ps 147 split), Psalm 151, vocabulary |
| Proverbs | Moderate | Different arrangement of chapters 25-31, significant additions |
| Job | Moderate | LXX is ~1/6 shorter than MT, significant omissions |
| 1 Samuel | Moderate | David and Goliath shorter in LXX (17:12-31 absent), significant for textual criticism |
| Exodus | Moderate | Tabernacle chapters rearranged |
| Isaiah | Moderate | Significant Messianic passage variants (7:14 parthenos, 9:6, 52:13-53:12) |

**Standard-divergence books (per-book variant files, 15-30 renderings each):**

All remaining OT books where LXX meaningfully differs. This covers the Pentateuch (Genesis, Leviticus, Numbers, Deuteronomy), Historical Books (Joshua, Judges, Ruth, 2 Samuel, 1-2 Kings, 1-2 Chronicles, Ezra, Nehemiah), remaining Prophets (Lamentations, Ezekiel, all 12 Minor Prophets), and remaining Wisdom (Ecclesiastes, Song of Solomon).

### 3.2 Schema

**Per-chapter files** (high-divergence books) — same schema as existing LXX files:

```json
{
  "meta": {
    "tradition": "lxx",
    "tradition_label": "Septuagint (LXX)",
    "source_text": "Rahlfs' Septuaginta",
    "base_text": "Westminster Leningrad Codex (WLC)"
  },
  "verses": [
    {
      "verse": 1,
      "has_variant": true,
      "significance": "moderate",
      "mt_reading": "Hebrew text...",
      "lxx_reading": "Greek text...",
      "mt_rendering": "MT rendering...",
      "variant_rendering": "LXX rendering...",
      "variant_notes": ["..."]
    }
  ]
}
```

**Per-book files** (standard-divergence books) — use `renderings[]` array keyed by reference, matching Vulgate pattern but with LXX fields:

```json
{
  "meta": {
    "tradition": "lxx",
    "tradition_label": "Septuagint (LXX)",
    "source_text": "Rahlfs' Septuaginta"
  },
  "renderings": [
    {
      "reference": "Genesis 2:7",
      "mt_reading": "עָפָר מִן־הָאֲדָמָה",
      "lxx_reading": "χοῦν ἀπὸ τῆς γῆς",
      "mt_rendering": "dust from the ground",
      "lxx_rendering": "clay from the earth",
      "significance": "moderate",
      "notes": ["LXX choun (clay/dust) is closer to Jerome's limus..."]
    }
  ]
}
```

### 3.3 File Structure

```
lxx-jeremiah/           (existing — keep)
lxx-daniel/             (existing — keep)
lxx-esther/             (existing — keep)
lxx-psalms/             (NEW — per-chapter, high divergence)
lxx-proverbs/           (NEW — per-chapter, moderate-high divergence)
lxx-job/                (NEW — per-chapter, moderate divergence)
lxx-1-samuel/           (NEW — per-chapter, moderate divergence)
lxx-exodus/             (NEW — per-chapter, moderate divergence)
lxx-isaiah/             (NEW — per-chapter, moderate divergence)
lxx/                    (NEW — per-book files for standard divergence)
├── genesis.json
├── leviticus.json
├── numbers.json
├── deuteronomy.json
├── joshua.json
├── judges.json
├── ruth.json
├── 2-samuel.json
├── 1-kings.json
├── 2-kings.json
├── 1-chronicles.json
├── 2-chronicles.json
├── ezra.json
├── nehemiah.json
├── ecclesiastes.json
├── song-of-songs.json
├── lamentations.json
├── ezekiel.json
├── hosea.json
├── ... (all 12 minor prophets)
└── malachi.json
```

### 3.4 Generation Rules

- **Source:** Rahlfs' Septuaginta (standard critical edition)
- **Focus on meaningful divergences:** theological reinterpretations, significant additions/omissions, vocabulary choices that shaped NT theology, passages where the NT quotes LXX against MT
- **Always note when the NT follows the LXX reading** — this is crucial for understanding how the early church read the OT
- **Document Greek text** alongside Hebrew MT for every variant
- **Significance levels:** `theological` (changes meaning), `major` (significant addition/omission), `moderate` (notable vocabulary/interpretation), `minor` (style/grammar)

### 3.5 Deliverables

- [ ] 6 new per-chapter LXX book directories (Psalms, Proverbs, Job, 1 Samuel, Exodus, Isaiah)
- [ ] ~20 new per-book LXX files for standard-divergence books
- [ ] Website routing for all new LXX traditions
- [ ] Standalone browsing pages for high-divergence books

---

## Phase 4: Expand DSS Beyond Isaiah {#phase-4}

**Why:** The Dead Sea Scrolls contain fragments of every OT book except Esther. Some have significant textual variants. Currently we only cover Isaiah (1QIsaᵃ). The most important remaining DSS witnesses are Psalms, Deuteronomy, Samuel, and the Minor Prophets.

### 4.1 Scope

**Substantial fragment coverage (per-chapter variant files):**

| Scroll | Book | Key Content |
|---|---|---|
| 11QPsa (Great Psalms Scroll) | Psalms | Different order of Psalms 91-150, Psalm 151, 4 non-canonical compositions |
| 4QSamᵃ | 1-2 Samuel | Often agrees with LXX against MT; significant for David narratives |
| 4QJer-b | Jeremiah | Shorter text matching LXX (already noted in LXX Jeremiah) |
| 4QDeut | Deuteronomy | "Sons of God" at Deut 32:8 (vs MT "sons of Israel") — major |
| 4QExod-a | Exodus | Variant readings in legal material |
| 1QDan / 4QDan | Daniel | Confirms bilingual structure, minor variants |

**Fragment-level coverage (per-book summary files):**

For books with only small DSS fragments (Genesis, Leviticus, Numbers, Joshua, Judges, Ruth, Kings, Ezekiel, Minor Prophets), create a summary file documenting:
- Which fragments exist and their designations
- Significant variants (if any)
- General assessment of how the DSS fragments compare to MT

### 4.2 Schema

Same as existing DSS Isaiah schema for per-chapter files. For fragment summary files:

```json
{
  "meta": {
    "tradition": "dss",
    "tradition_label": "Dead Sea Scrolls",
    "book": "Genesis",
    "fragments": ["4Q1 (4QGen-Exoda)", "4Q2 (4QGenb)", "4Q4 (4QGend)", "..."],
    "coverage": "fragmentary",
    "total_verses_attested": 89
  },
  "preamble": {
    "summary": "Genesis fragments from 6 Qumran manuscripts...",
    "notable_variants": "...",
    "coverage_assessment": "..."
  },
  "variants": [
    {
      "reference": "Genesis 1:9",
      "fragment": "4Q2",
      "has_variant": true,
      "significance": "minor",
      "mt_reading": "...",
      "dss_reading": "...",
      "notes": ["..."]
    }
  ]
}
```

### 4.3 Deliverables

- [ ] Per-chapter variant files for Psalms (11QPsa), Samuel (4QSamᵃ), Deuteronomy (4QDeut)
- [ ] Per-book fragment summary files for ~15 remaining books with DSS attestation
- [ ] Website routing for new DSS traditions
- [ ] Standalone browsing pages for major scroll witnesses (Psalms, Samuel, Deuteronomy)

---

## Phase 5: Expand Targumim to Comprehensive Coverage {#phase-5}

**Why:** The current 329 renderings (176 Onkelos + 153 Jonathan) are curated highlights. For verse-level stacking to work, we need comprehensive coverage — every verse where the Targum meaningfully departs from literal MT translation.

### 5.1 Scope

**Targum Onkelos (Pentateuch):**
- Current: 176 renderings across 5 books
- Target: ~500-700 renderings (every Memra substitution, anti-anthropomorphism, divine name change, Shekinah insertion, and interpretive expansion)
- Focus areas: Genesis theophanies, Exodus plagues/Sinai, Leviticus sacrificial vocabulary, Numbers wilderness narratives, Deuteronomy blessings/curses

**Targum Jonathan (Prophets):**
- Current: 153 renderings across 5 groupings
- Target: ~400-600 renderings covering all Prophets (Former: Joshua-Kings; Latter: Isaiah-Malachi)
- Focus areas: Messianic reinterpretations, Suffering Servant passages, divine warrior imagery, eschatological expansions

### 5.2 Format Change

When expanded, per-book files will be too large for single JSON files. **Split to per-chapter:**

```
targum-onkelos/
├── genesis/
│   ├── chapter-01.json
│   ├── chapter-02.json
│   └── ...
├── exodus/
│   └── ...
├── leviticus/
│   └── ...
├── numbers/
│   └── ...
└── deuteronomy/
    └── ...

targum-jonathan/
├── joshua/
│   └── ...
├── judges/
│   └── ...
├── 1-samuel/
│   └── ...
├── ... (all Former + Latter Prophets)
└── malachi/
    └── ...
```

**Schema per chapter (same fields, per-chapter structure):**

```json
{
  "meta": {
    "tradition": "targum-onkelos",
    "tradition_label": "Targum Onkelos",
    "book": "Genesis",
    "chapter": 1,
    "source_text": "Targum Onkelos (Sperber critical edition)"
  },
  "renderings": [
    {
      "verse": 1,
      "hebrew_text": "בְּרֵאשִׁית בָּרָא אֱלֹהִים",
      "targum_text": "בקדמין ברא יי",
      "targum_rendering": "In the beginning, the LORD created...",
      "mt_rendering": "In the beginning, God created...",
      "category": "divine-name",
      "notes": ["Onkelos renders Elohim as YY (the LORD)..."]
    }
  ]
}
```

### 5.3 Migration Plan

1. Generate expanded per-chapter files
2. Verify all existing 329 renderings are preserved in the new per-chapter files
3. Archive old per-book files
4. Update website `getStackedTraditions()` to use per-chapter loading
5. Verify stacking renders correctly

### 5.4 Deliverables

- [ ] ~500-700 Targum Onkelos renderings across 187 chapters (5 Pentateuch books)
- [ ] ~400-600 Targum Jonathan renderings across all Prophets
- [ ] Per-chapter file structure for both Targumim
- [ ] All existing renderings preserved (zero regression)
- [ ] Website routing updated

---

## Phase 6: Samaritan Pentateuch Gap Check {#phase-6}

**Why:** The current 156 variants may already be substantially complete for *significant* variants. But we need to verify.

### 6.1 Audit

1. Cross-check current 156 variants against published lists of significant SP variants (e.g., Tal & Florentin critical edition, Tsedaka edition)
2. Categories to verify completeness:
   - Gerizim theology variants (10th commandment, Deut 27:4 Gerizim vs Ebal)
   - Chronological variants (patriarchal ages in Gen 5, 11)
   - Harmonistic expansions (where SP adds text from parallel passages)
   - Proto-Samaritan expansions shared with 4QpaleoExodᵐ
3. Identify any significant gaps

### 6.2 Expand If Needed

If audit reveals significant gaps (>20 missing important variants), generate additional entries in the existing per-book format.

### 6.3 Deliverables

- [ ] Completeness audit report
- [ ] Any missing significant variants added
- [ ] Existing variants verified for accuracy

---

## Phase 7: Website — Generalize Stacking UI {#phase-7}

**Why:** The current `getStackedTraditions()` function (lines 1158-1434 in `tcr.ts`) is hardcoded per-book. Every book has manually specified tradition lookups. This won't scale to 73 Vulgate books, 39 LXX books, and expanded Targumim. We need a data-driven approach.

### 7.1 Replace Hardcoded Routing with Data-Driven Discovery

**Current problem:**
```javascript
// Current: hardcoded per-book checks
if (bookSlug === 'isaiah') {
  // load DSS Isaiah, Targum Jonathan, Vulgate
} else if (bookSlug === 'genesis') {
  // load Samaritan, Targum Onkelos, Vulgate, JST
} // ... 30+ more conditions
```

**New approach:** A tradition registry that maps book slugs to available traditions:

```typescript
interface TraditionSource {
  id: string;               // 'vulgate', 'lxx', 'dss', 'targum-onkelos', etc.
  label: string;
  type: 'variant' | 'rendering' | 'interpretive';
  loadingPattern: 'per-chapter' | 'per-book';
  dataPath: string;         // relative to data root
  dataKey: string;          // 'renderings' | 'variants' | 'footnotes' | 'verses'
  bookSlugs: string[];      // which books this tradition covers
}
```

The function `getStackedTraditions(bookSlug, chapterNum)` would:
1. Look up all `TraditionSource` entries where `bookSlugs` includes the requested book
2. Load each one using the appropriate loading pattern
3. Return the merged `StackedTradition[]`

### 7.2 Canon Filter on `/books` Page

Add a filter control:
- **All traditions** (default) — shows everything
- **Protestant** (66 books)
- **Catholic** (73 books — adds 7 deuterocanonical)
- **Orthodox** (78+ books)
- **Ethiopian** (81+ books — adds 1 Enoch, Jubilees)

### 7.3 Tradition Badge on Chapter Pages

When a chapter has tradition data, show a count: "4 traditions available" with the tradition labels. Currently exists but will be more prominent with expanded coverage.

### 7.4 Deliverables

- [ ] Tradition registry data structure in `tcr.ts`
- [ ] `getStackedTraditions()` rewritten to use registry (data-driven, not hardcoded)
- [ ] All existing tradition rendering verified unchanged after refactor
- [ ] Canon filter on `/books` page
- [ ] Deuterocanonical book pages rendering correctly
- [ ] Build verified — no regressions

---

## Phase 8: AI Search API — Index Tradition Data {#phase-8}

**Why:** Currently the AI search can't answer questions about traditions. "How does Jerome translate Genesis 3:15?" or "What does the Targum say about the binding of Isaac?" return nothing because tradition data isn't in the search index.

### 8.1 Index Expansion

Update `loadBookIndex()` in `server.js` to also index:

**Per-book tradition files:**
- Vulgate: Load `renderings[]` from each vulgate/*.json
- Targum: Load `renderings[]` from each targum-*/*.json (or per-chapter files)
- Samaritan: Load `variants[]` from each samaritan-pentateuch/*.json
- JST: Load `footnotes[]` and `passages[]`
- LXX per-book: Load `renderings[]`

**Per-chapter tradition files:**
- DSS Isaiah: Load `verses[]` where `has_variant === true`
- LXX (Jer, Dan, Esther, + new): Load `verses[]` where `has_variant === true`

**Index structure addition per chapter:**

```javascript
{
  chapter: 1,
  summary: "...",
  // ... existing fields ...
  traditions: {
    vulgate: { count: 3, samples: ["Gen 1:1: firmamentum...", "Gen 1:2: inanis et vacua..."] },
    targum: { count: 2, samples: ["Gen 1:1: Memra substitution..."] },
    dss: { count: 0 },
    lxx: { count: 1, samples: ["Gen 1:2: aoratos kai akataskeuastos..."] },
    jst: { count: 1, samples: ["Gen 6:6: God's regret reframed..."] },
    samaritan: { count: 0 }
  }
}
```

### 8.2 Query Enhancement

Update `buildContext()` to include tradition data when relevant:
- If query mentions "Jerome", "Vulgate", "Latin" → include Vulgate renderings in context
- If query mentions "Septuagint", "LXX", "Greek Old Testament" → include LXX variants
- If query mentions "Dead Sea", "Qumran", "DSS", "scrolls" → include DSS variants
- If query mentions "Targum", "Aramaic", "Onkelos", "Jonathan" → include Targum renderings
- If query mentions "Joseph Smith", "JST", "Inspired Version", "Restoration" → include JST data
- If query mentions "Samaritan", "Gerizim" → include SP variants
- If query mentions "how traditions read" or "compare" or "side by side" → include ALL traditions for that passage

### 8.3 System Prompt Update

Update the Claude system prompt to inform it about available tradition data:
- What each tradition is and its date/significance
- How to cite tradition readings in answers
- When to proactively mention tradition variants (e.g., if someone asks about Isaiah 7:14, note the LXX parthenos and DSS almah readings even if not asked)

### 8.4 Deliverables

- [ ] `loadBookIndex()` expanded to index tradition data
- [ ] `buildContext()` includes tradition data when relevant
- [ ] System prompt updated with tradition awareness
- [ ] Test queries verified:
  - "How does Jerome translate Genesis 3:15?" → returns Vulgate ipsa conteret reading
  - "What does the Targum say about Genesis 22?" → returns Onkelos Memra/Aqedah data
  - "Compare Isaiah 7:14 across traditions" → returns MT, LXX, DSS, Targum readings

---

## Phase 9: Preamble & Summary Audit {#phase-9}

**Why:** With substantially more tradition data stacked on every chapter, the existing preambles may be incomplete or misleading. The "connections" and "friction" sections in particular need updating to reference newly available tradition comparisons.

### 9.1 Scope

All 1,189 standard Bible chapter preambles need review. This is NOT a full rewrite — it's an enrichment pass focused on:

1. **Connections section:** Add tradition comparison notes where they're now available
   - "The Septuagint reads this passage differently — see the LXX variant for this chapter"
   - "Jerome's Latin Vulgate renders X as Y, which shaped the Western theological tradition of Z"
   - "The Targum reinterprets this passage messianically"
   - "The Dead Sea Scrolls preserve an older reading here"
   - "The JST modifies this verse to..."

2. **Friction section:** Add notes about cases where tradition readings illuminate the translation difficulty
   - "The difficulty of this Hebrew word is reflected in the divergent tradition readings: the LXX renders it as X, the Targum as Y"

3. **Summary/Remarkable sections:** Generally leave unchanged unless a tradition comparison is the most remarkable thing about a chapter (e.g., Isaiah 7:14 should mention the LXX/DSS readings in its "remarkable" section)

### 9.2 Priority Order

1. **Chapters with the most tradition data** — these benefit most from updated preambles
2. **Theologically sensitive chapters** — where tradition comparisons change the reader's understanding
3. **All remaining chapters** — even light-touch updates ("See tradition comparisons below")

### 9.3 Approach

Batch by book. For each book:
1. Identify which traditions now have data for this book
2. Read existing preambles
3. For each chapter with tradition data, draft 1-3 additional sentences for connections/friction
4. Validate updated preambles don't exceed ~400 words (keep concise)
5. Write updated chapter files

### 9.4 Deliverables

- [ ] All 1,189 preambles reviewed
- [ ] Tradition comparison notes added to all chapters with stacked tradition data
- [ ] No preambles exceed 400 words
- [ ] Preamble tone consistent (scholarly, ecumenical, no AI attribution)

---

## Phase 10: Full QA & Cross-Tradition Consistency Audit {#phase-10}

**Why:** With thousands of new tradition entries across dozens of books, we need to verify everything is correct, consistent, and properly integrated.

### 10.1 Automated QA

Extend `scripts/qa_validate.py` (or create new `qa_validate_traditions.py`) to check:

1. **JSON integrity:** Every tradition file is valid JSON
2. **Required fields:** Every entry has all required fields for its tradition type
3. **Reference parsing:** Every `reference` string parses to a valid book/chapter/verse
4. **No orphan references:** Every tradition reference points to a verse that exists in the base Bible
5. **No duplicate references:** No two entries in the same tradition file have the same reference
6. **Significance values:** All significance values are in the allowed set (minor/moderate/major/theological)
7. **Category values:** All Targum category values are in the allowed set
8. **Cross-tradition consistency:**
   - If DSS and LXX both have a variant for the same verse, their notes don't contradict each other
   - If Vulgate and Targum both render the same verse, the base TCR rendering cited is identical
9. **Website integration:** Every tradition file is loadable by `getStackedTraditions()`
10. **AI search integration:** Every tradition file is indexed by the search API

### 10.2 Manual Spot-Check

For each tradition, manually verify 20 randomly selected entries against scholarly sources:
- Vulgate entries against Stuttgart Vulgate
- LXX entries against Rahlfs
- DSS entries against DJD/Leon Levy
- Targum entries against Sperber/academic editions
- JST entries against published LDS Bible
- SP entries against Tal & Florentin / Tsedaka

### 10.3 Website Smoke Test

For 10 representative chapters across OT and NT:
1. Load the chapter page
2. Verify all expected traditions appear in the stacking UI
3. Verify tradition color coding is correct
4. Verify collapse/expand behavior
5. Verify verse-level alignment (tradition entries appear next to the correct verse)

### 10.4 AI Search Smoke Test

Run 20 test queries covering all traditions:
1. Specific verse + tradition ("How does the Vulgate render John 1:1?")
2. Topical + tradition ("What do the Targums say about the Messiah?")
3. Cross-tradition comparison ("Compare Genesis 3:15 across all traditions")
4. Extended Library ("What does 1 Enoch say about the Son of Man?")
5. Deuterocanonical ("Summarize the book of Tobit")

### 10.5 Deliverables

- [ ] Automated QA script for tradition files
- [ ] All tradition files pass automated QA
- [ ] 20 manual spot-checks per tradition (documented)
- [ ] 10 website smoke tests (documented)
- [ ] 20 AI search smoke tests (documented)
- [ ] All issues found during audit fixed
- [ ] SOT updated with final tradition counts

---

## Execution Order & Dependencies {#execution-order}

```
Phase 1: JST Footnotes           ─── no dependencies, start immediately
Phase 2: Vulgate Expansion        ─── no dependencies, can parallel with Phase 1
Phase 3: LXX Expansion            ─── no dependencies, can parallel with Phases 1-2
Phase 4: DSS Expansion            ─── no dependencies, can parallel with Phases 1-3
Phase 5: Targumim Expansion       ─── no dependencies, can parallel with Phases 1-4
Phase 6: Samaritan Audit          ─── no dependencies, can parallel with Phases 1-5
    │
    ▼ ── All data generation complete ──
    │
Phase 7: Website Generalization   ─── depends on Phases 1-6 (needs to know full scope)
Phase 8: AI Search Updates        ─── depends on Phases 1-6 (needs data to index)
    │
    ▼ ── Infrastructure updated ──
    │
Phase 9: Preamble Audit           ─── depends on Phases 1-8 (needs all data + stacking working)
Phase 10: Full QA                 ─── depends on all previous phases
```

**Recommended execution strategy:**

1. **Start with Phase 1 (JST)** — smallest scope, highest confidence, validates the workflow
2. **Parallel Phases 2-6** — data generation can happen simultaneously since traditions are independent
3. **Phase 7** (website) can start during data generation for the registry refactor, but final routing depends on knowing all tradition files
4. **Phase 8** (search) can start with index design during data generation
5. **Phases 9-10** are end-of-project quality passes

### Estimated Volume

| Phase | New Files | New Entries/Renderings |
|---|---|---|
| 1: JST | 2 files | ~500 entries |
| 2: Vulgate | ~57 per-book + ~137 per-chapter | ~1,500-2,000 renderings + ~3,000 deuterocanonical verses |
| 3: LXX | ~6 per-chapter dirs + ~20 per-book | ~2,000-3,000 variant entries |
| 4: DSS | ~3 per-chapter dirs + ~15 per-book | ~500-1,000 variant entries |
| 5: Targumim | ~40 per-chapter dirs | ~800-1,300 renderings |
| 6: SP | 0-5 files | 0-50 variants |
| **Total** | ~280+ files | ~5,300-7,850 new entries |

---

## Risk Register {#risk-register}

| Risk | Impact | Mitigation |
|---|---|---|
| **Tradition data quality** — AI generation may introduce errors in Latin/Greek/Aramaic texts | High — scholarly credibility depends on accuracy | Manual spot-checks (Phase 10), use critical editions as source, document uncertainty |
| **JST copyright** — Intellectual Reserve may assert copyright on JST footnote text | Medium — could require removing JST data | We document JST *changes and significance*, not reproduce JST text verbatim. Fair use / scholarly commentary defense. Extended Library Direction already flagged this. |
| **Website performance** — loading 6 tradition files per chapter may be slow | Medium — affects UX | Lazy-load traditions (only load when user expands stacking UI). Per-chapter files are small (<50KB each). |
| **Scope creep** — deuterocanonical books are entire new books, not just variant data | Medium — adds significant scope to Phase 2 | These are high-value content (Catholic/Orthodox readers). Can be deferred to a sub-phase if needed. |
| **LXX coverage depth** — deciding how many variants per book is subjective | Low — but affects consistency | Set clear threshold: include any variant that (a) changes theological meaning, (b) is reflected in NT quotation, (c) differs by >3 words, or (d) has been discussed in scholarly literature |
| **Targum expansion volume** — comprehensive Targum coverage is massive | Medium — may slow execution | Start with highest-value books (Genesis, Isaiah) and expand outward |
| **Preamble audit scope** — 1,189 chapters is a lot of preambles to review | Low — most updates are 1-3 sentences | Batch by book, automate identification of chapters with new tradition data |

---

## SOT Updates Required After This Roadmap

When work begins, update `TCR_source_of_truth.md`:
1. Reference this document in the System Reference table
2. Update Extended Library section with expanded scope targets
3. Update "Next" line in Current State to reflect tradition expansion
4. Update Change Log

---

*"Every tradition that shaped how people read the Bible — from the Dead Sea caves to the Restoration — in one place, side by side, for free."*
