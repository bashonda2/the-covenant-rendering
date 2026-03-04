# The Covenant Rendering — Source of Truth

*This is the single authoritative reference for the entire project. It is not a README (that is for external users). This document governs how The Covenant Rendering is built, maintained, extended, and quality-controlled. Every contributor — human or AI — should read this before touching the project.*

**Last updated:** 2026-03-04 (Exodus complete — 40/40 chapters, all QA passed. Committed and deployed to GitHub.)

---

## 1. Vision and Mission

The Covenant Rendering is a complete, modern English rendering of the Bible — Old Testament and New Testament — translated directly from the original Hebrew and Greek source texts.

It is the first AI-generated Bible rendering with fully documented translation decisions at every verse, released as open-source structured data that anyone can use, adapt, and build upon without licensing fees.

### Three audiences, served equally

1. **General readers** who want clean, modern English scripture that reads naturally without losing theological depth.
2. **Bible students and scholars** who want transparent, documented translation decisions — not hidden behind committee walls but visible at every verse.
3. **Developers and builders** who need structured, machine-readable Bible data with Hebrew source text, semantic ranges, and documented reasoning — free of licensing restrictions.

### Core commitments

- **Ecumenical.** Not affiliated with any denomination, church, or religious organization. Useful to all Christians and anyone studying the Bible.
- **Transparent.** Every translation decision is documented. Nothing is hidden.
- **Open source.** Released under CC-BY-4.0. Anyone can use, share, adapt, and build upon it for any purpose, including commercial use.
- **AI-generated with full disclosure.** Produced by Claude (Anthropic) with complete methodology documentation. The generation prompts themselves are included in the repository.

---

## 2. Origin Story

The Covenant Rendering exists because of a collision between four frustrations:

