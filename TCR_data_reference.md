# The Covenant Rendering — Data Reference

*What data and resources exist, and how do we use them?*

**Owner:** Aaron Blonquist
**Created:** 2026-02-27
**Last updated:** 2026-03-28
**Version:** 2.0

---

## System Reference

| Document | File | Question It Answers |
|---|---|---|
| Source of Truth | `TCR_source_of_truth.md` | What are we building? What's the current status? |
| **Data Reference** | **`TCR_data_reference.md`** | **What data exists? What are the schemas and terms?** |
| Quality Contract | `TCR_quality_contract.md` | What must be true for output to be correct? |
| Operational Playbook | `TCR_operational_playbook.md` | How do we generate, deploy, and operate? |

### Governing Prompt Documents

| Document | Path | Purpose |
|---|---|---|
| Master Generation Prompt | [`prompts/covenant_rendering_prompt.md`](prompts/covenant_rendering_prompt.md) | Translation philosophy, output format, consistency rules, quality standards |
| Addendum v1.2 | [`prompts/covenant_rendering_addendum_v1.2.md`](prompts/covenant_rendering_addendum_v1.2.md) | Theologically Rich Terms Register, expanded_rendering rules, term definitions |
| Quality Correction Addendum v1.3 | [`prompts/quality-correction-addendum-v1.3.md`](prompts/quality-correction-addendum-v1.3.md) | Three non-negotiable quality rules |
| QA Agent Prompt | [`prompts/qa_agent_prompt.md`](prompts/qa_agent_prompt.md) | QA validation rules, verdict format, two-agent pipeline enforcement |
| Leviticus Briefing | [`prompts/leviticus-briefing-addendum.md`](prompts/leviticus-briefing-addendum.md) | Leviticus-specific vocabulary, offerings, purity, watch chapters |

---

## 1. Source Texts

| Testament | Source Text | Description |
|---|---|---|
| Old Testament | Westminster Leningrad Codex (WLC) | The standard Masoretic Text used by all major modern translations |
| New Testament | SBL Greek New Testament (SBLGNT) | Critical text, equivalent to NA28/UBS5 |
| Reference | King James Version (KJV) | Provided for reader comparison only — never used as a translation source |

---

## 2. File Structure

**Data repo** (`~/The Covenant Rendering/` → github.com/bashonda2/the-covenant-rendering):
```
The Covenant Rendering/
├── TCR_source_of_truth.md          # Project identity, status, roadmap
├── TCR_data_reference.md           # This document — schemas, terms, field rules
├── TCR_quality_contract.md         # Quality rules, validation, decisions log
├── TCR_operational_playbook.md     # Generation pipeline, website, deployment
├── README.md                       # Public-facing project description
├── LICENSE                         # CC-BY-4.0
├── prompts/
│   ├── covenant_rendering_prompt.md        # Master generation prompt
│   ├── covenant_rendering_addendum_v1.2.md # Theologically Rich Terms Register
│   ├── quality-correction-addendum-v1.3.md # Quality rules: no KJV copying, no boilerplate, modern English
│   ├── qa_agent_prompt.md                  # QA validation rules, two-agent pipeline enforcement
│   ├── leviticus-briefing-addendum.md      # Leviticus-specific vocabulary, offerings, purity, watch chapters
│   ├── addendum_v1.1.md                    # Previous addendum version (archived)
│   └── rendering_prompt.md                 # Earlier prompt version (archived)
├── genesis/
│   ├── chapter-01.json
│   ├── chapter-02.json
│   └── ... (50 chapters)
├── exodus/
│   ├── chapter-01.json
│   ├── chapter-02.json
│   └── ... (40 chapters)
└── {book}/
    └── chapter-{NN}.json
```

**Website repo** (`~/TCR/` → github.com/bashonda2/tcr-site):
```
TCR/
├── astro.config.mjs
├── package.json
├── deploy.sh                       # Build + rsync to VPS in one command
├── public/
│   └── favicon.svg
├── src/
│   ├── data/
│   │   ├── tcr.ts                  # BOOKS registry, loadChapter(), TypeScript interfaces
│   │   ├── genesis/                # Build-time copies of JSON data
│   │   │   └── chapter-{NN}.json
│   │   └── exodus/
│   │       └── chapter-{NN}.json
│   ├── components/
│   │   └── VerseCard.astro         # Single verse display component
│   ├── layouts/
│   │   └── Layout.astro            # Base HTML, nav, footer, fonts, SEO
│   ├── pages/
│   │   ├── index.astro             # Homepage
│   │   ├── about.astro             # About / methodology
│   │   ├── [book]/
│   │   │   ├── index.astro         # Chapter grid (dynamic route)
│   │   │   └── [chapter].astro     # Verse-by-verse display (dynamic route)
│   └── styles/
│       └── global.css              # Tailwind imports, custom theme, Hebrew text styles
└── dist/                           # Build output (gitignored)
```

**Relationship between repos:** The data repo is the canonical source. JSON chapter files are *copied* into the site repo's `src/data/` directory. The site reads them at build time and generates static HTML. When new chapters are generated, they are saved to the data repo first, then copied to the site repo.

---

## 3. JSON Schema — Verse Object

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

---

## 4. JSON Schema — Chapter Object

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

---

## 5. Field Rules

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

## 6. Theologically Rich Terms Register

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

---

## 7. expanded_rendering Placement Log

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

*Version 2.0 — 2026-03-28*