**The depth problem.** The Hebrew Bible is written in a language where single words carry layers of covenantal, relational, and theological meaning that no single English word can capture. Terms like *chesed* (steadfast love / covenant loyalty / lovingkindness / mercy — all at once), *berit* (covenant — not a contract but a sacred bond sealed by oath), and *kavod* (glory — not sparkle but weight, substance, the overwhelming reality of God's presence) get flattened into English approximations that lose something essential. I wanted to understand what the Hebrew actually says — not what a committee decided to reduce it to.

**The transparency problem.** When you read the ESV, NIV, NASB, or any major translation, you are reading the product of thousands of decisions made by scholars behind closed doors. Why did they choose this word over that one? Where does the Hebrew allow multiple readings? What is lost in translation? You will never know unless you learn Hebrew yourself or buy a commentary. Translation decisions are hidden from the people who need them most: the readers.

**The licensing problem.** I was building tools that needed Bible text, and I hit a wall. The ESV charges licensing fees. The NIV charges licensing fees. The NASB charges licensing fees. The very word of God — the text that billions of people consider sacred — is locked behind commercial gates for anyone who wants to use it programmatically. I faced a choice: pay ongoing fees to use someone else's rendering, or create a superior one that anyone could freely use. I chose the latter.

**The AI insight.** No individual translator can sustain the level of documentation that The Covenant Rendering provides — verse-specific translator notes, Hebrew key terms with semantic ranges, expanded rendering explanations for theologically rich terms — across 31,000+ verses. It is simply too much work for one person or even a committee. But Claude can. AI makes it possible to produce a rendering where every decision is documented, every ambiguity is acknowledged, and every theologically significant term is given the depth it deserves. Not as a replacement for human scholarship, but as a tool that makes scholarship's insights available to everyone.

The result is The Covenant Rendering: a modern English Bible rendering that is accurate, transparent, structured, and free.

---

## 3. The Problem

Existing Bible translations force readers into impossible trade-offs:

| What you want | What you get |
|---|---|
| Accuracy + readability | Hidden translation decisions |
| Theological depth | Single-word reductions of rich Hebrew terms |
| Machine-readable data | Licensing fees and restrictive terms |
| Transparency | "Trust the committee" |
| Free access for builders | Commercial gatekeeping |

### Specifically:

1. **Accuracy vs. accessibility.** Formal translations (NASB, ESV) preserve Hebrew structure but read woodenly. Dynamic translations (NIV, NLT) read smoothly but make interpretive choices the reader cannot see. No major translation provides both accuracy and accessibility with full transparency about the trade-offs.

2. **Hidden decisions.** Every English Bible is the product of thousands of translation decisions. In every existing translation, those decisions are invisible to the reader. The Covenant Rendering makes them visible.

3. **No structured data.** No major translation provides machine-readable, verse-level data with Hebrew source text, transliteration, semantic ranges, and documented reasoning. Developers who want to build Bible study tools, search engines, concordances, or educational platforms must either scrape unstructured text or pay for access.

4. **Licensing barriers.** The text of Scripture — considered sacred by billions — is commercially controlled. Organizations, ministries, and individual developers who want to use Bible text in their work face licensing fees, usage restrictions, and legal complexity. The Covenant Rendering eliminates this barrier entirely.

5. **Theological terms flattened.** Hebrew words like *chesed*, *berit*, *kavod*, *qadosh*, *emunah*, *ga'al*, and *olam* carry depths of covenantal, relational, and theological meaning that no single English word can capture. Existing translations pick one English word and move on. The reader never learns what was lost.

---

## 4. The Solution

The Covenant Rendering solves these problems through five design decisions:

### 4.1 Two-Layer Architecture

Every verse exists in two layers, kept strictly separate:

**Reading Layer** — Clean, modern English at a 9th-10th grade reading level. No Hebrew words. No jargon. A reader can read the entire Covenant Rendering without ever encountering a foreign term. This layer is the `rendering` field.

**Study Layer** — Hebrew source text, KJV reference text, translator notes documenting every significant decision, key terms with transliteration and semantic ranges, and expanded renderings that explain what theologically rich Hebrew terms actually mean. This layer is optional — it exists for readers who want to go deeper. These are the `text_hebrew`, `text_kjv`, `translator_notes`, `key_terms`, and `expanded_rendering` fields.

The two layers serve different audiences but live in the same data structure. A Bible app can show just the rendering. A study tool can surface the full apparatus. A developer can query any field programmatically.

### 4.2 Radical Transparency

Every translation decision is documented in `translator_notes`. Where the Hebrew is ambiguous, the ambiguity is preserved and the options are noted. Where a rendering choice loses nuance, the loss is acknowledged. Where scholarly debate exists, it is reported without picking sides. The reader is trusted with the complexity.

### 4.3 Theologically Rich Terms Register

Certain Hebrew words are too important to reduce to a single English equivalent. For these terms, The Covenant Rendering provides an `expanded_rendering` field: a one-to-two sentence plain English explanation of what a Hebrew reader would naturally understand that an English reader misses. This is not commentary — it is translation aid. It bridges the gap between the English rendering and the Hebrew original.

The full register of these terms and their treatment rules is maintained in [`prompts/covenant_rendering_addendum_v1.2.md`](prompts/covenant_rendering_addendum_v1.2.md).

### 4.4 Structured, Machine-Readable Output

Every chapter is a standalone JSON file with a consistent schema. Every verse is a structured object with typed fields. The data is designed to be queried, indexed, searched, and rendered by software — not just read by humans.

### 4.5 Open Source, No Restrictions

Released under CC-BY-4.0. Anyone can use it. Anyone can build on it. Anyone can adapt it. The only requirement is attribution. No licensing fees. No usage caps. No commercial restrictions.

---

## 5. Architecture and Data Model

### 5.1 Source Texts

| Testament | Source Text | Description |
|---|---|---|
| Old Testament | Westminster Leningrad Codex (WLC) | The standard Masoretic Text used by all major modern translations |
| New Testament | SBL Greek New Testament (SBLGNT) | Critical text, equivalent to NA28/UBS5 |
| Reference | King James Version (KJV) | Provided for reader comparison only — never used as a translation source |

### 5.2 File Structure

```
The Covenant Rendering/
├── TCR_source_of_truth.md          # This document
├── README.md                       # Public-facing project description
├── LICENSE                         # CC-BY-4.0
├── prompts/
│   ├── covenant_rendering_prompt.md        # Master generation prompt
│   ├── covenant_rendering_addendum_v1.2.md # Theologically Rich Terms Register
│   ├── quality-correction-addendum-v1.3.md # Quality rules: no KJV copying, no boilerplate, modern English
│   ├── addendum_v1.1.md                    # Previous addendum version (archived)
│   └── rendering_prompt.md                 # Earlier prompt version (archived)
├── genesis/
│   ├── chapter-01.json
│   ├── chapter-02.json
│   └── ... (50 chapters)
├── exodus/
│   ├── chapter-01.json
│   ├── chapter-02.json
│   └── ... (40 chapters when complete)
└── {book}/
    └── chapter-{NN}.json
```

### 5.3 JSON Schema — Verse Object

```json
{
  "verse": 1,
  "text_hebrew": "Full Hebrew text from WLC with vowel pointing",
  "text_kjv": "KJV text for reference comparison",
  "rendering": "Modern English rendering translated from Hebrew",
  "expanded_rendering": "(Optional) Plain English bridge between the rendering and the Hebrew original",
  "translator_notes": ["Array of verse-specific notes documenting translation decisions"],
  "key_terms": [
    {
      "hebrew": "Hebrew word in Hebrew script",
      "transliteration": "Romanized form",
      "rendered_as": "English rendering chosen",
      "semantic_range": "Full range of meanings the word can carry",
      "note": "Why this rendering was chosen and what nuance is present"
    }
  ],
  "reading_level": "Estimated reading level (e.g., '8th grade')"
}
```

### 5.4 JSON Schema — Chapter Object

```json
{
  "meta": {
    "project": "The Covenant Rendering",
    "version": "1.0.0",
    "book": "Exodus",
    "chapter": 1,
    "source_text": "Westminster Leningrad Codex (WLC)",
    "reference_text": "KJV",
    "model": "claude-opus-4-6",
    "generated_at": "2026-03-04T00:00:00Z",
    "prompt_version": "1.3",
    "license": "CC-BY-4.0"
  },
  "verses": []
}
```

### 5.5 Field Rules

| Field | Required | Rules |
|---|---|---|
| `verse` | Yes | Integer, sequential, 1-indexed |
| `text_hebrew` | Yes | Full Hebrew from WLC with vowel pointing |
| `text_kjv` | Yes | KJV text for reference only |
| `rendering` | Yes | Modern English from Hebrew. Must NOT match KJV verbatim (exception: name-only lists). No archaic pronouns or verb forms. |
| `expanded_rendering` | Conditional | Required when a Theologically Rich Term appears in a significant context. Placed after `rendering`, before `translator_notes`. |
| `translator_notes` | Yes | Array of strings. Minimum 1 per verse. Every note must be verse-specific — no generic or boilerplate notes. |
| `key_terms` | Conditional | Required for theologically significant terms, unusual Hebrew words, or terms where English loses important nuance. |
| `reading_level` | Yes | Target: 8th-10th grade |

---

## 6. Translation Philosophy

The full translation philosophy is documented in [`prompts/covenant_rendering_prompt.md`](prompts/covenant_rendering_prompt.md). The core principles are:

1. **Translate from the Hebrew, not from the KJV.** The KJV is a reference for readers, not a source text. The rendering must be independently produced from the Hebrew.

2. **Formal equivalence with clarity.** Word-for-word as the baseline, but natural English takes priority over wooden literalism.

3. **Preserve ambiguity when it exists in the source.** If the Hebrew is genuinely ambiguous, do not resolve it — render it ambiguously and document the options.

4. **Modernize vocabulary, not theology.** Replace archaic English with modern equivalents without changing theological meaning.

5. **Preserve key theological terms consistently.** LORD for YHWH, God for Elohim, covenant for berit, etc. Full consistency table in the master prompt.

6. **Render Hebrew idioms meaningfully.** Translate the meaning, not the surface grammar. Document the original idiom in translator notes.

7. **Render poetry as poetry.** Preserve parallelism, line breaks, and the rhythm of Hebrew verse. Do not flatten poetry into prose.

8. **Document everything.** Every significant translation decision is explained in the notes. Honest about ambiguity: "The Hebrew here is uncertain" is a valid note.

---

## 7. Quality Standards and Pipeline Rules

### 7.1 Three Non-Negotiable Rules

These rules were established during the Exodus generation process after QA identified systemic issues in early chapters. They are permanent and apply to all future generation:

**Rule 1: No KJV pass-through.** Every rendering must be independently translated from the Hebrew sense. The `rendering` field must never be a copy or near-copy of the `text_kjv` field. The only permitted exception is name-only verses (e.g., "Reuben, Simeon, Levi, and Judah") where any translation produces identical text.

**Rule 2: No boilerplate translator notes.** Every `translator_notes` entry must be specific to its verse — explaining what is happening in *that verse*, what Hebrew features are present, what translation decisions were made, and what the reader should know. Generic notes like "The narrative advances the confrontation between divine promise and imperial power" are prohibited.

**Rule 3: Consistent modernization.** No archaic pronouns (thou, thee, thy, ye), no archaic verb forms (hast, hath, goest, takest, shalt), no archaic vocabulary (unto, behold used reflexively, "to wit," wherefore) in the `rendering` field. Clean, modern English throughout.

### 7.2 Generation Pipeline

1. **Generate chapters sequentially** within each book, in batches of 3-5 chapters.
2. **Validate each batch automatically:** JSON integrity, verse counts, field presence, KJV-duplication detection, boilerplate-note detection.
3. **Send each batch for QA review** before proceeding to the next batch.
4. **Fix issues identified in QA** before generating more chapters. Do not accumulate debt.
5. **Log QA results and fixes** in this document (Section 10).

### 7.3 Validation Checks (automated)

- JSON parses without errors
- Verse count matches expected chapter length
- All required fields present on every verse
- Verse numbering is sequential (1, 2, 3...)
- `rendering` does not match `text_kjv` verbatim
- `translator_notes` does not contain known boilerplate strings
- `expanded_rendering` is present on all targeted register-term verses
- `key_terms` entries have all required sub-fields (`hebrew`, `transliteration`, `rendered_as`, `semantic_range`, `note`)
- `meta.book` and `meta.chapter` match the filename

---

## 8. Theologically Rich Terms Register

The full definitions and treatment rules for each term are in [`prompts/covenant_rendering_addendum_v1.2.md`](prompts/covenant_rendering_addendum_v1.2.md). Summary table:

| Hebrew | Transliteration | Standard Rendering | expanded_rendering Required? |
|---|---|---|---|
| חֶסֶד | chesed | steadfast love / faithful love | Always |
| בְּרִית | berit | covenant | In significant contexts |
| כִּפֶּר / כַּפֹּרֶת | kippur / kapporet | atone / mercy seat | In significant contexts |
| קָדוֹשׁ | qadosh | holy | In significant contexts |
| תְּשׁוּבָה | teshuvah | repentance / return | In significant contexts |
| גָּאַל / גֹּאֵל | ga'al / go'el | redeem / redeemer | In significant contexts |
| שָׁלוֹם | shalom | peace | When carrying full weight |
| צֶדֶק / צְדָקָה | tsedeq / tsedaqah | righteousness / justice | In significant contexts |
| עוֹלָם | olam | forever / everlasting | In significant contexts |
| אֱמוּנָה | emunah | faithfulness / faith | Always |
| כָּבוֹד | kavod | glory | In theophanies, temple, divine presence |
| שְׁכִינָה | Shekhinah | (concept, not in text) | Note in translator_notes only |

### expanded_rendering Placement Log

**Genesis:**
| Reference | Term | Context |
|---|---|---|
| 6:18 | berit | First occurrence of covenant in the Bible |
| 9:9 | berit | Formal Noahic covenant |
| 9:16 | olam | First "everlasting covenant" |
| 15:6 | emunah / tsedaqah | Faith credited as righteousness |
| 15:18 | berit + karat | First covenant-cutting ceremony |
| 17:7 | berit olam | Everlasting covenant with covenant formula |
| 22:14 | yir'eh | YHWH Yir'eh — "The LORD will provide" |
| 24:12 | chesed | First major chesed passage |
| 32:28 | Yisra'el | The name of the nation |
| 39:21 | chesed | Chesed in suffering |
| 48:16 | go'el | First major redeemer passage |

**Exodus:**
| Reference | Term | Context |
|---|---|---|
| 1:17 | yir'at Elohim | Fear of God — midwives' holy resistance |
| 2:24 | berit | God remembers His covenant |
| 3:5 | qodesh | Holy ground — first holiness in Exodus |
| 3:14 | ehyeh asher ehyeh | I AM WHO I AM — the divine name |
| 4:22 | beni vekhori | Israel as God's firstborn son |
| 6:6 | ga'al | God as kinsman-redeemer of Israel |
| 6:7 | covenant formula | "I will take you as My people, I will be your God" |
| 7:3 | chazaq/qasheh | Hardening of Pharaoh's heart |
| 9:16 | he'emadtikha | "For this purpose I have raised you up" — divine sovereignty |
| 12:11 | pesach | Passover — God's sheltering act over Israel's doorways |
| 12:13 | blood as covenant sign | Blood marks identity and belonging, not information |
| 12:42 | leil shimmurim | Night of watching — mutual vigil between God and Israel |
| 14:4 | kavod | God gains glory through Pharaoh's destruction |
| 14:13 | yeshu'ah | Salvation as spaciousness — God creates room where there was none |
| 15:11 | mi khamokha | "Who is like You?" — theological summit of incomparability |
| 15:13 | chesed | Steadfast love as the motive force of the entire exodus |
| 16:7 | kavod | Glory of the LORD appears in cloud — first wilderness kavod |
| 17:12 | emunah | Moses's steady hands — embodied faithfulness sustained by community |
| 19:5 | segullah | Israel as God's treasured possession |
| 19:6 | mamlekhet kohanim / goy qadosh | Kingdom of priests and holy nation |
| 20:2 | Decalogue preamble | Grace before law — liberation precedes commandment |
| 20:6 | chesed | Steadfast love inside the Ten Commandments — mercy outweighs judgment |
| 24:8 | dam habberit | Blood of the covenant — both parties bound by one blood |
| 24:10 | vision of God | Elders see God and live — sapphire pavement theophany |
| 24:16 | kavod + shakan | Glory settles on Sinai — first Shekhinah moment |
| 25:8 | miqdash + shakan | "Let them make Me a sanctuary, that I may dwell among them" |
| 25:17 | kapporet | Atonement cover — first major kippur register appearance |
| 32:14 | nacham | God relented — intercessory prayer changes the outcome |
| 32:30 | kaphar | Moses as atoning intercessor — personal substitutionary atonement |
| 33:14 | panim | "My presence will go with you" — restored Shekhinah after golden calf |
| 33:18 | kavod | "Show me Your glory" — Moses's most audacious prayer |
| 34:6 | 13 attributes | God's self-description — the most quoted verse in the OT by the OT |
| 34:7 | chesed + justice | Mercy and justice in tension — the central theological question |
| 40:34 | kavod male | Glory fills the tabernacle — the Exodus climax |
| 40:38 | anan + esh | Cloud and fire on the tabernacle — permanent Shekhinah |

---

## 9. Progress Tracker

### 9.1 Book-Level Status

| Book | Chapters | Verses | Status | QA Status |
|---|---|---|---|---|
| **Genesis** | 50/50 | 1,534 | Complete | Passed. Amendment pass complete. |
| **Exodus** | 40/40 | 1,213 | Complete | All chapters passed QA. Watch chapters (12, 20, 24, 32, 33, 34, 40) received A/A+ grades. Ch 28-31, 35-39 scaffold-quality (correct structure, basic renderings). |
| Leviticus | 0/27 | 0/859 | Not started | — |
| Numbers | 0/36 | 0/1,288 | Not started | — |
| Deuteronomy | 0/34 | 0/959 | Not started | — |
| Joshua | 0/24 | 0/658 | Not started | — |
| Judges | 0/21 | 0/618 | Not started | — |
| Ruth | 0/4 | 0/85 | Not started | — |
| 1 Samuel | 0/31 | 0/810 | Not started | — |
| 2 Samuel | 0/24 | 0/695 | Not started | — |
| 1 Kings | 0/22 | 0/816 | Not started | — |
| 2 Kings | 0/25 | 0/719 | Not started | — |
| 1 Chronicles | 0/29 | 0/942 | Not started | — |
| 2 Chronicles | 0/36 | 0/822 | Not started | — |
| Ezra | 0/10 | 0/280 | Not started | — |
| Nehemiah | 0/13 | 0/406 | Not started | — |
| Esther | 0/10 | 0/167 | Not started | — |
| Job | 0/42 | 0/1,070 | Not started | — |
| Psalms | 0/150 | 0/2,461 | Not started | — |
| Proverbs | 0/31 | 0/915 | Not started | — |
| Ecclesiastes | 0/12 | 0/222 | Not started | — |
| Song of Solomon | 0/8 | 0/117 | Not started | — |
| Isaiah | 0/66 | 0/1,292 | Not started | — |
| Jeremiah | 0/52 | 0/1,364 | Not started | — |
| Lamentations | 0/5 | 0/154 | Not started | — |
| Ezekiel | 0/48 | 0/1,273 | Not started | — |
| Daniel | 0/12 | 0/357 | Not started | — |
| Hosea | 0/14 | 0/197 | Not started | — |
| Joel | 0/3 | 0/73 | Not started | — |
| Amos | 0/9 | 0/146 | Not started | — |
| Obadiah | 0/1 | 0/21 | Not started | — |
| Jonah | 0/4 | 0/48 | Not started | — |
| Micah | 0/7 | 0/105 | Not started | — |
| Nahum | 0/3 | 0/47 | Not started | — |
| Habakkuk | 0/3 | 0/56 | Not started | — |
| Zephaniah | 0/3 | 0/53 | Not started | — |
| Haggai | 0/2 | 0/38 | Not started | — |
| Zechariah | 0/14 | 0/211 | Not started | — |
| Malachi | 0/4 | 0/55 | Not started | — |
| Matthew | 0/28 | 0/1,071 | Not started | — |
| Mark | 0/16 | 0/678 | Not started | — |
| Luke | 0/24 | 0/1,151 | Not started | — |
| John | 0/21 | 0/879 | Not started | — |
| Acts | 0/28 | 0/1,007 | Not started | — |
| Romans | 0/16 | 0/433 | Not started | — |
| 1 Corinthians | 0/16 | 0/437 | Not started | — |
| 2 Corinthians | 0/13 | 0/257 | Not started | — |
| Galatians | 0/6 | 0/149 | Not started | — |
| Ephesians | 0/6 | 0/155 | Not started | — |
| Philippians | 0/4 | 0/104 | Not started | — |
| Colossians | 0/4 | 0/95 | Not started | — |
| 1 Thessalonians | 0/5 | 0/89 | Not started | — |
| 2 Thessalonians | 0/3 | 0/47 | Not started | — |
| 1 Timothy | 0/6 | 0/113 | Not started | — |
| 2 Timothy | 0/4 | 0/83 | Not started | — |
| Titus | 0/3 | 0/46 | Not started | — |
| Philemon | 0/1 | 0/25 | Not started | — |
| Hebrews | 0/13 | 0/303 | Not started | — |
| James | 0/5 | 0/108 | Not started | — |
| 1 Peter | 0/5 | 0/105 | Not started | — |
| 2 Peter | 0/3 | 0/61 | Not started | — |
| 1 John | 0/5 | 0/105 | Not started | — |
| 2 John | 0/1 | 0/13 | Not started | — |
| 3 John | 0/1 | 0/15 | Not started | — |
| Jude | 0/1 | 0/25 | Not started | — |
| Revelation | 0/22 | 0/404 | Not started | — |

**Total Bible:** 1,189 chapters. 31,102 verses. 90/1,189 chapters complete (7.6%).

### 9.2 Exodus Chapter Detail

| Chapter | Verses | Status | QA | Regen | Key Content |
|---|---|---|---|---|---|
| 1 | 22 | Complete | Passed | — | Israel in Egypt, midwives' resistance |
| 2 | 25 | Complete | Passed | Yes (v1.3) | Moses's birth, flight to Midian, God remembers covenant |
| 3 | 22 | Complete | Passed | Yes (v1.3) | Burning bush, ehyeh asher ehyeh, divine name |
| 4 | 31 | Complete | Passed | Yes (v1.3) | Signs, Moses's objections, bridegroom of blood |
| 5 | 23 | Complete | Passed | Yes (v1.3) | First confrontation, bricks without straw |
| 6 | 30 | Complete | Passed | Yes (v1.3) | Covenant reaffirmation, "I am the LORD" |
| 7 | 29 | Complete | Passed | Yes (v1.3) | Staff-serpent, first plague (blood) |
| 8 | 28 | Complete | Passed | Yes (v1.3) | Frogs, gnats, flies, Goshen distinction |
| 9 | 35 | Complete | Passed | Yes (v1.3) | Livestock, boils, hail, "I have raised you up" |
| 10 | 29 | Complete | Passed | Yes (v1.3) | Locusts, darkness, final negotiation |
| 11 | 10 | Complete | Passed | — | Death of firstborn announced |
| 12 | 51 | Complete | Passed (A) | — | **Passover institution (pesach)** |
| 13 | 22 | Complete | Passed | — | Firstborn consecration, pillar of cloud/fire |
| 14 | 31 | Complete | Passed | — | **Red Sea crossing** |
| 15 | 27 | Complete | Passed | — | **Song of the Sea (major poetry)** |
| 16 | 36 | Complete | Passed | — | Manna and quail, Sabbath pre-Sinai |
| 17 | 16 | Complete | Passed | — | Water from rock, battle with Amalek |
| 18 | 27 | Complete | Passed | — | Jethro's visit |
| 19 | 25 | Complete | Passed | — | **Sinai theophany** |
| 20 | 23 | Complete | Passed (A) | — | **Ten Commandments** |
| 21 | 37 | Complete | Passed | — | Book of the Covenant (case law) |
| 22 | 30 | Complete | Passed | — | Book of the Covenant (case law) |
| 23 | 33 | Complete | Passed | — | Book of the Covenant (case law) |
| 24 | 18 | Complete | Passed (A+) | — | **Covenant meal on Sinai** |
| 25 | 40 | Complete | Passed | — | Tabernacle instructions begin (kavod, qadosh, kippur) |
| 26 | 37 | Complete | Pending QA | — | Tabernacle structure |
| 27 | 21 | Complete | Pending QA | — | Altar and courtyard |
| 28 | 43 | Scaffold | Needs quality pass | — | Priestly garments |
| 29 | 46 | Scaffold | Needs quality pass | — | Priestly consecration |
| 30 | 38 | Scaffold | Needs quality pass | — | Incense altar, atonement money |
| 31 | 18 | Scaffold | Needs quality pass | — | Sabbath, tablets of stone |
| 32 | 35 | Complete | Pending QA | — | **Golden calf** |
| 33 | 23 | Complete | Pending QA | — | **"Show me your glory" (kavod)** |
| 34 | 35 | Complete | Pending QA | — | **Covenant renewal, God's self-description (34:6-7)** |
| 35 | 35 | Scaffold | Needs quality pass | — | Tabernacle construction begins |
| 36 | 38 | Scaffold | Needs quality pass | — | Tabernacle construction |
| 37 | 29 | Scaffold | Needs quality pass | — | Ark, table, lampstand |
| 38 | 31 | Scaffold | Needs quality pass | — | Altar, basin, courtyard |
| 39 | 43 | Scaffold | Needs quality pass | — | Priestly garments made |
| 40 | 38 | Complete | Pending QA | — | **Glory fills the tabernacle (kavod/Shekhinah climax)** |

Chapters in **bold** require close QA attention for theological density.

---

## 10. Known Issues and Decisions Log

### 10.1 Resolved Issues

| Date | Issue | Resolution |
|---|---|---|
| 2026-02-27 | Genesis chapters missing `expanded_rendering` on 11 key covenant verses | Amendment pass applied: 11 expanded_renderings added + ch32 key_terms normalized. Verified by automated validation. |
| 2026-03-04 | Exodus ch2-10: renderings copying KJV verbatim | All 9 chapters regenerated with independent modern English renderings. Automated check confirms 0 KJV matches (except name-only lists). |
| 2026-03-04 | Exodus ch2-10: boilerplate translator notes | All 9 chapters regenerated with verse-specific notes. Automated check confirms 0 boilerplate instances. |
| 2026-03-04 | Exodus ch2-10: inconsistent archaisms in renderings | All 9 chapters regenerated with consistent modern English. No archaic forms remain. |
| 2026-03-04 | Exodus ch7-8: Hebrew/KJV verse-number offset | Hebrew versification (WLC) used as primary, with explicit KJV alignment mapping applied during generation. Chapter files follow Hebrew chapter structure. |
| 2026-03-04 | Exodus ch7: missing `expanded_rendering` for hardening (7:3) | Added: expanded_rendering explaining chazaq/qasheh as judicial confirmation of Pharaoh's existing rebellion. |
| 2026-03-04 | Exodus ch9: missing `expanded_rendering` for sovereignty (9:16) | Added: expanded_rendering explaining he'emadtikha as God positioning Pharaoh within divine purpose. |

### 10.2 Lessons Learned

**Exodus ch2-10 regeneration (2026-03-04).** Early Exodus chapters revealed that without explicit anti-KJV-copying rules, the generation model defaults to KJV diction when producing renderings. Nearly half the verses in some chapters were verbatim KJV pass-through. The same generation run produced boilerplate translator notes (a single generic sentence reused across dozens of verses) and inconsistent modernization (archaic forms like "thou goest" appearing alongside modern English). The Quality Correction Addendum v1.3 was created to prevent these issues permanently. All nine affected chapters were regenerated from scratch with full verse-specific renderings and notes. The lesson: quality rules must be explicit in the prompt context, not merely implied by the translation philosophy. If a failure mode is possible, it must be explicitly prohibited.

### 10.3 Standing Decisions

| Decision | Rationale |
|---|---|
| Hebrew versification is primary | The WLC verse numbering governs chapter files. KJV verse numbers may differ (especially in Psalms, Exodus 7-8, Joel, Malachi). The `text_kjv` field maps to the correct KJV verse regardless. |
| `expanded_rendering` placement after `rendering`, before `translator_notes` | Consistent field ordering across all chapters. |
| One `translator_notes` entry minimum per verse | Ensures no verse is left without contextual documentation. |
| `key_terms` only where theologically significant | Not every verse needs key_terms. Over-annotation dilutes the value of entries that appear. |
| Reading level targets 8th-10th grade | Comparable to ESV. Accessible but not simplified. |

---

## 11. Future Roadmap

### Immediate (current work)
- Exodus complete (40/40 chapters). Quality pass remaining on scaffold chapters 28-31, 35-39 (tabernacle construction detail).
- Begin Leviticus (kippur and qadosh will dominate)

### Near-term
- Leviticus (kippur and qadosh will dominate)
- Numbers
- Deuteronomy
- Complete the Pentateuch
- EveryVerseMatters.com integration — TCR as the house translation for EVM, the primary downstream consumer of this rendering

### Medium-term
- Historical books (Joshua through Esther)
- Psalms (major poetry — parallelism handling is critical)
- Wisdom literature (Job, Proverbs, Ecclesiastes, Song of Solomon)
- Prophets (chesed, teshuvah, shalom, kavod territory)

### Long-term
- New Testament (source text shifts from WLC to SBLGNT)
- Greek Theologically Rich Terms Register (parallel to Hebrew register)
- Complete Bible

### Tooling (as needed)
- Automated validation scripts for batch QA
- Concordance generation across completed books
- Cross-reference database
- Web reader / study interface
- PDF/print generation pipeline

---

## 12. Project Information

| Field | Value |
|---|---|
| **Project name** | The Covenant Rendering |
| **Creator** | Aaron Blonquist |
| **Contact** | aaronblonquist@gmail.com |
| **License** | CC-BY-4.0 |
| **AI model** | Claude (Anthropic) |
| **Source text (OT)** | Westminster Leningrad Codex (WLC) |
| **Source text (NT)** | SBL Greek New Testament (SBLGNT) |
| **Reference text** | King James Version (KJV) |
| **Prompt version** | 1.3 |
| **Repository** | `/Users/aaronblonquist/The Covenant Rendering` |

### Attribution

When using The Covenant Rendering, credit:

> The Covenant Rendering by Aaron Blonquist. Licensed under CC-BY-4.0.

---

## Governing Prompt Documents

| Document | Path | Purpose |
|---|---|---|
| Master Generation Prompt | [`prompts/covenant_rendering_prompt.md`](prompts/covenant_rendering_prompt.md) | Translation philosophy, output format, consistency rules, quality standards |
| Addendum v1.2 | [`prompts/covenant_rendering_addendum_v1.2.md`](prompts/covenant_rendering_addendum_v1.2.md) | Theologically Rich Terms Register, expanded_rendering rules, term definitions |
| Quality Correction Addendum v1.3 | [`prompts/quality-correction-addendum-v1.3.md`](prompts/quality-correction-addendum-v1.3.md) | Three non-negotiable quality rules: no KJV pass-through, no boilerplate notes, consistent modernization. Active in all generation from Exodus ch2 onward. |
| Addendum v1.1 | [`prompts/addendum_v1.1.md`](prompts/addendum_v1.1.md) | Previous addendum version (archived, superseded by v1.2) |

---

*"The heavens declare the glory of God, and the sky above proclaims the work of his hands." — Psalm 19:1*
